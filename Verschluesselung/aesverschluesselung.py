# Copyright (c) 2025 Franz Steinkress
# Licensed under the MIT License - see LICENSE for details
#
# aesverschluesselung.py
# Ein einfaches AES-Verschlüsselungstool mit der cryptography-Bibliothek

import os
import argparse
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend
import base64

class AESVerschluesselung:
    """Hauptklasse für die AES-Verschlüsselung und -Entschlüsselung."""
    
    def __init__(self, passwort, salz_laenge=16):
        """Initialisiert die Verschlüsselung. Leitet Schlüssel aus Passwort ab."""
        self.passwort = passwort.encode()
        self.salz_laenge = salz_laenge
        self.schluessel_laenge = 32  # AES-256 benötigt 32 Bytes
        self.iv_laenge = 16  # Initialisierungsvektor für CBC-Modus
    
    def generiere_schluessel(self, salz):
        """Leitet einen AES-Schlüssel aus dem Passwort und Salz ab."""
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=self.schluessel_laenge,
            salt=salz,
            iterations=100000,
            backend=default_backend()
        )
        return kdf.derive(self.passwort)
    
    def verschluesseln(self, klartext, ausgabe_datei):
        """Verschlüsselt den Text. Speichert in Datei."""
        try:
            klartext_bytes = klartext.encode()
            salz = os.urandom(self.salz_laenge)
            schluessel = self.generiere_schluessel(salz)
            iv = os.urandom(self.iv_laenge)
            
            cipher = Cipher(
                algorithms.AES(schluessel),
                modes.CBC(iv),
                backend=default_backend()
            )
            verschluesseler = cipher.encryptor()
            
            # Padding für AES (PKCS7 manuell)
            padding_laenge = self.iv_laenge - (len(klartext_bytes) % self.iv_laenge)
            klartext_bytes += bytes([padding_laenge] * padding_laenge)
            
            verschluesselter_text = verschluesseler.update(klartext_bytes) + verschluesseler.finalize()
            
            # Speichere Salz, IV und verschlüsselten Text
            with open(ausgabe_datei, "wb") as datei:
                datei.write(salz + iv + verschluesselter_text)
            
            print(f"Text erfolgreich verschlüsselt und in {ausgabe_datei} gespeichert.")
            return True
        except Exception as e:
            print(f"Fehler beim Verschlüsseln: {e}")
            return False
    
    def entschluesseln(self, eingabe_datei):
        """Entschlüsselt die Datei. Gibt den Klartext zurück."""
        try:
            with open(eingabe_datei, "rb") as datei:
                daten = datei.read()
            
            salz = daten[:self.salz_laenge]
            iv = daten[self.salz_laenge:self.salz_laenge + self.iv_laenge]
            verschluesselter_text = daten[self.salz_laenge + self.iv_laenge:]
            
            schluessel = self.generiere_schluessel(salz)
            cipher = Cipher(
                algorithms.AES(schluessel),
                modes.CBC(iv),
                backend=default_backend()
            )
            entschluesseler = cipher.decryptor()
            
            klartext_bytes = entschluesseler.update(verschluesselter_text) + entschluesseler.finalize()
            
            # Entferne Padding
            padding_laenge = klartext_bytes[-1]
            klartext_bytes = klartext_bytes[:-padding_laenge]
            
            return klartext_bytes.decode()
        except Exception as e:
            print(f"Fehler beim Entschlüsseln: {e}")
            return None

def main():
    """Hauptfunktion. Verarbeitet Kommandozeilenargumente."""
    parser = argparse.ArgumentParser(description="AES-Verschlüsselungstool")
    parser.add_argument("--verschluesseln", help="Text zum Verschlüsseln")
    parser.add_argument("--ausgabe", default="verschluesselt.bin", help="Ausgabedatei für verschlüsselten Text")
    parser.add_argument("--entschluesseln", action="store_true", help="Datei entschlüsseln")
    parser.add_argument("--eingabe", default="verschluesselt.bin", help="Eingabedatei zum Entschlüsseln")
    parser.add_argument("--passwort", required=True, help="Passwort für Verschlüsselung/Entschlüsselung")
    parser.add_argument("--original", help="Originaltext zum Vergleich nach Entschlüsselung")
    
    args = parser.parse_args()
    
    verschluesselung = AESVerschluesselung(args.passwort)
    
    if args.verschluesseln:
        erfolg = verschluesselung.verschluesseln(args.verschluesseln, args.ausgabe)
        if not erfolg:
            return
    
    if args.entschluesseln:
        klartext = verschluesselung.entschluesseln(args.eingabe)
        if klartext:
            print(f"Entschlüsselter Text: {klartext}")
            if args.original:
                if klartext == args.original:
                    print("Überprüfung erfolgreich: Entschlüsselter Text stimmt mit dem Original überein.")
                else:
                    print("Überprüfung fehlgeschlagen: Entschlüsselter Text stimmt nicht mit dem Original überein.")
        else:
            print("Entschlüsselung fehlgeschlagen.")

if __name__ == "__main__":
    main()