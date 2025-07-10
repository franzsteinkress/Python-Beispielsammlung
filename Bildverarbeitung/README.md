# Bildverarbeitung

Eine einfache Tkinter-basierte Python-Anwendung für typische OpenCV-Bildverarbeitungsaufgaben wie Graustufen, Kantenfilter und Unschärfe.

## Voraussetzungen
- Python 3.13.4 oder höher
- Bibliotheken: `opencv-python`, `Pillow`
- Tkinter (in Python enthalten)

## Installation
1. Klone das Repository oder kopiere die Dateien.
2. Stelle sicher, dass Python 3.13.4 installiert ist:
   ```bash
   python --version
   ```
3. Erstelle und aktiviere eine virtuelle Umgebung:
   ```bash
   cd ./Bildverarbeitung
   python -m venv .venv
   .venv\Scripts\Activate.ps1
   ```
4. Installiere die Abhängigkeiten:
   ```bash
   pip install opencv-python Pillow
   ```
5. Starte die Anwendung:
   ```bash
   python bildverarbeitung_app.py
   ```

## Nutzung
- Klicke auf „Bild öffnen“ oder nutze „Datei > Bild öffnen“, um ein Bild (JPG, PNG) zu laden.
- Wende Filter an: Graustufen, Kanten, Unschärfe.
- Speichere das verarbeitete Bild über „Bild speichern“ oder „Datei > Bild speichern“.
- Bilder werden in einer maximalen Größe von 500x500 Pixeln angezeigt.

## Lizenz
Die Anwendung ist unter der [MIT-Lizenz](../LICENSE) lizenziert.