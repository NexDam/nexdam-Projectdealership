# NexDam Motors - Web App Concessionaria

Web app per la gestione di una concessionaria auto: catalogo veicoli, dettaglio, richieste di contatto e pannello admin per gestire i veicoli.

**Stack:** Python (Flask) per il backend, MySQL (fornito da XAMPP) come database, HTML/CSS/JavaScript per il frontend.

## Struttura del progetto

```
nexdam-ProjectDealership/
├── app/
│   ├── app.py            # applicazione Flask (route)
│   ├── db.py             # connessione al database MySQL
│   ├── templates/        # pagine HTML (Jinja2)
│   └── static/           # CSS, JS e immagini
├── database/
│   └── schema.sql        # schema del database + dati di esempio
├── seed_admin.py         # crea l'utente amministratore
├── requirements.txt
└── .env.example
```

## 1. Avviare MySQL con XAMPP

1. Apri **XAMPP Control Panel**.
2. Avvia il modulo **MySQL** (Apache non è necessario, perché il sito viene servito da Flask).
3. Apri **phpMyAdmin** (`http://localhost/phpmyadmin`).
4. Vai su **Importa** e seleziona il file `database/schema.sql` di questo progetto, oppure copia/incolla il contenuto nella tab SQL ed esegui.
   - Questo crea il database `concessionaria`, le tabelle e alcuni veicoli di esempio.

## 2. Configurare il progetto Python

Apri un terminale nella cartella del progetto:

```bash
python -m venv .venv
.venv\Scripts\activate      # su Windows (PowerShell/cmd)
pip install -r requirements.txt
```

Copia `.env.example` in `.env` e adatta i valori se necessario (di default XAMPP usa utente `root` senza password):

```bash
copy .env.example .env
```

## 3. Creare l'utente amministratore

```bash
python seed_admin.py
```

Verranno create le credenziali di default:
- **username:** `admin`
- **password:** `admin123`

Cambia la password dopo il primo accesso (puoi aggiornarla direttamente nel database, nella tabella `admin`).

## 4. Avviare l'applicazione

```bash
cd app
python app.py
```

L'app sarà disponibile su **http://localhost:5000**

- Sito pubblico: catalogo, dettaglio veicolo, pagina contatti.
- Area admin: `http://localhost:5000/admin/login` per aggiungere, modificare ed eliminare veicoli, e per vedere le richieste di contatto inviate dagli utenti.

## Note

- Le immagini dei veicoli vanno inserite in `app/static/images/cars/`; se un veicolo non ha un'immagine specifica viene mostrato un placeholder (`default-car.svg`).
- Il database va sempre avviato tramite il modulo MySQL di XAMPP prima di lanciare `app.py`.
