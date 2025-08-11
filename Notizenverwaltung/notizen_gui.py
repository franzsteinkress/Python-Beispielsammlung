# Copyright (c) 2025 Franz Steinkress
# Licensed under the MIT License - see LICENSE for details
#
# notizen_gui.py
# Eine grafische Benutzeroberfläche für die Flask-basierte REST-API zur Notizenverwaltung

import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import requests
import json

class NotizenGUI:
    """GUI für die Notizen-REST-API."""
    
    def __init__(self, root):
        """Initialisiert die GUI."""
        self.root = root
        self.root.title("Notizenverwaltung")
        self.root.geometry("600x400")
        self.root.iconbitmap('./static/ico/fs.ico')

        # Style konfigurieren
        style = ttk.Style()
        style.theme_use("clam")
        self.root.configure(bg="#2D74B2")
        style.configure("TFrame", background="#2D74B2")
        style.configure("TLabel", background="#2D74B2", foreground="white", font=("Segoe UI", 10))
        style.configure("Primary.TButton",
                        background="#2D74B2",
                        foreground="white",
                        font=("Segoe UI", 10, "bold"),
                        padding=(8, 4),
                        borderwidth=1)
        style.map("Primary.TButton",
                  background=[("active", "#255A92"), ("pressed", "#1F5380"), ("!disabled", "#2D74B2")],
                  foreground=[("disabled", "#CFCFCF"), ("!disabled", "white")])

        # API-Basis-URL
        self.api_url = "http://127.0.0.1:5000/api/notizen"
        
        # GUI-Elemente
        self.erstelle_gui()
        self.lade_notizen()
    
    def erstelle_gui(self):
        """Erstellt die Tkinter-Oberfläche."""
        # Frame für Notizen-Liste
        frame_liste = ttk.Frame(self.root, padding=10)
        frame_liste.pack(fill=tk.BOTH, expand=True)
        
        # Listbox für Notizen
        self.notizen_liste = tk.Listbox(frame_liste, height=10, width=50)
        self.notizen_liste.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.notizen_liste.bind('<<ListboxSelect>>', self.zeige_ausgewaehlte_notiz)
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(frame_liste)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.notizen_liste.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=self.notizen_liste.yview)
        
        # Frame für Eingabefelder
        frame_eingabe = ttk.Frame(self.root, padding=10)
        frame_eingabe.pack(fill=tk.X)
        
        # Titel-Eingabe
        ttk.Label(frame_eingabe, text="Titel:").pack(side=tk.LEFT)
        self.titel_eingabe = ttk.Entry(frame_eingabe, width=40)
        self.titel_eingabe.pack(side=tk.LEFT, padx=5)
        
        # Inhalt-Eingabe
        ttk.Label(frame_eingabe, text="Inhalt:").pack(side=tk.LEFT)
        self.inhalt_eingabe = ttk.Entry(frame_eingabe, width=40)
        self.inhalt_eingabe.pack(side=tk.LEFT, padx=5)
        
        # Buttons
        frame_buttons = ttk.Frame(self.root, padding=10)
        frame_buttons.pack(fill=tk.X)
        
        ttk.Button(frame_buttons, text="Neu", command=self.erstelle_notiz, style="Primary.TButton").pack(side=tk.LEFT, padx=5)
        ttk.Button(frame_buttons, text="Aktualisieren", command=self.aktualisiere_notiz, style="Primary.TButton").pack(side=tk.LEFT, padx=5)
        ttk.Button(frame_buttons, text="Löschen", command=self.loesche_notiz, style="Primary.TButton").pack(side=tk.LEFT, padx=5)
    
    def lade_notizen(self):
        """Lädt alle Notizen von der API und füllt die Listbox."""
        try:
            response = requests.get(self.api_url)
            response.raise_for_status()
            notizen = response.json()
            self.notizen_liste.delete(0, tk.END)
            for notiz in notizen:
                self.notizen_liste.insert(tk.END, f"{notiz['titel']} (ID: {notiz['id']})")
        except requests.exceptions.RequestException as e:
            messagebox.showerror("Fehler", f"Fehler beim Laden der Notizen: {e}")
    
    def zeige_ausgewaehlte_notiz(self, event):
        """Zeigt die Details der ausgewählten Notiz in den Eingabefeldern."""
        try:
            selection = self.notizen_liste.curselection()
            if not selection:
                return
            index = selection[0]
            notiz_text = self.notizen_liste.get(index)
            notiz_id = int(notiz_text.split(" (ID: ")[1].rstrip(")"))
            
            response = requests.get(f"{self.api_url}/{notiz_id}")
            response.raise_for_status()
            notiz = response.json()
            
            self.titel_eingabe.delete(0, tk.END)
            self.titel_eingabe.insert(0, notiz["titel"])
            self.inhalt_eingabe.delete(0, tk.END)
            self.inhalt_eingabe.insert(0, notiz["inhalt"])
            self.aktuelle_id = notiz_id
        except requests.exceptions.RequestException as e:
            messagebox.showerror("Fehler", f"Fehler beim Abrufen der Notiz: {e}")
    
    def erstelle_notiz(self):
        """Erstellt eine neue Notiz über die API."""
        titel = self.titel_eingabe.get()
        inhalt = self.inhalt_eingabe.get()
        if not titel:
            messagebox.showwarning("Warnung", "Titel ist erforderlich!")
            return
        try:
            response = requests.post(self.api_url, json={"titel": titel, "inhalt": inhalt})
            response.raise_for_status()
            self.lade_notizen()
            self.titel_eingabe.delete(0, tk.END)
            self.inhalt_eingabe.delete(0, tk.END)
            messagebox.showinfo("Erfolg", "Notiz erstellt!")
        except requests.exceptions.RequestException as e:
            messagebox.showerror("Fehler", f"Fehler beim Erstellen der Notiz: {e}")
    
    def aktualisiere_notiz(self):
        """Aktualisiert die ausgewählte Notiz über die API."""
        if not hasattr(self, 'aktuelle_id'):
            messagebox.showwarning("Warnung", "Bitte wähle eine Notiz aus!")
            return
        titel = self.titel_eingabe.get()
        inhalt = self.inhalt_eingabe.get()
        if not titel:
            messagebox.showwarning("Warnung", "Titel ist erforderlich!")
            return
        try:
            response = requests.put(f"{self.api_url}/{self.aktuelle_id}", json={"titel": titel, "inhalt": inhalt})
            response.raise_for_status()
            self.lade_notizen()
            self.titel_eingabe.delete(0, tk.END)
            self.inhalt_eingabe.delete(0, tk.END)
            messagebox.showinfo("Erfolg", "Notiz aktualisiert!")
        except requests.exceptions.RequestException as e:
            messagebox.showerror("Fehler", f"Fehler beim Aktualisieren der Notiz: {e}")
    
    def loesche_notiz(self):
        """Löscht die ausgewählte Notiz über die API."""
        if not hasattr(self, 'aktuelle_id'):
            messagebox.showwarning("Warnung", "Bitte wähle eine Notiz aus!")
            return
        try:
            response = requests.delete(f"{self.api_url}/{self.aktuelle_id}")
            response.raise_for_status()
            self.lade_notizen()
            self.titel_eingabe.delete(0, tk.END)
            self.inhalt_eingabe.delete(0, tk.END)
            messagebox.showinfo("Erfolg", "Notiz gelöscht!")
        except requests.exceptions.RequestException as e:
            messagebox.showerror("Fehler", f"Fehler beim Löschen der Notiz: {e}")

if __name__ == "__main__":
    root = tk.Tk()
    app = NotizenGUI(root)
    root.mainloop()
