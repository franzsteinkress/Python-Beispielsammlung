# Copyright (c) 2025 Franz Steinkress
# Licensed under the MIT License - see LICENSE for details
#
# blockchain_app.py
# Eine Ethereum-Blockchain-Demo mit Tkinter-Bedienoberfläche

import tkinter as tk
from tkinter import messagebox
import os
from web3 import Web3
import requests

class EthereumDemo:
    """Hauptklasse für die Ethereum-Demo-Anwendung."""
    
    def __init__(self, haupt_fenster):
        """Initialisiert die GUI. Verbindet zur Blockchain."""
        self.haupt_fenster = haupt_fenster
        self.haupt_fenster.title("Ethereum Blockchain Demo")
        self.haupt_fenster.iconbitmap('resources/fs.ico')
        self.ganache_url = "http://127.0.0.1:7545"
        self.blockchain_verbindung = None
        self.konten = []
        
        # Fenstergröße und Zentrierung
        breite = 600
        hoehe = 400
        bildschirm_breite = self.haupt_fenster.winfo_screenwidth()
        bildschirm_hoehe = self.haupt_fenster.winfo_screenheight()
        x = (bildschirm_breite - breite) // 2
        y = (bildschirm_hoehe - hoehe) // 2
        self.haupt_fenster.geometry(f"{breite}x{hoehe}+{x}+{y}")
        
        # Verbinde zur Blockchain
        self.verbindungsaufbau()
        
        # Erstelle GUI
        self.erstelle_oberflaeche()
    
    def verbindungsaufbau(self):
        """Verbindet zur Ganache-Blockchain. Lädt Konten."""
        try:
            self.blockchain_verbindung = Web3(Web3.HTTPProvider(self.ganache_url))
            if not self.blockchain_verbindung.is_connected():
                raise Exception("Verbindung zur Blockchain fehlgeschlagen.")
            self.konten = self.blockchain_verbindung.eth.accounts
            print("Verbunden zur Blockchain. Konten geladen.")
        except Exception as e:
            messagebox.showerror("Fehler", f"Verbindung fehlgeschlagen: {e}")
            self.haupt_fenster.quit()
    
    def hole_kontostand(self, adresse):
        """Holt den Kontostand einer Adresse in Ether."""
        try:
            saldo = self.blockchain_verbindung.eth.get_balance(adresse)
            return self.blockchain_verbindung.from_wei(saldo, "ether")
        except Exception as e:
            messagebox.showerror("Fehler", f"Fehler beim Abrufen des Kontostands: {e}")
            return None
    
    def sende_transaktion(self, sender_adresse, empfaenger_adresse, betrag_ether, private_key):
        """Sendet eine Transaktion von Sender zu Empfänger."""
        try:
            if not self.blockchain_verbindung.is_address(empfaenger_adresse):
                raise ValueError("Ungültige Empfängeradresse.")
            betrag_wei = self.blockchain_verbindung.to_wei(betrag_ether, "ether")

            transaktion = {
                "from": sender_adresse,
                "to": empfaenger_adresse,
                "value": betrag_wei,
                "gas": 21000,
                "gasPrice": self.blockchain_verbindung.eth.gas_price,
                "nonce": self.blockchain_verbindung.eth.get_transaction_count(sender_adresse)
            }

            signierte_transaktion = self.blockchain_verbindung.eth.account.sign_transaction(
                transaktion, private_key=private_key
            )

            tx_hash = self.blockchain_verbindung.eth.send_raw_transaction(
                signierte_transaktion.raw_transaction
            )
            tx_beleg = self.blockchain_verbindung.eth.wait_for_transaction_receipt(tx_hash)
            return tx_beleg["transactionHash"].hex()
        except Exception as e:
            messagebox.showerror("Fehler", f"Transaktion fehlgeschlagen: {e}")
            return None
    
    def hole_privaten_schluessel(self, adresse):
        """Holt den privaten Schlüssel für eine Adresse von Ganache."""
        try:
            response = requests.post(self.ganache_url, json={
                "method": "eth_getAccountPrivateKey",
                "params": [adresse],
                "id": 1,
                "jsonrpc": "2.0"
            })
            print(response.text)
            result = response.json()
            if "result" in result:
                return result["result"]
            raise Exception("Privater Schlüssel nicht gefunden.")
        except Exception as e:
            raise Exception(f"Fehler beim Abrufen des privaten Schlüssels: {e}")
    
    def erstelle_oberflaeche(self):
        """Erstellt die Tkinter-Bedienoberfläche."""
        haupt_frame = tk.Frame(self.haupt_fenster, padx=10, pady=10)
        haupt_frame.grid(row=0, column=0, sticky="nsew")
        self.haupt_fenster.grid_rowconfigure(0, weight=1)
        self.haupt_fenster.grid_columnconfigure(0, weight=1)
        haupt_frame.configure(bg="#403D3A")

        # Kontoauswahl
        tk.Label(haupt_frame, text="Sender-Konto:", bg="#403D3A", fg="white", font="Arial 12").grid(row=0, column=0, sticky="e", pady=5)
        self.konto_auswahl = tk.StringVar(self.haupt_fenster)
        if self.konten:
            self.konto_auswahl.set(self.konten[0])
        tk.OptionMenu(haupt_frame, self.konto_auswahl, *self.konten).grid(row=0, column=1, sticky="w", pady=5)
        
        # Kontostand abrufen
        tk.Button(
            haupt_frame,
            text="Kontostand abrufen",
            command=self.zeige_kontostand,
            bg="#F2AF67",
            font="Arial 12"
        ).grid(row=1, column=1, sticky="w", pady=10)
        
        # Kontostand-Anzeige
        self.kontostand_label = tk.Label(haupt_frame, text="Kontostand: -", bg="#403D3A", fg="white", font="Arial 12 bold")
        self.kontostand_label.grid(row=2, column=1, sticky="w", pady=10)
        
        # Empfängeradresse
        tk.Label(haupt_frame, text="Empfängeradresse:", bg="#403D3A", fg="white", font="Arial 12").grid(row=3, column=0, sticky="e", pady=5)
        self.empfaenger_eingabe = tk.Entry(haupt_frame, font="Arial 12", width=45)
        self.empfaenger_eingabe.grid(row=3, column=1, sticky="w", pady=5)
        
        # Betrag
        tk.Label(haupt_frame, text="Betrag (Ether):", bg="#403D3A", fg="white", font="Arial 12").grid(row=4, column=0, sticky="e", pady=5)
        self.betrag_eingabe = tk.Entry(haupt_frame, font="Arial 12")
        self.betrag_eingabe.grid(row=4, column=1, sticky="w", pady=5)
        
        # Privater Schlüssel
        tk.Label(haupt_frame, text="Privater Schlüssel:", bg="#403D3A", fg="white", font="Arial 12").grid(row=5, column=0, sticky="e", pady=5)
        self.private_key_eingabe = tk.Entry(haupt_frame, font="Arial 12", show="*", width=45)
        self.private_key_eingabe.grid(row=5, column=1, sticky="w", pady=5)
        
        # Transaktion senden
        tk.Button(
            haupt_frame,
            text="Transaktion senden",
            command=self.sende_transaktion_gui,
            bg="#F2AF67",
            font="Arial 12"
        ).grid(row=6, column=1, sticky="w", pady=10)
        
        # Transaktionsergebnis
        self.transaktions_label = tk.Label(haupt_frame, text="Transaktionsstatus: -", bg="#403D3A", fg="white", font="Arial 12 bold", wraplength=0)
        self.transaktions_label.grid(row=7, column=1, sticky="w", pady=10)
    
    def zeige_kontostand(self):
        """Zeigt den Kontostand des ausgewählten Kontos an."""
        adresse = self.konto_auswahl.get()
        saldo = self.hole_kontostand(adresse)
        if saldo is not None:
            self.kontostand_label.config(text=f"Kontostand: {saldo:.4f} ETH")
    
    def sende_transaktion_gui(self):
        """Sendet eine Transaktion basierend auf Benutzereingaben."""
        sender_adresse = self.konto_auswahl.get()
        empfaenger_adresse = self.empfaenger_eingabe.get()
        private_key = self.private_key_eingabe.get()
        try:
            betrag_ether = float(self.betrag_eingabe.get())
            if betrag_ether <= 0:
                raise ValueError("Betrag muss positiv sein.")
            if not all([empfaenger_adresse, self.betrag_eingabe.get(), private_key]):
                raise ValueError("Alle Felder (Empfängeradresse, Betrag, privater Schlüssel) müssen ausgefüllt sein!")
            tx_hash = self.sende_transaktion(sender_adresse, empfaenger_adresse, betrag_ether, private_key)
            if tx_hash:
                self.transaktions_label.config(text=f"Transaktionsstatus: Erfolgreich (Hash: {tx_hash})")
        except ValueError as e:
            messagebox.showerror("Fehler", f"Ungültige Eingabe: {e}")
        except Exception as e:
            messagebox.showerror("Fehler", f"Transaktion fehlgeschlagen: {e}")

def main():
    """Hauptfunktion. Startet die Tkinter-Anwendung."""
    haupt_fenster = tk.Tk()
    app = EthereumDemo(haupt_fenster)
    haupt_fenster.mainloop()

if __name__ == "__main__":
    main()