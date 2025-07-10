# Notizenverwaltung

Eine Flask-basierte REST-API zur Verwaltung von Notizen mit SQLite-Datenbank und einer Weboberfläche zum Testen.

## Voraussetzungen
- Python 3.13.4 oder höher
- Bibliotheken: Flask, flask-cors requests

## Installation
1. Klone das Repository oder kopiere die Dateien.
2. Stelle sicher, dass Python 3.13.4 installiert ist:
   ```bash
   python --version
   ```
3. Erstelle und aktiviere eine virtuelle Umgebung:
   ```bash
   cd ./Notizenverwaltung
   python -m venv .venv
   .venv\Scripts\Activate.ps1
   ```
4. Installiere die Abhängigkeiten:
   ```bash
   pip install Flask flask-cors requests
   ```
5. Initialisiere die Datenbank:
   ```bash
   python init_db.py
   ```
6. Starte die API:
   ```bash
   python notizen_app.py
   ```

## Nutzung der API
- Die API ist unter `http://localhost:5000/api/notizen` erreichbar.
- Endpunkte:
  - `GET /api/notizen`: Listet alle Notizen.
  - `GET /api/notizen/<id>`: Ruft eine Notiz ab.
  - `POST /api/notizen`: Erstellt eine Notiz (JSON: `{"titel": "Titel", "inhalt": "Inhalt"}`).
  - `PUT /api/notizen/<id>`: Aktualisiert eine Notiz (JSON wie bei POST).
  - `DELETE /api/notizen/<id>`: Löscht eine Notiz.
- Beispiel mit `curl`:
  ```bash
  curl http://localhost:5000/api/notizen
  curl -X POST -H "Content-Type: application/json" -d '{"titel":"Neue Notiz","inhalt":"Test"}' http://localhost:5000/api/notizen
  ```

## Nutzung der Weboberfläche
- Öffne `http://localhost:5000/notizen` im Browser.
- Funktionen:
  - Zeigt alle Notizen in einer Tabelle mit ID, Titel, Inhalt, Erstellungsdatum.
  - Klick auf Titel zeigt Details in einem Modal.
  - Formular zum Erstellen neuer Notizen.
  - Bearbeitungsformular für bestehende Notizen.
  - Lösch-Button mit Bestätigung.
- Fehler werden als temporäre Meldungen angezeigt.

## Test-Alternativen
- **Browser (nur GET)**: Öffne `http://localhost:5000/api/notizen` oder `http://localhost:5000/api/notizen/<id>` für JSON-Antworten.
- **Postman**:
  - Verwende Postman (Desktop oder Web: `https://web.postman.co/`).
  - Beispiel POST:
    ```bash
    curl -X POST -H "Content-Type: application/json" -d '{"titel":"Test","inhalt":"Hallo"}' http://localhost:5000/api/notizen
    ```
- **Python `requests`**:
  ```python
  import requests
  print(requests.get("http://localhost:5000/api/notizen").json())
  print(requests.post("http://localhost:5000/api/notizen", json={"titel": "Test", "inhalt": "Hallo"}).json())
  ```
- **cURL** (siehe Beispiele oben).

## Ausführung der grafischen Benutzeroberfläche (GUI)
Die grafische Benutzeroberfläche (`notizen_gui.py`) erfordert die gleichzeitige Ausführung der REST-API (`notizen_api.py`). Dies kann durch die Nutzung von zwei separaten Terminals erreicht werden. Führen Sie die folgenden Schritte aus:

### Voraussetzungen
- Die virtuelle Umgebung ist aktiviert (`.venv\Scripts\Activate.ps1`).
- Die Datenbank (`database.db`) ist initialisiert (z. B. durch `python init_db.py`).

### Schritt-für-Schritt-Anleitung
1. **Terminal 1: Starten der REST-API**
   - Öffnen Sie ein Terminal im Projektverzeichnis (z. B. `C:\repos\Python-Beispielsammlung\Notizenverwaltung`).
   - Führen Sie den folgenden Befehl aus, um die API zu starten:
     ```powershell
     python notizen_api.py
     ```
   - Vergewissern Sie sich, dass der Server erfolgreich startet (Ausgabe: `Running on http://localhost:5000/`).

2. **Terminal 2: Starten der GUI**
   - Öffnen Sie ein zweites Terminal im gleichen Verzeichnis.
   - Führen Sie den folgenden Befehl aus, um die GUI zu starten:
     ```powershell
     python notizen_gui.py
     ```
   - Die GUI sollte ein Tkinter-Fenster öffnen und die Notizen von der API abrufen.

### Hinweise
- Beide Terminals müssen gleichzeitig aktiv bleiben, da die GUI auf die laufende API angewiesen ist.
- Verwenden Sie Visual Studio Code, um die Terminals effizient zu verwalten (Menü: `Terminal > Neues Terminal` oder `Terminal > Terminal teilen`).

## http://localhost:5000/api/notizen
- Zeigt alle Notizen als JSON an.
- Beispielausgabe:
  ```json
  [
    {
      "erstellt": "2025-07-06 22:29:53",
      "id": 1,
      "inhalt": "Dies ist der Inhalt der ersten Notiz",
      "titel": "Erste Notiz"
    }
  ]
  ```

## http://localhost:5000/notizen
- Öffnet die Weboberfläche zur interaktiven Verwaltung der Notizen.
- Enthält Formulare zum Erstellen, Bearbeiten und Löschen sowie eine Tabelle mit Notizen.

## F12
- Öffne die Entwicklertools im Browser (Taste F12).
- Nutze den Reiter "Konsole" für JavaScript-Fehler und "Netzwerk" für API-Anfragen, um Probleme zu debuggen.

## sqlite3 database.db "SELECT * FROM notizen;"
- Überprüfe die Datenbankinhalte manuell:
  ```powershell
  sqlite3 database.db "SELECT * FROM notizen;"
  ```
- Zeigt alle Notizen mit ID, Titel, Inhalt und Erstellungsdatum an.

## Lizenz
Die Anwendung ist unter der [MIT-Lizenz](../LICENSE) lizenziert.