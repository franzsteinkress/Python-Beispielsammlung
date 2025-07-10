# Bestätigungsdialog

Eine einfache Tkinter-Anwendung, die ein Hauptfenster mit einem Button anzeigt, der einen nicht modalen Bestätigungsdialog öffnet. Der Dialog fragt, ob der Benutzer fortfahren möchte, und bietet Optionen „Ja“ oder „Nein“.

## Voraussetzungen
- Python 3.13.4 oder höher
- Tkinter (in der Python-Standardbibliothek enthalten)

## Installation
1. Klone das Repository oder kopiere die Datei `bestaetigung_app.py`.
2. Stelle sicher, dass Python 3.13.4 installiert ist:
   ```bash
   python --version
   ```
3. Erstelle und aktiviere eine virtuelle Umgebung:
   ```bash
   cd ./Bestaetigungsdialog
   python -m venv .venv
   .venv\Scripts\Activate.ps1
   ```
4. Starte die Anwendung:
   ```bash
   python bestaetigung_app.py
   ```

## Nutzung
- Klicke auf „Drücken Sie hier“, um einen nicht modalen Bestätigungsdialog zu öffnen.
- Wähle im Dialog:
  * „Ja“: Schließt den Dialog und fährt fort.
  * „Nein“: Schließt den Dialog und die gesamte Anwendung.

## Lizenz
Die Anwendung ist unter der MIT-Lizenz lizenziert. Siehe `LICENSE` für Details.