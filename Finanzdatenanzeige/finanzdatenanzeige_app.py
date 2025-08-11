# Copyright (c) 2025 Franz Steinkress
# Licensed under the MIT License - see LICENSE for details
#
# finanzdatenanzeige_app.py
# Eine Tkinter-basierte Anwendung zum Anzeigen von CSV-Dateien von Banken.
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import csv
import os

class Finanzdatenanzeige:
    """Hauptklasse für die Finanzdatenanzeige-Anwendung."""
    
    def __init__(self, haupt_fenster):
        """Initialisiert das Hauptfenster. Erstellt Benutzeroberfläche."""
        self.haupt_fenster = haupt_fenster
        self.haupt_fenster.title("Finanzdatenanzeige")
        self.haupt_fenster.iconbitmap('resources/fs.ico')
        self.haupt_fenster.configure(bg="#E0E0E0")  # hellgrauer Hintergrund

        # ttk-Theme auf "alt" setzen
        style = ttk.Style()
        style.theme_use("alt")

        # Farben für Treeview anpassen
        style.configure("Treeview", background="#FFFFFF", foreground="black", fieldbackground="#FFFFFF")
        style.configure("TButton", background="#D0D0D0", foreground="black")

        self.csv_datei_pfad = ""
        
        # Fenstergröße und Zentrierung
        breite = 800
        hoehe = 600
        bildschirm_breite = self.haupt_fenster.winfo_screenwidth()
        bildschirm_hoehe = self.haupt_fenster.winfo_screenheight()
        x = (bildschirm_breite - breite) // 2
        y = (bildschirm_hoehe - hoehe) // 2
        self.haupt_fenster.geometry(f"{breite}x{hoehe}+{x}+{y}")
        self.haupt_fenster.resizable(True, True)
        
        # Menüleiste
        self.erstelle_menue()
        
        # Hauptframe
        self.haupt_frame = tk.Frame(self.haupt_fenster, bg="#E0E0E0")
        self.haupt_frame.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)

        # Grid-Konfiguration Hauptfenster
        self.haupt_fenster.grid_rowconfigure(0, weight=1)
        self.haupt_fenster.grid_columnconfigure(0, weight=1)
        
        # Button zum Öffnen der Datei
        tk.Button(
            self.haupt_frame,
            text="CSV-Datei öffnen",
            command=self.oeffne_csv,
            font="Arial 12",
            bg="#D0D0D0"
        ).grid(row=0, column=0, pady=10)
        
        # Frame für Tabelle + Scrollbars
        tabelle_frame = ttk.Frame(self.haupt_frame)
        tabelle_frame.grid(row=1, column=0, sticky="nsew")

        # Grid-Konfiguration für haupt_frame
        self.haupt_frame.grid_rowconfigure(1, weight=1)
        self.haupt_frame.grid_columnconfigure(0, weight=1)

        # Treeview (Tabelle)
        self.daten_tabelle = ttk.Treeview(tabelle_frame, show="headings")
        self.daten_tabelle.grid(row=0, column=0, sticky="nsew")

        # Vertikale Scrollbar
        vertikale_scrollleiste = ttk.Scrollbar(
            tabelle_frame, orient="vertical", command=self.daten_tabelle.yview
        )
        vertikale_scrollleiste.grid(row=0, column=1, sticky="ns")

        # Horizontale Scrollbar
        horizontale_scrollleiste = ttk.Scrollbar(
            tabelle_frame, orient="horizontal", command=self.daten_tabelle.xview
        )
        horizontale_scrollleiste.grid(row=1, column=0, sticky="ew")

        # Scrollbar-Verknüpfung
        self.daten_tabelle.configure(
            yscrollcommand=vertikale_scrollleiste.set,
            xscrollcommand=horizontale_scrollleiste.set
        )

        # Grid-Konfiguration für tabelle_frame
        tabelle_frame.rowconfigure(0, weight=1)
        tabelle_frame.columnconfigure(0, weight=1)

    def erstelle_menue(self):
        """Erstellt die Menüleiste. Fügt Datei- und Hilfe-Menüs hinzu."""
        menue_leiste = tk.Menu(self.haupt_fenster)
        self.haupt_fenster.config(menu=menue_leiste)
        
        # Dateimenü
        datei_menue = tk.Menu(menue_leiste, tearoff=0)
        menue_leiste.add_cascade(label="Datei", menu=datei_menue)
        datei_menue.add_command(label="Öffnen", command=self.oeffne_csv)
        datei_menue.add_command(label="Beenden", command=self.beende_anwendung)
        
        # Hilfemenü
        hilfe_menue = tk.Menu(menue_leiste, tearoff=0)
        menue_leiste.add_cascade(label="Hilfe", menu=hilfe_menue)
        hilfe_menue.add_command(label="Über", command=self.zeige_info)
    
    def oeffne_csv(self):
        """Öffnet eine CSV-Datei. Zeigt die Daten in der Tabelle an."""
        datei_pfad = filedialog.askopenfilename(
            title="CSV-Datei auswählen",
            filetypes=[("CSV-Dateien", "*.csv"), ("Alle Dateien", "*.*")]
        )
        if not datei_pfad:
            return
        
        try:
            with open(datei_pfad, "r", encoding="utf-8-sig") as datei:
                csv_leser = csv.reader(datei)
                kopfzeilen = next(csv_leser)  # Erste Zeile als Kopfzeilen
                
                # Tabelle zurücksetzen
                self.daten_tabelle.delete(*self.daten_tabelle.get_children())
                self.daten_tabelle["columns"] = kopfzeilen
                for spalte in kopfzeilen:
                    self.daten_tabelle.heading(spalte, text=spalte)
                    self.daten_tabelle.column(spalte, width=100, stretch=True)
                
                # Daten einfügen
                for zeile in csv_leser:
                    self.daten_tabelle.insert("", tk.END, values=zeile)
                
                self.csv_datei_pfad = datei_pfad
                self.haupt_fenster.title(f"Finanzdatenanzeige - {os.path.basename(datei_pfad)}")
        
        except UnicodeDecodeError:
            messagebox.showerror("Fehler", "Datei konnte nicht gelesen werden. Überprüfe das Encoding.")
        except Exception as e:
            messagebox.showerror("Fehler", f"Fehler beim Öffnen der Datei: {e}")
    
    def zeige_info(self):
        """Zeigt Informationen über die Anwendung."""
        messagebox.showinfo("Über", "Finanzdatenanzeige. Version 1.0. MIT-Lizenz.")
    
    def beende_anwendung(self):
        """Beendet die Anwendung."""
        self.haupt_fenster.destroy()

if __name__ == "__main__":
    # Starte die Anwendung
    haupt_fenster = tk.Tk()
    app = Finanzdatenanzeige(haupt_fenster)
    haupt_fenster.mainloop()
