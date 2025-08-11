# Copyright (c) 2025 Franz Steinkress
# Licensed under the MIT License - see LICENSE for details
#
# bildverarbeitung_app.py
# Eine Tkinter-basierte Anwendung für einfache OpenCV-Bildverarbeitung

import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter import ttk
from ttkthemes import ThemedTk
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
        self.haupt_fenster.configure(bg="#2D74B2")  # Mittelblauer Hintergrund
        try:
            self.haupt_fenster.iconbitmap('resources/fs.ico')
        except:
            pass
        self.bild_pfad = ""
        self.original_bild = None
        self.verarbeitetes_bild = None
        self.bild_label = None
        self.unschaerfe_wert = tk.IntVar(value=5)
        self.ist_unschaerfe_modus = False
        self.bild_verzeichnis = ""
        self.bild_dateien = []
        self.aktueller_bild_index = -1
        
        # Fenstergröße und Zentrierung
        breite = 600
        hoehe = 650
        bildschirm_breite = self.haupt_fenster.winfo_screenwidth()
        bildschirm_hoehe = self.haupt_fenster.winfo_screenheight()
        x = (bildschirm_breite - breite) // 2
        y = (bildschirm_hoehe - hoehe) // 2
        self.haupt_fenster.geometry(f"{breite}x{hoehe}+{x}+{y}")
        self.haupt_fenster.resizable(True, True)
        
        # Menüleiste
        self.erstelle_menue()
        
        # Hauptframe
        self.haupt_frame = ttk.Frame(self.haupt_fenster)
        self.haupt_frame.pack(expand=True, fill="both", padx=10, pady=10)
        self.haupt_frame.configure(style="Custom.TFrame")
        
        # Werkzeugleiste für Filter
        self.werkzeug_leiste = ttk.Frame(self.haupt_frame)
        self.werkzeug_leiste.pack(fill="x", pady=5)
        self.werkzeug_leiste.configure(style="Custom.TFrame")
        
        # Buttons
        self.button_oeffnen = ttk.Button(
            self.werkzeug_leiste,
            text="Bild öffnen",
            command=self.oeffne_bild
        )
        self.button_oeffnen.pack(side=tk.LEFT, padx=5)
        
        self.button_graustufen = ttk.Button(
            self.werkzeug_leiste,
            text="Graustufen",
            command=self.wende_graustufen_an,
            state="disabled"
        )
        self.button_graustufen.pack(side=tk.LEFT, padx=5)
        
        self.button_kanten = ttk.Button(
            self.werkzeug_leiste,
            text="Kanten",
            command=self.wende_kanten_an,
            state="disabled"
        )
        self.button_kanten.pack(side=tk.LEFT, padx=5)
        
        self.button_unschaerfe = ttk.Button(
            self.werkzeug_leiste,
            text="Unschärfe",
            command=self.zeige_unschaerfe_slider,
            state="disabled"
        )
        self.button_unschaerfe.pack(side=tk.LEFT, padx=5)
        
        self.button_speichern = ttk.Button(
            self.werkzeug_leiste,
            text="Speichern",
            command=self.speichere_bild,
            state="disabled"
        )
        self.button_speichern.pack(side=tk.LEFT, padx=5)
        
        # Navigationsbuttons
        self.button_zurueck = ttk.Button(
            self.werkzeug_leiste,
            text="←",
            command=self.vorheriges_bild,
            state="disabled",
            width=3
        )
        self.button_zurueck.pack(side=tk.LEFT, padx=5)
        
        self.button_vor = ttk.Button(
            self.werkzeug_leiste,
            text="→",
            command=self.naechstes_bild,
            state="disabled",
            width=3
        )
        self.button_vor.pack(side=tk.LEFT, padx=5)
        
        # Schieberegler für Unschärfe (immer sichtbar)
        self.unschaerfe_frame = ttk.Frame(self.haupt_frame)
        self.unschaerfe_frame.pack(fill="x", pady=5)
        self.unschaerfe_frame.configure(style="Custom.TFrame")
        self.unschaerfe_label = ttk.Label(self.unschaerfe_frame, background="#2D74B2", text="Unschärfe-Intensität")
        self.unschaerfe_label.pack(side=tk.LEFT, padx=5)
        self.unschaerfe_slider = ttk.Scale(
            self.unschaerfe_frame,
            from_=1, to=21,
            orient="horizontal",
            variable=self.unschaerfe_wert,
            command=self.aktualisiere_unschaerfe,
            state="disabled"
        )
        self.unschaerfe_slider.pack(side=tk.LEFT, padx=5)
        
        # Bildanzeigebereich (quadratisch, weißer Hintergrund)
        self.bild_frame = ttk.Frame(self.haupt_frame, style="Custom.TFrame")
        self.bild_frame.pack(expand=True, fill="both")
        self.bild_label = ttk.Label(self.bild_frame, background="white")
        #self.bild_label.pack(expand=True, fill="both", padx=10, pady=10)
        self.bild_label.pack(anchor="center", pady=20)
        self.bild_frame.configure(width=500, height=500)
        self.bild_frame.pack_propagate(False)
        
        # Stil für weißen Rahmen
        style = ttk.Style()
        style.configure("White.TFrame", background="white")
        style.configure("Custom.TFrame", background="#2D74B2")
        
    def erstelle_menue(self):
        """Erstellt die Menüleiste. Fügt Datei- und Hilfe-Menüs hinzu."""
        menue_leiste = tk.Menu(self.haupt_fenster)
        self.haupt_fenster.config(menu=menue_leiste)
        
        datei_menue = tk.Menu(menue_leiste, tearoff=0)
        menue_leiste.add_cascade(label="Datei", menu=datei_menue)
        datei_menue.add_command(label="Bild öffnen", command=self.oeffne_bild)
        datei_menue.add_command(label="Bild speichern", command=self.speichere_bild)
        datei_menue.add_command(label="Beenden", command=self.beende_anwendung)
        
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
            self.bild_verzeichnis = os.path.dirname(datei_pfad)
            self.lade_bild_dateien()
            self.aktueller_bild_index = self.bild_dateien.index(os.path.basename(datei_pfad))
            self.lade_bild(datei_pfad)
            # Aktiviere alle Buttons nach Bildladen
            self.button_graustufen.configure(state="normal")
            self.button_kanten.configure(state="normal")
            self.button_unschaerfe.configure(state="normal")
            self.button_speichern.configure(state="normal")
            self.button_zurueck.configure(state="normal")
            self.button_vor.configure(state="normal")
        except Exception as e:
            messagebox.showerror("Fehler", f"Fehler beim Öffnen des Bildes: {e}")
            
    def lade_bild_dateien(self):
        """Lädt Liste der Bilddateien im Verzeichnis."""
        self.bild_dateien = [
            f for f in os.listdir(self.bild_verzeichnis)
            if f.lower().endswith(('.jpg', '.jpeg', '.png'))
        ]
        self.bild_dateien.sort()
        
    def lade_bild(self, datei_pfad):
        """Lädt ein Bild und zeigt es an."""
        self.bild_pfad = datei_pfad
        self.original_bild = cv2.imread(datei_pfad)
        if self.original_bild is None:
            raise ValueError("Bild konnte nicht geladen werden")
        self.verarbeitetes_bild = self.original_bild.copy()
        self.zeige_bild(self.verarbeitetes_bild)
        self.haupt_fenster.title(f"BildVerarbeitung - {os.path.basename(datei_pfad)}")
        self.ist_unschaerfe_modus = False
        self.unschaerfe_slider.configure(state="disabled")
        
    def vorheriges_bild(self):
        """Lädt das vorherige Bild im Verzeichnis."""
        if not self.bild_dateien or self.aktueller_bild_index <= 0:
            return
        self.aktueller_bild_index -= 1
        neuer_pfad = os.path.join(self.bild_verzeichnis, self.bild_dateien[self.aktueller_bild_index])
        self.lade_bild(neuer_pfad)
        
    def naechstes_bild(self):
        """Lädt das nächste Bild im Verzeichnis."""
        if not self.bild_dateien or self.aktueller_bild_index >= len(self.bild_dateien) - 1:
            return
        self.aktueller_bild_index += 1
        neuer_pfad = os.path.join(self.bild_verzeichnis, self.bild_dateien[self.aktueller_bild_index])
        self.lade_bild(neuer_pfad)
        
    def zeige_bild(self, bild):
        """Zeigt ein OpenCV-Bild im Tkinter-Label an."""
        if bild is None:
            return
            
        bild_rgb = cv2.cvtColor(bild, cv2.COLOR_BGR2RGB)
        hoehe, breite = bild.shape[:2]
        max_groesse = 480  # Etwas kleiner als Bildframe für Padding
        skala = min(max_groesse / breite, max_groesse / hoehe)
        neue_breite = int(breite * skala)
        neue_hoehe = int(hoehe * skala)
        bild_skaliered = cv2.resize(bild_rgb, (neue_breite, neue_hoehe), interpolation=cv2.INTER_AREA)
        
        pil_bild = Image.fromarray(bild_skaliered)
        tk_bild = ImageTk.PhotoImage(pil_bild)
        
        self.bild_label.configure(image=tk_bild)
        self.bild_label.image_ref = tk_bild
        
    def wende_graustufen_an(self):
        if self.original_bild is None:
            messagebox.showwarning("Warnung", "Kein Bild geladen!")
            return
        self.ist_unschaerfe_modus = False
        self.unschaerfe_slider.configure(state="disabled")
        self.verarbeitetes_bild = cv2.cvtColor(self.original_bild, cv2.COLOR_BGR2GRAY)
        self.verarbeitetes_bild = cv2.cvtColor(self.verarbeitetes_bild, cv2.COLOR_GRAY2BGR)
        self.zeige_bild(self.verarbeitetes_bild)
        
    def wende_kanten_an(self):
        if self.original_bild is None:
            messagebox.showwarning("Warnung", "Kein Bild geladen!")
            return
        self.ist_unschaerfe_modus = False
        self.unschaerfe_slider.configure(state="disabled")
        grau_bild = cv2.cvtColor(self.original_bild, cv2.COLOR_BGR2GRAY)
        self.verarbeitetes_bild = cv2.Canny(grau_bild, 100, 200)
        self.verarbeitetes_bild = cv2.cvtColor(self.verarbeitetes_bild, cv2.COLOR_GRAY2BGR)
        self.zeige_bild(self.verarbeitetes_bild)
        
    def zeige_unschaerfe_slider(self):
        if self.original_bild is None:
            messagebox.showwarning("Warnung", "Kein Bild geladen!")
            return
        self.ist_unschaerfe_modus = True
        self.unschaerfe_slider.configure(state="normal")
        self.aktualisiere_unschaerfe(None)
        
    def aktualisiere_unschaerfe(self, event):
        if self.original_bild is None or not self.ist_unschaerfe_modus:
            return
        k = self.unschaerfe_wert.get()
        if k % 2 == 0:  # Kernelgröße muss ungerade sein
            k += 1
        self.verarbeitetes_bild = cv2.GaussianBlur(self.original_bild, (k, k), 0)
        self.zeige_bild(self.verarbeitetes_bild)
        
    def speichere_bild(self):
        if self.verarbeitetes_bild is None:
            messagebox.showwarning("Warnung", "Kein Bild zum Speichern!")
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
        messagebox.showinfo("Über", "Bildverarbeitung mit OpenCV. Version 1.2. MIT-Lizenz.")
        
    def beende_anwendung(self):
        self.haupt_fenster.destroy()

if __name__ == "__main__":
    haupt_fenster = ThemedTk(theme="plastik")
    app = Bildverarbeitung(haupt_fenster)
    haupt_fenster.mainloop()