"""Crea l'utente amministratore di default nel database.

Esegui dopo aver importato database/schema.sql:
    python seed_admin.py
"""
import os
from dotenv import load_dotenv
from werkzeug.security import generate_password_hash

load_dotenv()

from app.db import execute, query  # noqa: E402

DEFAULT_USERNAME = "admin"
DEFAULT_PASSWORD = "admin123"


def main():
    existing = query("SELECT id FROM admin WHERE username = %s", (DEFAULT_USERNAME,), fetchone=True)
    if existing:
        print(f"L'utente admin '{DEFAULT_USERNAME}' esiste già.")
        return
    password_hash = generate_password_hash(DEFAULT_PASSWORD)
    execute("INSERT INTO admin (username, password_hash) VALUES (%s, %s)", (DEFAULT_USERNAME, password_hash))
    print(f"Utente admin creato -> username: {DEFAULT_USERNAME} password: {DEFAULT_PASSWORD}")
    print("IMPORTANTE: cambia la password dopo il primo accesso.")


if __name__ == "__main__":
    main()
