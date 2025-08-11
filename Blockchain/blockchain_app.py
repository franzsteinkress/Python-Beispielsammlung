# Copyright (c) 2025 Franz Steinkress
# Licensed under the MIT License - see LICENSE for details
#
# blockchain_app.py
# Eine Ethereum-Blockchain-Demo mit Tkinter-Bedienoberfläche

import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from ttkthemes import ThemedTk
from web3 import Web3
import requests

class EthereumDemo:
    def __init__(self, haupt_fenster):
        self.haupt_fenster = haupt_fenster
        self.haupt_fenster.title("Ethereum Blockchain Demo")
        self.haupt_fenster.iconbitmap('resources/fs.ico')
        self.ganache_url = "http://127.0.0.1:7545"
        self.blockchain_verbindung = None
        self.konten = []
        
        # Fenstergröße und Zentrierung
        breite, hoehe = 600, 400
        x = (self.haupt_fenster.winfo_screenwidth() - breite) // 2
        y = (self.haupt_fenster.winfo_screenheight() - hoehe) // 2
        self.haupt_fenster.geometry(f"{breite}x{hoehe}+{x}+{y}")
        
        self.verbindungsaufbau()
        self.erstelle_styles()
        self.erstelle_oberflaeche()
    
    def verbindungsaufbau(self):
        try:
            self.blockchain_verbindung = Web3(Web3.HTTPProvider(self.ganache_url))
            if not self.blockchain_verbindung.is_connected():
                raise Exception("Verbindung zur Blockchain fehlgeschlagen.")
            self.konten = self.blockchain_verbindung.eth.accounts
            print("Verbunden zur Blockchain. Konten geladen.")
        except Exception as e:
            messagebox.showerror("Fehler", f"Verbindung fehlgeschlagen: {e}")
            self.haupt_fenster.quit()
    
    def erstelle_styles(self):
        style = ttk.Style(self.haupt_fenster)

        # Basis-Buttonfarbe
        style.configure(
            "Custom.TButton",
            font=("Arial", 12),
            background="#F2AF67",
            foreground="black",
            borderwidth=1
        )

        # Hover und Fokus
        style.map(
            "Custom.TButton",
            background=[
                ("active", "#E89C50"),   # Hover
                ("focus", "#E89C50"),    # Fokus
                ("pressed", "#D4863E")   # Klick
            ]
        )

        # Label-Design
        style.configure(
            "Custom.TLabel",
            background="#403D3A",
            foreground="white",
            font=("Arial", 12)
        )

    def hole_kontostand(self, adresse):
        try:
            saldo = self.blockchain_verbindung.eth.get_balance(adresse)
            return self.blockchain_verbindung.from_wei(saldo, "ether")
        except Exception as e:
            messagebox.showerror("Fehler", f"Fehler beim Abrufen des Kontostands: {e}")
            return None
    
    def sende_transaktion(self, sender_adresse, empfaenger_adresse, betrag_ether, private_key):
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
    
    def erstelle_oberflaeche(self):
        haupt_frame = tk.Frame(self.haupt_fenster, padx=10, pady=10, bg="#403D3A")
        haupt_frame.grid(row=0, column=0, sticky="nsew")
        self.haupt_fenster.grid_rowconfigure(0, weight=1)
        self.haupt_fenster.grid_columnconfigure(0, weight=1)

        # Sender-Konto
        ttk.Label(haupt_frame, text="Sender-Konto:", style="Custom.TLabel").grid(row=0, column=0, sticky="e", pady=5)
        self.konto_auswahl = tk.StringVar(self.haupt_fenster)
        if self.konten:
            self.konto_auswahl.set(self.konten[0])
        ttk.OptionMenu(haupt_frame, self.konto_auswahl, self.konten[0], *self.konten).grid(row=0, column=1, sticky="w", pady=5)

        # Kontostand abrufen
        ttk.Button(haupt_frame, text="Kontostand abrufen", style="Custom.TButton", command=self.zeige_kontostand).grid(row=1, column=1, sticky="w", pady=10)
        
        ttk.Label(haupt_frame, text="Kontostand:", style="Custom.TLabel", font=("Arial", 12, "bold")).grid(row=2, column=0, sticky="e", pady=5)
        self.kontostand_label = ttk.Label(haupt_frame, style="Custom.TLabel")
        self.kontostand_label.grid(row=2, column=1, sticky="w", pady=10)

        # Empfängeradresse
        ttk.Label(haupt_frame, text="Empfängeradresse:", style="Custom.TLabel").grid(row=3, column=0, sticky="e", pady=5)
        self.empfaenger_eingabe = ttk.Entry(haupt_frame, width=60)
        self.empfaenger_eingabe.grid(row=3, column=1, sticky="w", pady=5)
        
        # Betrag
        ttk.Label(haupt_frame, text="Betrag (Ether):", style="Custom.TLabel").grid(row=4, column=0, sticky="e", pady=5)
        self.betrag_eingabe = ttk.Entry(haupt_frame)
        self.betrag_eingabe.grid(row=4, column=1, sticky="w", pady=5)
        
        # Privater Schlüssel
        ttk.Label(haupt_frame, text="Privater Schlüssel:", style="Custom.TLabel").grid(row=5, column=0, sticky="e", pady=5)
        self.private_key_eingabe = ttk.Entry(haupt_frame, show="*", width=60)
        self.private_key_eingabe.grid(row=5, column=1, sticky="w", pady=5)
        
        # Transaktion senden
        ttk.Button(haupt_frame, text="Transaktion senden", style="Custom.TButton", command=self.sende_transaktion_gui).grid(row=6, column=1, sticky="w", pady=10)

        ttk.Label(haupt_frame, text="Transaktionsstatus:", style="Custom.TLabel", font=("Arial", 12)).grid(row=7, column=0, sticky="w", pady=10)
        self.transaktions_label = ttk.Label(haupt_frame, style="Custom.TLabel", font=("Arial", 10))
        self.transaktions_label.grid(row=7, column=1, sticky="w", pady=10)
    
    def zeige_kontostand(self):
        adresse = self.konto_auswahl.get()
        saldo = self.hole_kontostand(adresse)
        if saldo is not None:
            self.kontostand_label.config(text=f"{saldo:.4f} ETH")
    
    def sende_transaktion_gui(self):
        sender_adresse = self.konto_auswahl.get()
        empfaenger_adresse = self.empfaenger_eingabe.get()
        private_key = self.private_key_eingabe.get()
        try:
            betrag_ether = float(self.betrag_eingabe.get())
            if betrag_ether <= 0:
                raise ValueError("Betrag muss positiv sein.")
            if not all([empfaenger_adresse, self.betrag_eingabe.get(), private_key]):
                raise ValueError("Alle Felder müssen ausgefüllt sein!")
            tx_hash = self.sende_transaktion(sender_adresse, empfaenger_adresse, betrag_ether, private_key)
            if tx_hash:
                self.transaktions_label.config(text=f"{tx_hash}")
        except ValueError as e:
            messagebox.showerror("Fehler", f"Ungültige Eingabe: {e}")
        except Exception as e:
            messagebox.showerror("Fehler", f"Transaktion fehlgeschlagen: {e}")

def main():
    haupt_fenster = ThemedTk(theme="radiance")  # Nur Windows
    app = EthereumDemo(haupt_fenster)
    haupt_fenster.mainloop()

if __name__ == "__main__":
    main()
