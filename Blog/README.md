# Blog-Anwendung

Eine einfache Blog-Anwendung mit Flask und SQLite, die das Erstellen, Bearbeiten, Anzeigen und Löschen von Blog-Posts ermöglicht.

## Voraussetzungen
- Python 3.13.4 oder höher
- Flask (`pip install Flask`)

## Installation
1. Klone das Repository oder kopiere die Dateien.
2. Stelle sicher, dass Python 3.13.4 installiert ist:
   ```bash
   python --version
   ```
3. Erstelle und aktiviere eine virtuelle Umgebung:
   ```bash
   cd ./Blog
   python -m venv .venv
   .venv\Scripts\Activate.ps1
   ```
4. Installiere Flask:
   ```bash
   pip install Flask
   ```
5. Initialisiere die Datenbank:
   ```bash
   python init_db.py
   ```
6. Starte die Anwendung:
   ```bash
   python blog_app.py
   ```

## Nutzung
- Öffne `http://localhost:5000` im Browser.
- Erstelle neue Posts über „Neuer Post“.
- Bearbeite oder lösche Posts auf der Startseite oder der Post-Seite.

## Hinweis
- **Debug-Modus**: Die Anwendung läuft standardmäßig im Debug-Modus, was detaillierte Fehlerseiten und automatisches Neuladen bei Code-Änderungen ermöglicht. Dies ist für die Entwicklung gedacht. Um den Debug-Modus zu deaktivieren (z. B. für Produktion), setze `app.debug = False` oder führe die Anwendung mit `FLASK_ENV=production flask run` aus. Beachte, dass der Debug-Modus Sicherheitsrisiken in einer öffentlichen Umgebung birgt.

## Lizenz
Die Anwendung ist unter der [MIT-Lizenz](../LICENSE) lizenziert.