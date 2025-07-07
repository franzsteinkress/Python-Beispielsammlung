# Funktionsdialog

Eine Tkinter-basierte Python-Anwendung mit einem Texteditor und Werkzeugen wie Uhr, Fortschrittsbalken, Bildbetrachter und mehr.

## Voraussetzungen
- Python 3.13.4 oder höher
- Tkinter (Standardbibliothek)
- Pillow (`pip install Pillow`)

## Installation
1. Klone das Repository oder kopiere die Datei `funktionsdialog_app.py`.
2. Stelle sicher, dass Python 3.13.4 installiert ist:
   ```bash
   python --version
   ```
3. Erstelle und aktiviere eine virtuelle Umgebung:
   ```bash
   cd ./Funktionsdialog
   python -m venv .venv
   .venv\Scripts\activate
   ```
4. Installiere Pillow:
   ```bash
   pip install Pillow
   ```
5. Starte die Anwendung:
   ```bash
   python funktionsdialog_app.py
   ```

## Nutzung
- **Texteditor**:
  * Neuen Text erstellen, öffnen, speichern oder beenden.
  * Werkzeuge über das Menü aufrufen.
- **Werkzeuge**:
  * Uhr: Zeigt eine digitale Uhr an.
  * Fortschrittsbalken: Zeigt animierte Fortschrittsbalken.
  * Kalkulator: Öffnet den Systemrechner.
  * Bildbetrachter: Zeigt Bilder an (JPEG, PNG).
  * Betriebssystem-Info: Zeigt Systeminformationen.
  * Übersetzer: Vereinfachte Demo (für echte Übersetzung API erforderlich).

## Einschränkungen
- Der Übersetzer ist eine Dummy-Funktion. Für echte Übersetzungen ist eine API erforderlich.
- Video- und Mediaplayer werden nicht verwendet. Nutze externe Player wie VLC.
- Einige Funktionen (z. B. Bildbetrachter) sind auf einfache Formate beschränkt.

## Lizenz
Die Anwendung ist unter der MIT-Liz-Lizenz lizenziert. Siehe `LICENSE.md` für Details.