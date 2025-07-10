# Verschluesselung

Ein einfaches AES-Verschlüsselungstool in Python mit der `cryptography`-Bibliothek.

## Voraussetzungen
- Python 3.13.4 oder höher
- Bibliothek: `cryptography`

## Installation
1. Klone das Repository oder kopiere die Dateien.
2. Stelle sicher, dass Python 3.13.4 installiert ist:
   ```bash
   python --version
   ```
3. Erstelle und aktiviere eine virtuelle Umgebung:
   ```bash
   cd ./Verschluesselung
   python -m venv .venv
   .venv\Scripts\Activate.ps1
   ```
4. Installiere die Abhängigkeit:
   ```bash
   pip install cryptography
   ```
5. Starte die Anwendung:
   ```bash
   python aesverschluesselung.py --help
   ```

## Nutzung
- **Verschlüsseln**:
  ```bash
  python aesverschluesselung.py --verschluesseln "Hallo Welt" --passwort meinPasswort123 --ausgabe verschluesselt.bin
  ```
- **Entschlüsseln und Überprüfen**:
  ```bash
  python aesverschluesselung.py --entschluesseln --passwort meinPasswort123 --eingabe verschluesselt.bin --original "Hallo Welt"
  ```
- Ausgabe zeigt den entschlüsselten Text und ob er mit dem Original übereinstimmt.
- Falsches Passwort oder ungültige Dateien führen zu Fehlermeldungen.

### Grafische Benutzeroberfläche (GUI)
Neben der Kommandozeilen-Nutzung bietet das Projekt eine grafische Benutzeroberfläche, die in `verschluesselung_gui.py` implementiert ist. Diese ermöglicht eine benutzerfreundliche Bedienung der folgenden Funktionen:

- **Verschlüsseln**: 
Eingabefelder für den Text, das Passwort und die Ausgabedatei (Standard: `verschluesselt.bin`) starten die Verschlüsselung mit `aesverschluesselung.py --verschluesseln`.
- **Entschlüsseln und Überprüfen**: 
Eingabefelder für das Passwort, die Eingabedatei (Standard: `verschluesselt.bin`) und den Originaltext ermöglichen die Entschlüsselung und Vergleich mit `aesverschluesselung.py --entschluesseln`. Das Ergebnis zeigt den entschlüsselten Text und ob er mit dem Original übereinstimmt.

#### GUI-Start
1. Aktiviere die virtuelle Umgebung:
   ```bash
   .venv\Scripts\Activate.ps1
   ```
2. Führe das GUI-Skript aus:
   ```bash
   python verschluesselung_gui.py
   ```
- Das GUI verwendet ein benutzerdefiniertes Icon (`fs.ico`), das im gleichen Verzeichnis liegen muss.
- Ergebnisse und Fehlermeldungen (z. B. bei falschem Passwort oder ungültigen Dateien) werden in Pop-up-Fenstern angezeigt.

## Lizenz
Die Anwendung ist unter der [MIT-Lizenz](../LICENSE) lizenziert.