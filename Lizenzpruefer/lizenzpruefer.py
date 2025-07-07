# Copyright (c) 2025 Franz Steinkress
# Licensed under the MIT License - see LICENSE for details
#
# lizenzpruefer.py
# Ein Lizenzprüfungssystem mit RSA-Signaturen zur Validierung von Lizenzdateien

import json
import os
import argparse
import base64
from datetime import datetime
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.backends import default_backend
from cryptography.exceptions import InvalidSignature

class Lizenzpruefer:
    """Hauptklasse für die Lizenzprüfung und -generierung."""
    
    def __init__(self):
        """Initialisiert den Lizenzprüfer. Setzt Standardpfade für Schlüssel."""
        self.privater_schluessel_pfad = "config/keys/privater_schluessel.pem"
        self.oeffentlicher_schluessel_pfad = "config/keys/oeffentlicher_schluessel.pem"
    
    def generiere_schluesselpaar(self):
        """Generiert ein RSA-Schlüsselpaar. Speichert in Dateien."""
        privater_schluessel = rsa.generate_private_key(
            public_exponent=65537,
            key_size=2048,
            backend=default_backend()
        )
        oeffentlicher_schluessel = privater_schluessel.public_key()
        
        # Speichere privaten Schlüssel
        with open(self.privater_schluessel_pfad, "wb") as datei:
            datei.write(
                privater_schluessel.private_bytes(
                    encoding=serialization.Encoding.PEM,
                    format=serialization.PrivateFormat.PKCS8,
                    encryption_algorithm=serialization.NoEncryption()
                )
            )
        
        # Speichere öffentlichen Schlüssel
        with open(self.oeffentlicher_schluessel_pfad, "wb") as datei:
            datei.write(
                oeffentlicher_schluessel.public_bytes(
                    encoding=serialization.Encoding.PEM,
                    format=serialization.PublicFormat.SubjectPublicKeyInfo
                )
            )
        print(f"Schlüsselpaar generiert: {self.privater_schluessel_pfad}, {self.oeffentlicher_schluessel_pfad}")
    
    def lade_privaten_schluessel(self):
        """Lädt den privaten Schlüssel aus der Datei."""
        try:
            with open(self.privater_schluessel_pfad, "rb") as datei:
                return serialization.load_pem_private_key(
                    datei.read(),
                    password=None,
                    backend=default_backend()
                )
        except Exception as e:
            print(f"Fehler beim Laden des privaten Schlüssels: {e}")
            return None
    
    def lade_oeffentlichen_schluessel(self):
        """Lädt den öffentlichen Schlüssel aus der Datei."""
        try:
            with open(self.oeffentlicher_schluessel_pfad, "rb") as datei:
                return serialization.load_pem_public_key(
                    datei.read(),
                    backend=default_backend()
                )
        except Exception as e:
            print(f"Fehler beim Laden des öffentlichen Schlüssels: {e}")
            return None
    
    def erstelle_lizenz(self, lizenznehmer, ablaufdatum, produkt_id, lizenz_datei):
        """Erstellt eine Lizenzdatei mit Signatur."""
        privater_schluessel = self.lade_privaten_schluessel()
        if not privater_schluessel:
            return False
        
        lizenz_daten = {
            "lizenznehmer": lizenznehmer,
            "ablaufdatum": ablaufdatum,
            "produkt_id": produkt_id
        }
        lizenz_json = json.dumps(lizenz_daten, sort_keys=True).encode()
        
        # Erstelle Signatur
        try:
            signatur = privater_schluessel.sign(
                lizenz_json,
                padding.PSS(
                    mgf=padding.MGF1(hashes.SHA256()),
                    salt_length=padding.PSS.MAX_LENGTH
                ),
                hashes.SHA256()
            )
            lizenz_daten["signatur"] = base64.b64encode(signatur).decode()
            
            with open(lizenz_datei, "w") as datei:
                json.dump(lizenz_daten, datei, indent=4)
            
            print(f"Lizenzdatei erstellt: {lizenz_datei}")
            return True
        except Exception as e:
            print(f"Fehler beim Erstellen der Lizenz: {e}")
            return False
    
    def pruefe_lizenz(self, lizenz_datei):
        """Prüft die Gültigkeit einer Lizenzdatei."""
        oeffentlicher_schluessel = self.lade_oeffentlichen_schluessel()
        if not oeffentlicher_schluessel:
            return False
        
        try:
            with open(lizenz_datei, "r") as datei:
                lizenz_daten = json.load(datei)
            
            lizenznehmer = lizenz_daten.get("lizenznehmer")
            ablaufdatum = lizenz_daten.get("ablaufdatum")
            produkt_id = lizenz_daten.get("produkt_id")
            signatur = base64.b64decode(lizenz_daten.get("signatur"))
            
            # Überprüfe Ablaufdatum
            aktuelles_datum = datetime.now().strftime("%Y-%m-%d")
            if ablaufdatum < aktuelles_datum:
                print(f"Lizenz abgelaufen: {ablaufdatum}")
                return False
            
            # Überprüfe Signatur
            lizenz_json = json.dumps(
                {
                    "lizenznehmer": lizenznehmer,
                    "ablaufdatum": ablaufdatum,
                    "produkt_id": produkt_id
                },
                sort_keys=True
            ).encode()
            
            oeffentlicher_schluessel.verify(
                signatur,
                lizenz_json,
                padding.PSS(
                    mgf=padding.MGF1(hashes.SHA256()),
                    salt_length=padding.PSS.MAX_LENGTH
                ),
                hashes.SHA256()
            )
            
            print(f"Lizenz gültig für {lizenznehmer}, Produkt-ID: {produkt_id}, Ablaufdatum: {ablaufdatum}")
            return True
        except InvalidSignature:
            print("Ungültige Signatur.")
            return False
        except Exception as e:
            print(f"Fehler beim Prüfen der Lizenz: {e}")
            return False

def main():
    """Hauptfunktion. Verarbeitet Kommandozeilenargumente."""
    parser = argparse.ArgumentParser(description="Lizenzprüfungssystem")
    parser.add_argument("--generiere-schluessel", action="store_true", help="Generiert ein neues Schlüsselpaar")
    parser.add_argument("--erstelle-lizenz", action="store_true", help="Erstellt eine neue Lizenzdatei")
    parser.add_argument("--lizenznehmer", help="Name des Lizenznehmers")
    parser.add_argument("--ablaufdatum", help="Ablaufdatum der Lizenz (YYYY-MM-DD)")
    parser.add_argument("--produkt-id", help="Produkt-ID")
    parser.add_argument("--lizenz-datei", default="lizenz.json", help="Pfad zur Lizenzdatei")
    parser.add_argument("--pruefe-lizenz", action="store_true", help="Prüft eine Lizenzdatei")
    
    args = parser.parse_args()
    
    pruefer = Lizenzpruefer()
    
    if args.generiere_schluessel:
        pruefer.generiere_schluesselpaar()
    
    if args.erstelle_lizenz:
        if not all([args.lizenznehmer, args.ablaufdatum, args.produkt_id]):
            print("Fehler: Lizenznehmer, Ablaufdatum und Produkt-ID sind erforderlich.")
            return
        pruefer.erstelle_lizenz(args.lizenznehmer, args.ablaufdatum, args.produkt_id, args.lizenz_datei)
    
    if args.pruefe_lizenz:
        pruefer.pruefe_lizenz(args.lizenz_datei)

if __name__ == "__main__":
    main()