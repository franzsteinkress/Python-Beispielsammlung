# Blockchain-Demo

Eine Ethereum-Blockchain-Demo mit Tkinter-Bedienoberfläche.
Die Demo stellt grundlegende Funktionen bereit, wie die Verbindung zu einer Ganache-Blockchain (http://127.0.0.1:7545), das Abrufen von Kontoständen und das Senden von Transaktionen zwischen Konten. Die GUI zeigt eine Dropdown-Liste für Sender-Konten, Eingabefelder für Empfängeradresse, Betrag und privaten Schlüssel, sowie Buttons zum Abrufen des Kontostands und Senden von Transaktionen. Feedback über Erfolg oder Fehler (inklusive Transaktions-Hashes) wird angezeigt.

## Voraussetzungen
- Python 3.13.4 oder höher
- Ganache (lokale Ethereum-Blockchain, Version 2.7.1 oder höher)
- Bibliotheken: `web3`, `requests`
- Tkinter (in Python enthalten)
- Eine `.ico`-Datei (z. B. `fs.ico`) für das Fenstersymbol

## Installation
1. **Ganache herunterladen und installieren**:
   - Lade Ganache von [https://trufflesuite.com/ganache/](https://trufflesuite.com/ganache/) (z. B. `Ganache-2.7.1-win-x64.appx` für Windows) herunter.
   - Doppelklicke auf die `.appx`-Datei. Falls nötig, aktiviere den Entwicklermodus unter **Einstellungen > Datenschutz und Sicherheit > Für Entwickler** und installiere über PowerShell mit:
     ```powershell
     Add-AppxPackage .\Ganache-2.7.1-win-x64.appx
     ```
   - Starte Ganache nach der Installation. Die Standard-URL ist `http://127.0.0.1:7545`.

2. **Projekt einrichten**:
   - Klone das Repository oder kopiere die Dateien (z. B. `blockchain_app.py`).
   - Stelle sicher, dass Python 3.13.4 oder höher installiert ist:
     ```bash
     python --version
     ```
   - Erstelle und aktiviere eine virtuelle Umgebung:
     ```bash
     cd ./Blockchain
     python -m venv .venv
     .venv\Scripts\Activate.ps1
     ```
   - Installiere die Abhängigkeiten:
     ```bash
     pip install web3 requests
     ```
   - Kopiere eine `.ico`-Datei (z. B. `fs.ico`) in das Projektverzeichnis.

3. **Anwendung starten**:
   - Starte die Anwendung:
     ```bash
     python blockchain_app.py
     ```

## Nutzung
- **Ganache starten**: Öffne Ganache, wähle **Quickstart Ethereum**, und notiere dir die Konten-Adressen und privaten Schlüssel (unter **Accounts**) für Tests.
- **GUI öffnen**: Die Anwendung zeigt ein Fenster mit einer Dropdown-Liste für Sender-Konten.
- **Kontostand abrufen**: Wähle ein Konto aus und klicke auf „Kontostand abrufen“, um den Kontostand in Ether anzuzeigen.
- **Transaktion senden**:
  - Gib eine gültige Empfängeradresse (aus Ganache) ein.
  - Gib einen Betrag in Ether ein.
  - Gib den privaten Schlüssel des Sender-Kontos ein (aus Ganache, z. B. mit `show="*"` maskiert).
  - Klicke auf „Transaktion senden“. Alle drei Felder müssen ausgefüllt sein, sonst erscheint eine Fehlermeldung.
- **Feedback**: Der Transaktionsstatus (z. B. „Erfolgreich (Hash: ...)“) wird ohne Wortumbruch angezeigt, mit bis zu drei Zeilen, abhängig von der Fensterbreite.

## Hinweis
- Diese Demo verwendet Ganache für eine lokale Blockchain. Für echte Ethereum-Netzwerke (z. B. Sepolia) benötigst du Ether und einen Node-Provider (z. B. Infura).
- Private Schlüssel sollten in Produktionsumgebungen sicher verwaltet werden (z. B. mit Wallets wie MetaMask), nicht direkt eingegeben werden.
- Der Transaktions-Hash wird als durchgehender String angezeigt; bei Überschreiten der Fensterbreite wird er abgeschnitten.

## Lizenz
Die Anwendung ist unter der MIT-Lizenz lizenziert. Siehe `LICENSE` für Details.