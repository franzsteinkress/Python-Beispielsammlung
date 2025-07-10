# Finanzdatenanzeige

Eine einfache Tkinter-basierte Python-Anwendung zum Anzeigen von CSV-Dateien von Banken in einer Tabelle.

## Voraussetzungen
- Python 3.13.4 oder höher
- Keine externen Bibliotheken erforderlich (nutzt Standardbibliotheken: tkinter, csv, os)

## Installation
1. Klone das Repository oder kopiere die Dateien.
2. Stelle sicher, dass Python 3.13.4 installiert ist:
   ```bash
   python --version
   ```
2. Optional: Erstelle und aktiviere eine virtuelle Umgebung:
   ```bash
   cd ./Finanzdatenanzeige
   python -m venv .venv
   .venv\Scripts\Activate.ps1
   ```
3. Starte die Anwendung:
   ```bash
   python finanzdatenanzeige_app.py
   ```

## Nutzung
- Klicke auf „CSV-Datei öffnen“ oder nutze das Menü „Datei > Öffnen“.
- Wähle eine CSV-Datei (z. B. mit Spalten wie Datum, Betrag, Beschreibung).
- Die Daten werden in einer Tabelle angezeigt.
- Unterstützt UTF-8-Encoding mit BOM (typisch für Bank-CSVs).

## Lizenz
Die Anwendung ist unter der MIT-Lizenz lizenziert. Siehe `LICENSE` für Details.