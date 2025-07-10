# Lizenzpruefer

Ein Python-basiertes Lizenzprüfungssystem, das Lizenzdateien mit RSA-Signaturen validiert.

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
   cd ./Lizenzpruefer
   python -m venv .venv
   .venv\Scripts\Activate.ps1
   ```
4. Installiere die Abhängigkeit:
   ```bash
   pip install cryptography pillow
   ```
5. Starte die Anwendung:
   ```bash
   python lizenzpruefer.py --help
   ```

## Nutzung
- **Schlüsselpaar generieren**:
   ```bash
   python lizenzpruefer.py --generiere-schluessel
   ```
- **Lizenzdatei erstellen**:
   ```bash
   python lizenzpruefer.py --erstelle-lizenz --lizenznehmer "Max Mustermann" --ablaufdatum "2026-12-31" --produkt-id "PROD123" --lizenz-datei config/licenses/lizenz.json
   ```
- **Lizenzdatei prüfen**:
   ```bash
   python lizenzpruefer.py --pruefe-lizenz --lizenz-datei config/licenses/lizenz.json
   ```
- Ausgabe zeigt, ob die Lizenz gültig ist, und gibt Lizenznehmer, Produkt-ID und Ablaufdatum an.

### Grafische Benutzeroberfläche (GUI)
Neben der Kommandozeilen-Nutzung bietet das Projekt eine grafische Benutzeroberfläche, die in `lizenzpruefer_gui.py` implementiert ist. Diese ermöglicht eine intuitive Bedienung der folgenden Funktionen:

- **Schlüsselpaar generieren**: 
Ein Button startet die Schlüsselpaar-Erstellung mit `lizenzpruefer.py --generiere-schluessel`.
- **Lizenzdatei erstellen**: 
Eingabefelder für Lizenznehmer, Ablaufdatum (im Format YYYY-MM-DD), Produkt-ID und Lizenzdatei-Pfad ermöglichen die Erstellung einer Lizenz mit `lizenzpruefer.py --erstelle-lizenz`.
- **Lizenzdatei prüfen**: 
Ein Eingabefeld für den Pfad zur Lizenzdatei startet die Prüfung mit `lizenzpruefer.py --pruefe-lizenz`.

#### GUI-Start
1. Aktiviere die virtuelle Umgebung:
   ```bash
   .venv\Scripts\Activate.ps1
   ```
2. Führe das GUI-Skript aus:
   ```bash
   python lizenzpruefer_gui.py
   ```
- Das GUI verwendet ein benutzerdefiniertes Icon (`fs.ico`), das im gleichen Verzeichnis liegen muss.
- Ergebnisse und Fehlermeldungen werden in Pop-up-Fenstern angezeigt.

## Lizenz
Die Anwendung ist unter der MIT-Lizenz lizenziert. Siehe `LICENSE` für Details.