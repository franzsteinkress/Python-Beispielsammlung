# Copyright (c) 2025 Franz Steinkress
# Licensed under the MIT License - see LICENSE for details
#
# funktionswerkzeug_app.py
# Eine Tkinter-basierte Funktionswerkzeug-Anwendung mit verschiedenen Werkzeugen

import tkinter as tk
from tkinter import messagebox, ttk
import random
import os
import colorama
from colorama import Fore, Back, Style
import pyqrcode
from PIL import Image, ImageTk
import hashlib
import time

colorama.init(autoreset=True)

class Funktionswerkzeug:
    """Hauptklasse für die Funktionswerkzeug-Anwendung."""
    
    def __init__(self, haupt_fenster):
        """Initialisiert das Hauptfenster. Erstellt Werkzeug-Buttons."""
        self.haupt_fenster = haupt_fenster
        self.haupt_fenster.title("Funktionswerkzeug")
        self.haupt_fenster.iconbitmap('static/icons/fs.ico')

        # Fenstergröße und Zentrierung
        breite = 500
        hoehe = 300
        bildschirm_breite = self.haupt_fenster.winfo_screenwidth()
        bildschirm_hoehe = self.haupt_fenster.winfo_screenheight()
        x = (bildschirm_breite - breite) // 2
        y = (bildschirm_hoehe - hoehe) // 2
        self.haupt_fenster.geometry(f"{breite}x{hoehe}+{x}+{y}")
        self.haupt_fenster.resizable(False, False)
        
        # Hauptframe für Buttons
        haupt_frame = tk.Frame(self.haupt_fenster, padx=10, pady=10)
        haupt_frame.pack(expand=True, fill="both")
        
        # Werkzeug-Buttons
        werkzeuge = [
            {"text": "Akronym-Generator", "command": self.start_akronym},
            {"text": "BMI-Rechner", "command": self.start_bmi},
            {"text": "Farbiger Text", "command": self.start_farbiger_text},
            {"text": "Würfel-Simulator", "command": self.start_wuerfel},
            {"text": "Fahrenheit zu Celsius", "command": self.start_fahrenheit},
            {"text": "Passwort-Generator", "command": self.start_passwort},
            {"text": "QR-Code-Generator", "command": self.start_qrcode},
            {"text": "Römische Zahlen", "command": self.start_roman}
        ]
        
        for i, werkzeug in enumerate(werkzeuge):
            tk.Button(
                haupt_frame,
                text=werkzeug["text"],
                command=werkzeug["command"],
                font="Arial 12",
                width=20
            ).grid(row=i//2, column=i%2, padx=10, pady=10)
        
        # Info-Button
        tk.Button(
            haupt_frame,
            text="Über",
            command=self.zeige_info,
            font="Arial 12",
            width=20
        ).grid(row=len(werkzeuge)//2, column=0, columnspan=2, pady=10)
    
    def zeige_info(self):
        """Zeigt Informationen über die Anwendung."""
        messagebox.showinfo("Über", "Funktionswerkzeug. Version 1.0. MIT-Lizenz.")
    
    def start_akronym(self):
        """Startet das Akronym-Werkzeug."""
        fenster = tk.Toplevel(self.haupt_fenster)
        fenster.title("Akronym-Generator")
        fenster.geometry("400x200")
        fenster.resizable(False, False)
        fenster.iconbitmap('static/icons/fs.ico')

        tk.Label(fenster, text="Phrase eingeben:", font="Arial 12").pack(pady=10)
        eingabe_text = tk.Entry(fenster, width=30, font="Arial 12")
        eingabe_text.pack(pady=5)
        
        ergebnis_label = tk.Label(fenster, text="", font="Arial 12", wraplength=350)
        ergebnis_label.pack(pady=10)
        
        def generiere_akronym():
            phrase = eingabe_text.get().strip()
            if not phrase:
                ergebnis_label.config(text="Bitte eine Phrase eingeben!")
                return
            woerter = phrase.split()
            akronym = "".join(wort[0].upper() for wort in woerter if wort)
            ergebnis_label.config(text=f"Akronym: {akronym}")
        
        tk.Button(fenster, text="Generieren", command=generiere_akronym, font="Arial 12").pack(pady=5)
    
    def start_bmi(self):
        """Startet das BMI-Werkzeug."""
        fenster = tk.Toplevel(self.haupt_fenster)
        fenster.title("BMI-Rechner")
        fenster.geometry("400x300")
        fenster.resizable(False, False)
        fenster.iconbitmap('static/icons/fs.ico')
        
        tk.Label(fenster, text="Größe (cm):", font="Arial 12").pack(pady=5)
        groesse_eingabe = tk.Entry(fenster, width=10, font="Arial 12")
        groesse_eingabe.pack(pady=5)
        
        tk.Label(fenster, text="Gewicht (kg):", font="Arial 12").pack(pady=5)
        gewicht_eingabe = tk.Entry(fenster, width=10, font="Arial 12")
        gewicht_eingabe.pack(pady=5)
        
        ergebnis_label = tk.Label(fenster, text="", font="Arial 12", wraplength=350)
        ergebnis_label.pack(pady=10)
        
        def berechne_bmi():
            try:
                groesse = float(groesse_eingabe.get())
                gewicht = float(gewicht_eingabe.get())
                if groesse <= 0 or gewicht <= 0:
                    ergebnis_label.config(text="Bitte gültige Werte eingeben!")
                    return
                groesse_m = groesse / 100
                bmi = gewicht / (groesse_m * groesse_m)
                kategorie = ""
                if bmi <= 16:
                    kategorie = "starkes Untergewicht"
                elif bmi <= 18.5:
                    kategorie = "Untergewicht"
                elif bmi <= 25:
                    kategorie = "gesund"
                elif bmi <= 30:
                    kategorie = "Übergewicht"
                else:
                    kategorie = "starkes Übergewicht"
                ergebnis_label.config(text=f"BMI: {bmi:.2f}. Kategorie: {kategorie}")
            except ValueError:
                ergebnis_label.config(text="Bitte Zahlen eingeben!")
        
        tk.Button(fenster, text="Berechnen", command=berechne_bmi, font="Arial 12").pack(pady=5)
    
    def start_farbiger_text(self):
        """Startet das Werkzeug für farbigen Text."""
        fenster = tk.Toplevel(self.haupt_fenster)
        fenster.title("Farbiger Text")
        fenster.geometry("400x200")
        fenster.resizable(False, False)
        fenster.iconbitmap('static/icons/fs.ico')
        
        text_bereich = tk.Text(fenster, height=5, width=50, font="Arial 12")
        text_bereich.pack(pady=10)
        
        def zeige_farbigen_text():
            text_bereich.delete(1.0, tk.END)
            text_bereich.insert(tk.END, "Hallo, ich bin dein Werkzeug!\n", "blau_gelb")
            text_bereich.insert(tk.END, "Ich bin dein Lehrer!\n", "gelb_blau")
            text_bereich.insert(tk.END, "Farbiger Text!", "rot_gruen")
            text_bereich.tag_config("blau_gelb", foreground="blue", background="yellow")
            text_bereich.tag_config("gelb_blau", foreground="yellow", background="blue")
            text_bereich.tag_config("rot_gruen", foreground="red", background="green")
        
        tk.Button(fenster, text="Text anzeigen", command=zeige_farbigen_text, font="Arial 12").pack(pady=5)
    
    def start_wuerfel(self):
        """Startet den Würfel-Simulator."""
        fenster = tk.Toplevel(self.haupt_fenster)
        fenster.title("Würfel-Simulator")
        fenster.geometry("400x200")
        fenster.resizable(False, False)
        fenster.iconbitmap('static/icons/fs.ico')
        
        ergebnis_label = tk.Label(fenster, text="Würfel bereit!", font="Arial 12", wraplength=350)
        ergebnis_label.pack(pady=10)
        
        def wuerfeln():
            min_wert = 1
            max_wert = 6
            wuerfel1 = random.randint(min_wert, max_wert)
            wuerfel2 = random.randint(min_wert, max_wert)
            ergebnis_label.config(text=f"Würfel 1: {wuerfel1}. Würfel 2: {wuerfel2}")
        
        tk.Button(fenster, text="Würfeln", command=wuerfeln, font="Arial 12").pack(pady=5)
        tk.Button(fenster, text="Schließen", command=fenster.destroy, font="Arial 12").pack(pady=5)
    
    def start_fahrenheit(self):
        """Startet das Fahrenheit-zu-Celsius-Werkzeug."""
        fenster = tk.Toplevel(self.haupt_fenster)
        fenster.title("Fahrenheit zu Celsius")
        fenster.geometry("400x200")
        fenster.resizable(False, False)
        fenster.iconbitmap('static/icons/fs.ico')
        
        tk.Label(fenster, text="Fahrenheit:", font="Arial 12").pack(pady=5)
        fahrenheit_eingabe = tk.Entry(fenster, width=10, font="Arial 12")
        fahrenheit_eingabe.pack(pady=5)
        
        ergebnis_label = tk.Label(fenster, text="", font="Arial 12", wraplength=350)
        ergebnis_label.pack(pady=10)
        
        def konvertiere():
            try:
                fahrenheit = float(fahrenheit_eingabe.get())
                celsius = (fahrenheit - 32) * 5 / 9
                ergebnis_label.config(text=f"{fahrenheit}°F = {celsius:.2f}°C")
            except ValueError:
                ergebnis_label.config(text="Bitte eine Zahl eingeben!")
        
        tk.Button(fenster, text="Konvertieren", command=konvertiere, font="Arial 12").pack(pady=5)
    
    def start_passwort(self):
        """Startet das Passwort-Generator-Werkzeug."""
        fenster = tk.Toplevel(self.haupt_fenster)
        fenster.title("Passwort-Generator")
        fenster.geometry("400x200")
        fenster.resizable(False, False)
        fenster.iconbitmap('static/icons/fs.ico')
        
        tk.Label(fenster, text="Passwortlänge:", font="Arial 12").pack(pady=5)
        laenge_eingabe = tk.Entry(fenster, width=10, font="Arial 12")
        laenge_eingabe.pack(pady=5)
        
        ergebnis_label = tk.Label(fenster, text="", font="Arial 12", wraplength=350)
        ergebnis_label.pack(pady=10)
        
        def generiere_passwort():
            try:
                laenge = int(laenge_eingabe.get())
                if laenge <= 0:
                    ergebnis_label.config(text="Bitte eine positive Zahl eingeben!")
                    return
                zeichen = "abcdefghijklmnopqrstuvwxyz01234567890ABCDEFGHIJKLMNOPQRSTUVWXYZ!@#$%^&*()?"
                passwort = "".join(random.sample(zeichen, laenge))
                ergebnis_label.config(text=f"Passwort: {passwort}")
            except ValueError:
                ergebnis_label.config(text="Bitte eine Zahl eingeben!")
        
        tk.Button(fenster, text="Generieren", command=generiere_passwort, font="Arial 12").pack(pady=5)
    
    def start_qrcode(self):
        """Startet das QR-Code-Werkzeug."""
        fenster = tk.Toplevel(self.haupt_fenster)
        fenster.title("QR-Code-Generator")
        fenster.geometry("400x300")
        fenster.resizable(False, False)
        fenster.iconbitmap('static/icons/fs.ico')
        
        tk.Label(fenster, text="URL eingeben:", font="Arial 12").pack(pady=5)
        url_eingabe = tk.Entry(fenster, width=30, font="Arial 12")
        url_eingabe.pack(pady=5)
        
        ergebnis_label = tk.Label(fenster, text="", font="Arial 12", wraplength=350)
        ergebnis_label.pack(pady=10)
        
        def generiere_qrcode():
            url = url_eingabe.get().strip()
            if not url:
                ergebnis_label.config(text="Bitte eine URL eingeben!")
                return
            qr = pyqrcode.create(url)
            qr_datei = f"static/qr_codes/qr_{hashlib.md5(url.encode()).hexdigest()}.png"
            os.makedirs("static/qr_codes", exist_ok=True)
            qr.png(qr_datei, scale=8)
            ergebnis_label.config(text=f"QR-Code gespeichert: {qr_datei}")
            try:
                bild = Image.open(qr_datei)
                bild = bild.resize((100, 100), Image.Resampling.LANCZOS)
                foto = ImageTk.PhotoImage(bild)
                bild_label = tk.Label(fenster, image=foto)
                bild_label.image_ref = foto
                bild_label.pack(pady=5)
            except Exception:
                ergebnis_label.config(text=f"QR-Code gespeichert, aber Anzeige fehlgeschlagen!")
        
        tk.Button(fenster, text="Generieren", command=generiere_qrcode, font="Arial 12").pack(pady=5)
    
    def start_roman(self):
        """Startet das Werkzeug für römische Zahlen."""
        fenster = tk.Toplevel(self.haupt_fenster)
        fenster.title("Römische Zahlen")
        fenster.geometry("400x200")
        fenster.resizable(False, False)
        fenster.iconbitmap('static/icons/fs.ico')
        
        tk.Label(fenster, text="Römische Zahl eingeben:", font="Arial 12").pack(pady=5)
        roman_eingabe = tk.Entry(fenster, width=10, font="Arial 12")
        roman_eingabe.pack(pady=5)
        
        ergebnis_label = tk.Label(fenster, text="", font="Arial 12", wraplength=350)
        ergebnis_label.pack(pady=10)
        
        def konvertiere_roman():
            roemisch = roman_eingabe.get().strip().upper()
            if not roemisch or not all(c in "IVXLCDM" for c in roemisch):
                ergebnis_label.config(text="Bitte eine gültige römische Zahl eingeben!")
                return
            umrechnung = {
                "I": 1, "V": 5, "X": 10, "L": 50, "C": 100, "D": 500, "M": 1000
            }
            summe = 0
            for i in range(len(roemisch) - 1):
                links = roemisch[i]
                rechts = roemisch[i + 1]
                if umrechnung[links] < umrechnung[rechts]:
                    summe -= umrechnung[links]
                else:
                    summe += umrechnung[links]
            summe += umrechnung[roemisch[-1]]
            ergebnis_label.config(text=f"Dezimal: {summe}")
        
        tk.Button(fenster, text="Konvertieren", command=konvertiere_roman, font="Arial 12").pack(pady=5)

if __name__ == "__main__":
    # Starte die Anwendung
    haupt_fenster = tk.Tk()
    app = Funktionswerkzeug(haupt_fenster)
    haupt_fenster.mainloop()