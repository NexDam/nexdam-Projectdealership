import os
from functools import wraps

from dotenv import load_dotenv
from flask import Flask, render_template, request, redirect, url_for, session, flash
from werkzeug.security import check_password_hash
from werkzeug.utils import secure_filename

load_dotenv()

from db import query, execute  # noqa: E402

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "dev-secret-key")

# Upload delle foto dei veicoli
IMMAGINE_DEFAULT = "default-car.webp"
ESTENSIONI_IMMAGINE = {".webp", ".jpg", ".jpeg", ".png"}
MAX_UPLOAD_MB = 4
app.config["MAX_CONTENT_LENGTH"] = MAX_UPLOAD_MB * 1024 * 1024


def login_required(view):
    @wraps(view)
    def wrapped(*args, **kwargs):
        if not session.get("admin_id"):
            return redirect(url_for("admin_login"))
        return view(*args, **kwargs)
    return wrapped


# ---------- Pagine pubbliche ----------

@app.route("/")
def home():
    auto_in_evidenza = query(
        "SELECT * FROM veicoli WHERE disponibile = 1 ORDER BY creato_il DESC LIMIT 6"
    )
    return render_template("index.html", auto=auto_in_evidenza)


@app.route("/catalogo")
def catalogo():
    marca = request.args.get("marca", "").strip()
    carburante = request.args.get("carburante", "").strip()
    prezzo_max = request.args.get("prezzo_max", "").strip()

    sql = "SELECT * FROM veicoli WHERE disponibile = 1"
    params = []

    if marca:
        sql += " AND marca = %s"
        params.append(marca)
    if carburante:
        sql += " AND carburante = %s"
        params.append(carburante)
    if prezzo_max:
        sql += " AND prezzo <= %s"
        params.append(prezzo_max)

    sql += " ORDER BY prezzo ASC"

    veicoli = query(sql, params)
    marche = query("SELECT DISTINCT marca FROM veicoli ORDER BY marca")
    return render_template(
        "catalogo.html",
        veicoli=veicoli,
        marche=marche,
        filtri={"marca": marca, "carburante": carburante, "prezzo_max": prezzo_max},
    )


@app.route("/veicolo/<int:veicolo_id>")
def dettaglio_veicolo(veicolo_id):
    veicolo = query("SELECT * FROM veicoli WHERE id = %s", (veicolo_id,), fetchone=True)
    if not veicolo:
        flash("Veicolo non trovato.", "error")
        return redirect(url_for("catalogo"))
    return render_template("dettaglio.html", veicolo=veicolo)


@app.route("/contatti", methods=["GET", "POST"])
def contatti():
    if request.method == "POST":
        nome = request.form.get("nome", "").strip()
        email = request.form.get("email", "").strip()
        telefono = request.form.get("telefono", "").strip()
        messaggio = request.form.get("messaggio", "").strip()
        veicolo_id = request.form.get("veicolo_id") or None

        if not nome or not email or not messaggio:
            flash("Compila tutti i campi obbligatori.", "error")
            return redirect(url_for("contatti", veicolo_id=veicolo_id))

        execute(
            "INSERT INTO richieste_contatto (nome, email, telefono, messaggio, veicolo_id) "
            "VALUES (%s, %s, %s, %s, %s)",
            (nome, email, telefono, messaggio, veicolo_id),
        )
        flash("Richiesta inviata con successo! Ti contatteremo a breve.", "success")
        return redirect(url_for("contatti"))

    veicolo_id = request.args.get("veicolo_id")
    veicolo = None
    if veicolo_id:
        veicolo = query("SELECT * FROM veicoli WHERE id = %s", (veicolo_id,), fetchone=True)
    return render_template("contatti.html", veicolo=veicolo)


# ---------- Area amministrazione ----------

@app.route("/admin/login", methods=["GET", "POST"])
def admin_login():
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "")

        admin = query("SELECT * FROM admin WHERE username = %s", (username,), fetchone=True)
        if admin and check_password_hash(admin["password_hash"], password):
            session["admin_id"] = admin["id"]
            session["admin_username"] = admin["username"]
            return redirect(url_for("admin_dashboard"))

        flash("Credenziali non valide.", "error")
    return render_template("admin/login.html")


@app.route("/admin/logout")
def admin_logout():
    session.clear()
    return redirect(url_for("admin_login"))


@app.route("/admin")
@login_required
def admin_dashboard():
    veicoli = query("SELECT * FROM veicoli ORDER BY creato_il DESC")
    richieste = query(
        "SELECT r.*, v.marca, v.modello FROM richieste_contatto r "
        "LEFT JOIN veicoli v ON v.id = r.veicolo_id ORDER BY r.creato_il DESC LIMIT 20"
    )
    non_lette = query(
        "SELECT COUNT(*) AS n FROM richieste_contatto WHERE letto = 0", fetchone=True
    )["n"]
    return render_template(
        "admin/dashboard.html", veicoli=veicoli, richieste=richieste, non_lette=non_lette
    )


