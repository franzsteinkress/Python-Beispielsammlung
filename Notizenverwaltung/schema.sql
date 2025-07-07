-- schema.sql
-- Definiert das Schema für die Notizen-Datenbank

DROP TABLE IF EXISTS notizen;

CREATE TABLE notizen (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    erstellt TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    titel TEXT NOT NULL,
    inhalt TEXT NOT NULL
);