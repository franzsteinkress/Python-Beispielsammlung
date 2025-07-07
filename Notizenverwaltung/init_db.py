# init_db.py
# Initialisiert die SQLite-Datenbank für die Notizen-API

import sqlite3

# Verbindung zur Datenbank herstellen
datenbank_verbindung = sqlite3.connect("database.db")

# Schema-Skript ausführen
with open("schema.sql") as datei:
    datenbank_verbindung.executescript(datei.read())

# Beispielnotizen einfügen
cursor = datenbank_verbindung.cursor()
cursor.execute(
    "INSERT INTO notizen (titel, inhalt) VALUES (?, ?)",
    ("Erste Notiz", "Dies ist der Inhalt der ersten Notiz")
)
cursor.execute(
    "INSERT INTO notizen (titel, inhalt) VALUES (?, ?)",
    ("Zweite Notiz", "Dies ist der Inhalt der zweiten Notiz")
)

# Änderungen speichern und Verbindung schließen
datenbank_verbindung.commit()
datenbank_verbindung.close()