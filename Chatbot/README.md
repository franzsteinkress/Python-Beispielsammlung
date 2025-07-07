# Chatbot Simulator

Eine einfache Flask-Webanwendung mit einem rudimentären Chatbot Simulator, der auf Benutzereingaben antwortet.

## Voraussetzungen
- Python 3.13.4 oder höher
- Flask (`pip install Flask`)

## Installation
1. Klone das Repository oder kopiere die Dateien `chatbot_app.py` und `templates/index.html`.
2. Erstelle ein Verzeichnis `templates` und speichere `index.html` darin.
3. Stelle sicher, dass Python 3.13.4 installiert ist:
   ```bash
   python --version
   ```
4. Erstelle und aktiviere eine virtuelle Umgebung:
   ```bash
   cd ./ChatBot
   python -m venv .venv
   .venv\Scripts\activate
   ```
5. Installiere Flask:
   ```bash
   pip install Flask
   ```
6. Starte die Anwendung:
   ```bash
   python chatbot_app.py
   ```

## Nutzung
- Öffne einen Browser und gehe zu `http://localhost:5000`.
- Gib eine Nachricht in das Eingabefeld ein und klicke auf „Senden“ oder drücke Enter.
- Der Chatbot gibt eine einfache Antwort zurück, die deine Eingabe widerspiegelt.

## Einschränkungen
- Der Chatbot ist eine vereinfachte Dummy-Funktion. Für einen vollwertigen Chatbot wäre eine KI-Bibliothek (z. B. `transformers`) oder eine API erforderlich.
- Die Anwendung läuft standardmäßig im Debug-Modus (nur für Entwicklung), was detaillierte Fehlerseiten und automatisches Neuladen bei Code-Änderungen ermöglicht. Um den Debug-Modus zu deaktivieren (z. B. für Produktion), setze `app.debug = False`.

## Lizenz
Die Anwendung ist unter der MIT-Lizenz lizenziert. Siehe `LICENSE` für Details.