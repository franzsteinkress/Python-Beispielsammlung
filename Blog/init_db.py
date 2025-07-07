# init_db.py
# Initialisiert die SQLite-Datenbank für die Blog-Anwendung

import sqlite3

# Verbindung zur Datenbank herstellen
db_connection = sqlite3.connect("database.db")

# Schema-Skript ausführen
with open("schema.sql") as file:
    db_connection.executescript(file.read())

# Cursor für Datenbankoperationen
db_cursor = db_connection.cursor()

# Beispielposts einfügen
db_cursor.execute("INSERT INTO posts (title, content) VALUES (?, ?)",
                  ("Erster Post", "Inhalt des ersten Posts"))
db_cursor.execute("INSERT INTO posts (title, content) VALUES (?, ?)",
                  ("Zweiter Post", "Inhalt des zweiten Posts"))

# Änderungen speichern und Verbindung schließen
db_connection.commit()
db_connection.close()