@app.route("/admin/richiesta/<int:richiesta_id>/letto", methods=["POST"])
@login_required
def admin_segna_richiesta(richiesta_id):
    richiesta = query(
        "SELECT letto FROM richieste_contatto WHERE id = %s", (richiesta_id,), fetchone=True
    )
    if not richiesta:
        flash("Richiesta non trovata.", "error")
        return redirect(url_for("admin_dashboard"))

    nuovo_stato = 0 if richiesta["letto"] else 1
    execute(
        "UPDATE richieste_contatto SET letto = %s WHERE id = %s", (nuovo_stato, richiesta_id)
    )
    flash(
        "Richiesta segnata come letta." if nuovo_stato else "Richiesta rimessa tra le da leggere.",
        "success",
    )
    return redirect(url_for("admin_dashboard"))


@app.route("/admin/veicolo/nuovo", methods=["GET", "POST"])
@login_required
def admin_nuovo_veicolo():
    if request.method == "POST":
        _salva_veicolo()
        flash("Veicolo aggiunto.", "success")
        return redirect(url_for("admin_dashboard"))
    return render_template("admin/form_veicolo.html", veicolo=None)


@app.route("/admin/veicolo/<int:veicolo_id>/modifica", methods=["GET", "POST"])
@login_required
def admin_modifica_veicolo(veicolo_id):
    veicolo = query("SELECT * FROM veicoli WHERE id = %s", (veicolo_id,), fetchone=True)
    if not veicolo:
        flash("Veicolo non trovato.", "error")
        return redirect(url_for("admin_dashboard"))

    if request.method == "POST":
        _salva_veicolo(veicolo_id)
        flash("Veicolo aggiornato.", "success")
        return redirect(url_for("admin_dashboard"))

    return render_template("admin/form_veicolo.html", veicolo=veicolo)


@app.route("/admin/veicolo/<int:veicolo_id>/elimina", methods=["POST"])
@login_required
def admin_elimina_veicolo(veicolo_id):
    execute("DELETE FROM veicoli WHERE id = %s", (veicolo_id,))
    flash("Veicolo eliminato.", "success")
    return redirect(url_for("admin_dashboard"))


def _cartella_immagini():
    return os.path.join(app.static_folder, "images", "cars")


def _salva_immagine(file_caricato):
    """Salva la foto caricata e ne restituisce il nome file.

    Restituisce None se non e stato caricato nulla o se il file e stato
    rifiutato; in quel caso il chiamante mantiene l'immagine precedente.
    """
    if not file_caricato or not file_caricato.filename:
        return None

    nome = secure_filename(file_caricato.filename)
    estensione = os.path.splitext(nome)[1].lower()
    if not nome or estensione not in ESTENSIONI_IMMAGINE:
        flash(
            "Formato immagine non supportato: sono ammessi WEBP, JPG e PNG. "
            "L'immagine precedente e stata mantenuta.",
            "error",
        )
        return None

    cartella = _cartella_immagini()
    os.makedirs(cartella, exist_ok=True)

    # Non sovrascrivere un file gia presente: aggiunge un suffisso numerico.
    base = os.path.splitext(nome)[0]
    definitivo = nome
    contatore = 1
    while os.path.exists(os.path.join(cartella, definitivo)):
        definitivo = f"{base}-{contatore}{estensione}"
        contatore += 1

    file_caricato.save(os.path.join(cartella, definitivo))
    return definitivo


def _salva_veicolo(veicolo_id=None):
    immagine = _salva_immagine(request.files.get("immagine"))
    if immagine is None and veicolo_id:
        precedente = query(
            "SELECT immagine FROM veicoli WHERE id = %s", (veicolo_id,), fetchone=True
        )
        immagine = precedente["immagine"] if precedente else None
    if immagine is None:
        immagine = IMMAGINE_DEFAULT

    dati = (
        request.form.get("marca", "").strip(),
        request.form.get("modello", "").strip(),
        int(request.form.get("anno")),
        float(request.form.get("prezzo")),
        int(request.form.get("km") or 0),
        request.form.get("carburante"),
        request.form.get("cambio"),
        request.form.get("colore", "").strip(),
        request.form.get("descrizione", "").strip(),
        immagine,
        1 if request.form.get("disponibile") == "on" else 0,
    )

    if veicolo_id:
        execute(
            "UPDATE veicoli SET marca=%s, modello=%s, anno=%s, prezzo=%s, km=%s, "
            "carburante=%s, cambio=%s, colore=%s, descrizione=%s, immagine=%s, "
            "disponibile=%s WHERE id=%s",
            dati + (veicolo_id,),
        )
    else:
        execute(
            "INSERT INTO veicoli (marca, modello, anno, prezzo, km, carburante, cambio, "
            "colore, descrizione, immagine, disponibile) "
            "VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",
            dati,
        )


@app.errorhandler(413)
def immagine_troppo_grande(_):
    flash(f"Immagine troppo grande: il limite e {MAX_UPLOAD_MB} MB.", "error")
    return redirect(url_for("admin_dashboard")), 302


if __name__ == "__main__":
    app.run(debug=True, port=5000)
