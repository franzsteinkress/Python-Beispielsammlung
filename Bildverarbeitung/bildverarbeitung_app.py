# Copyright (c) 2025 Franz Steinkress
# Licensed under the MIT License - see LICENSE for details
#
# bildverarbeitung_app.py
# Eine Tkinter-basierte Anwendung für einfache OpenCV-Bildverarbeitung

import tkinter as tk
from tkinter import filedialog, messagebox
import cv2
import numpy as np
from PIL import Image, ImageTk
import os

class Bildverarbeitung:
    """Hauptklasse für die Bildverarbeitungsanwendung."""
    
    def __init__(self, haupt_fenster):
        """Initialisiert das Hauptfenster. Erstellt Benutzeroberfläche."""
        self.haupt_fenster = haupt_fenster
        self.haupt_fenster.title("Bildverarbeitung")
        self.haupt_fenster.iconbitmap('resources/fs.ico')
        self.bild_pfad = ""
        self.original_bild = None
        self.verarbeitetes_bild = None
        self.bild_label = None
        
        # Fenstergröße und Zentrierung
        breite = 800
        hoehe = 600
        bildschirm_breite = self.haupt_fenster.winfo_screenwidth()
        bildschirm_hoehe = self.haupt_fenster.winfo_screenheight()
        x = (bildschirm_breite - breite) // 2
        y = (bildschirm_hoehe - hoehe) // 2
        self.haupt_fenster.geometry(f"{breite}x{hoehe}+{x}+{y}")
        self.haupt_fenster.resizable(True, True)
        self.haupt_fenster.configure(bg="#2D74B2")
        
        # Menüleiste
        self.erstelle_menue()
        
        # Hauptframe
        self.haupt_frame = tk.Frame(self.haupt_fenster, bg="#2D74B2")
        self.haupt_frame.pack(expand=True, fill="both", padx=10, pady=10)
        
        # Werkzeugleiste für Filter
        self.werkzeug_leiste = tk.Frame(self.haupt_frame, bg="#2D74B2")
        self.werkzeug_leiste.pack(fill="x")
        
        tk.Button(
            self.werkzeug_leiste,
            text="Bild öffnen",
            command=self.oeffne_bild,
            font="Arial 12"
        ).pack(side=tk.LEFT, padx=5)
        
        tk.Button(
            self.werkzeug_leiste,
            text="Graustufen",
            command=self.wende_graustufen_an,
            font="Arial 12"
        ).pack(side=tk.LEFT, padx=5)
        
        tk.Button(
            self.werkzeug_leiste,
            text="Kanten",
            command=self.wende_kanten_an,
            font="Arial 12"
        ).pack(side=tk.LEFT, padx=5)
        
        tk.Button(
            self.werkzeug_leiste,
            text="Unschärfe",
            command=self.wende_unschaerfe_an,
            font="Arial 12"
        ).pack(side=tk.LEFT, padx=5)
        
        tk.Button(
            self.werkzeug_leiste,
            text="Speichern",
            command=self.speichere_bild,
            font="Arial 12"
        ).pack(side=tk.LEFT, padx=5)
        
        # Bildanzeigebereich
        self.bild_label = tk.Label(self.haupt_frame, bg="#2D74B2")
        self.bild_label.pack(expand=True, fill="both")
    
    def erstelle_menue(self):
        """Erstellt die Menüleiste. Fügt Datei- und Hilfe-Menüs hinzu."""
        menue_leiste = tk.Menu(self.haupt_fenster)
        self.haupt_fenster.config(menu=menue_leiste)
        
        # Dateimenü
        datei_menue = tk.Menu(menue_leiste, tearoff=0)
        menue_leiste.add_cascade(label="Datei", menu=datei_menue)
        datei_menue.add_command(label="Bild öffnen", command=self.oeffne_bild)
        datei_menue.add_command(label="Bild speichern", command=self.speichere_bild)
        datei_menue.add_command(label="Beenden", command=self.beende_anwendung)
        
        # Hilfemenü
        hilfe_menue = tk.Menu(menue_leiste, tearoff=0)
        menue_leiste.add_cascade(label="Hilfe", menu=hilfe_menue)
        hilfe_menue.add_command(label="Über", command=self.zeige_info)
    
    def oeffne_bild(self):
        """Öffnet ein Bild. Zeigt es im Hauptfenster an."""
        datei_pfad = filedialog.askopenfilename(
            title="Bild auswählen",
            filetypes=[("Bilddateien", "*.jpg *.jpeg *.png"), ("Alle Dateien", "*.*")]
        )
        if not datei_pfad:
            return
        
        try:
            self.bild_pfad = datei_pfad
            self.original_bild = cv2.imread(datei_pfad)
            if self.original_bild is None:
                raise ValueError("Bild konnte nicht geladen werden")
            self.verarbeitetes_bild = self.original_bild.copy()
            self.zeige_bild(self.verarbeitetes_bild)
            self.haupt_fenster.title(f"BildVerarbeitung - {os.path.basename(datei_pfad)}")
        except Exception as e:
            messagebox.showerror("Fehler", f"Fehler beim Öffnen des Bildes: {e}")
    
    def zeige_bild(self, bild):
        """Zeigt ein OpenCV-Bild im Tkinter-Label an."""
        if bild is None:
            return
        
        # Konvertiere BGR zu RGB
        bild_rgb = cv2.cvtColor(bild, cv2.COLOR_BGR2RGB)
        # Skaliere Bild für Anzeige
        hoehe, breite = bild.shape[:2]
        max_groesse = 500
        skala = min(max_groesse / breite, max_groesse / hoehe)
        neue_breite = int(breite * skala)
        neue_hoehe = int(hoehe * skala)
        bild_skaliered = cv2.resize(bild_rgb, (neue_breite, neue_hoehe), interpolation=cv2.INTER_AREA)
        
        # Konvertiere zu PIL-Bild
        pil_bild = Image.fromarray(bild_skaliered)
        tk_bild = ImageTk.PhotoImage(pil_bild)
        
        # Aktualisiere Label
        if self.bild_label is None:
            self.bild_label = tk.Label(self.haupt_frame, image=tk_bild)
            self.bild_label.pack(expand=True, fill="both")
        else:
            self.bild_label.configure(image=tk_bild)
        self.bild_label.image_ref = tk_bild
    
    def wende_graustufen_an(self):
        """Wendet Graustufenfilter auf das Bild an."""
        if self.original_bild is None:
            messagebox.showwarning("Warnung", "Kein Bild geladen!")
            messagebox.iconbitmap('resources/fs.ico')
            return
        self.verarbeitetes_bild = cv2.cvtColor(self.original_bild, cv2.COLOR_BGR2GRAY)
        # Konvertiere zurück zu RGB für Tkinter
        self.verarbeitetes_bild = cv2.cvtColor(self.verarbeitetes_bild, cv2.COLOR_GRAY2RGB)
        self.zeige_bild(self.verarbeitetes_bild)
    
    def wende_kanten_an(self):
        """Wendet Canny-Kantenfilter auf das Bild an."""
        if self.original_bild is None:
            messagebox.showwarning("Warnung", "Kein Bild geladen!")
            messagebox.iconbitmap('resources/fs.ico')
            return
        grau_bild = cv2.cvtColor(self.original_bild, cv2.COLOR_BGR2GRAY)
        self.verarbeitetes_bild = cv2.Canny(grau_bild, 100, 200)
        # Konvertiere zurück zu RGB für Tkinter
        self.verarbeitetes_bild = cv2.cvtColor(self.verarbeitetes_bild, cv2.COLOR_GRAY2RGB)
        self.zeige_bild(self.verarbeitetes_bild)
    
    def wende_unschaerfe_an(self):
        """Wendet Gaußsche Unschärfe auf das Bild an."""
        if self.original_bild is None:
            messagebox.showwarning("Warnung", "Kein Bild geladen!")
            messagebox.iconbitmap('resources/fs.ico')
            return
        self.verarbeitetes_bild = cv2.GaussianBlur(self.original_bild, (5, 5), 0)
        self.zeige_bild(self.verarbeitetes_bild)
    
    def speichere_bild(self):
        """Speichert das verarbeitete Bild."""
        if self.verarbeitetes_bild is None:
            messagebox.showwarning("Warnung", "Kein Bild zum Speichern!")
            messagebox.iconbitmap('resources/fs.ico')
            return
        
        datei_pfad = filedialog.asksaveasfilename(
            title="Bild speichern",
            defaultextension=".png",
            filetypes=[("PNG-Dateien", "*.png"), ("JPEG-Dateien", "*.jpg"), ("Alle Dateien", "*.*")]
        )
        if not datei_pfad:
            return
        
        try:
            cv2.imwrite(datei_pfad, cv2.cvtColor(self.verarbeitetes_bild, cv2.COLOR_RGB2BGR))
            messagebox.showinfo("Erfolg", f"Bild gespeichert als {os.path.basename(datei_pfad)}")
        except Exception as e:
            messagebox.showerror("Fehler", f"Fehler beim Speichern des Bildes: {e}")
    
    def zeige_info(self):
        """Zeigt Informationen über die Anwendung."""
        messagebox.showinfo("Über", "Bildverarbeitung mit OpenCV. Version 1.0. MIT-Lizenz.")
    
    def beende_anwendung(self):
        """Beendet die Anwendung."""
        self.haupt_fenster.destroy()

if __name__ == "__main__":
    # Starte die Anwendung
    haupt_fenster = tk.Tk()
    app = Bildverarbeitung(haupt_fenster)
    haupt_fenster.mainloop()