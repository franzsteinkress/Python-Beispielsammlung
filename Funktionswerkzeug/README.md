# Funktionswerkzeug

Eine Tkinter-basierte Python-Anwendung mit verschiedenen Werkzeugen:
- Akronym-Generator
- BMI-Rechner
- Farbiger Text
- Würfel-Simulator
- Fahrenheit-zu-Celsius-Konverter
- Passwort-Generator
- QR-Code-Generator
- Römische-Zahlen-Konverter

## Voraussetzungen
- Python 3.13.4 oder höher
- Bibliotheken: `colorama`, `pyqrcode`, `pypng`, `pillow`
- Tkinter (in Python enthalten)

## Installation
1. Klone das Repository oder kopiere die Dateien.
2. Stelle sicher, dass Python 3.13.4 installiert ist:
   ```bash
   python --version
   ```
3. Erstelle und aktiviere eine virtuelle Umgebung:
   ```bash
   cd ./Funktionswerkzeug
   python -m venv .venv
   .venv\Scripts\Activate.ps1
   ```
4. Installiere die Abhängigkeiten:
   ```bash
   pip install colorama pyqrcode pypng pillow
   ```
5. Starte die Anwendung:
   ```bash
   python funktionswerkzeug_app.py
   ```

## Nutzung
- Wähle ein Werkzeug über die Buttons im Hauptfenster.
- Gib die erforderlichen Eingaben ein und klicke auf die entsprechenden Buttons.
- QR-Codes werden in `static/qr_codes/` gespeichert.

## Lizenz
Die Anwendung ist unter der MIT-Lizenz lizenziert. Siehe `LICENSE` für Details.