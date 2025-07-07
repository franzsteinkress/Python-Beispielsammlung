# Copyright (c) 2025 Franz Steinkress
# Licensed under the MIT License - see LICENSE for details
#
# lizenzpruefer.py
# Eine GUI für das Lizenzprüfungssystem

import tkinter as tk
from tkinter import messagebox
import subprocess
import os

def generate_keypair():
    try:
        result = subprocess.run([os.path.join(os.getcwd(), ".venv", "Scripts", "python.exe"), "lizenzpruefer.py", "--generiere-schluessel"], 
                              capture_output=True, text=True)
        if result.returncode == 0:
            messagebox.showinfo("Erfolg", "Schlüsselpaar generiert!\n" + result.stdout)
        else:
            messagebox.showerror("Fehler", "Fehler beim Generieren:\n" + result.stderr)
    except Exception as e:
        messagebox.showerror("Fehler", f"Fehler: {str(e)}")

def create_license():
    lizenznehmer = entry_lizenznehmer.get().strip()
    ablaufdatum = entry_ablaufdatum.get().strip()
    produkt_id = entry_produkt_id.get().strip()
    lizenz_datei = entry_lizenz_datei.get().strip() or "config/licenses/lizenz.json"
    if not all([lizenznehmer, ablaufdatum, produkt_id]):
        messagebox.showerror("Fehler", "Bitte alle Felder ausfüllen!")
        return
    try:
        cmd = [os.path.join(os.getcwd(), ".venv", "Scripts", "python.exe"), "lizenzpruefer.py", "--erstelle-lizenz", "--lizenznehmer", lizenznehmer, 
               "--ablaufdatum", ablaufdatum, "--produkt-id", produkt_id, "--lizenz-datei", lizenz_datei]
        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode == 0:
            messagebox.showinfo("Erfolg", f"Lizenzdatei erstellt: {lizenz_datei}\n" + result.stdout)
        else:
            messagebox.showerror("Fehler", "Fehler beim Erstellen:\n" + result.stderr)
    except Exception as e:
        messagebox.showerror("Fehler", f"Fehler: {str(e)}")

def check_license():
    lizenz_datei = entry_lizenz_datei_check.get().strip() or "lizenz.json"
    if not lizenz_datei:
        messagebox.showerror("Fehler", "Bitte Lizenzdatei angeben!")
        return
    try:
        result = subprocess.run([os.path.join(os.getcwd(), ".venv", "Scripts", "python.exe"), "lizenzpruefer.py", "--pruefe-lizenz", "--lizenz-datei", lizenz_datei], 
                              capture_output=True, text=True)
        if result.returncode == 0:
            messagebox.showinfo("Erfolg", "Lizenz ist gültig!\n" + result.stdout)
        else:
            messagebox.showerror("Fehler", "Lizenz ungültig:\n" + result.stderr)
    except Exception as e:
        messagebox.showerror("Fehler", f"Fehler: {str(e)}")

# Hauptfenster
fenster = tk.Tk()
fenster.title("Lizenzprüfer GUI")
fenster.iconbitmap('resources/fs.ico')  # Benutzerdefiniertes Icon
fenster.geometry("400x340")

# Frame für Schlüsselpaar
frame_key = tk.LabelFrame(fenster, text="Schlüsselpaar generieren")
frame_key.grid(row=0, column=0, padx=10, pady=5, sticky="ew")
tk.Button(frame_key, text="Schlüsselpaar generieren", command=generate_keypair).grid(row=0, column=0, pady=5)

# Frame für Lizenz erstellen
frame_create = tk.LabelFrame(fenster, text="Lizenzdatei erstellen")
frame_create.grid(row=1, column=0, padx=10, pady=5, sticky="ew")
tk.Label(frame_create, text="Lizenznehmer:").grid(row=0, column=0, padx=5, pady=2)
entry_lizenznehmer = tk.Entry(frame_create, width=30)
entry_lizenznehmer.grid(row=0, column=1, padx=5, pady=2)
tk.Label(frame_create, text="Ablaufdatum (YYYY-MM-DD):").grid(row=1, column=0, padx=5, pady=2)
entry_ablaufdatum = tk.Entry(frame_create, width=30)
entry_ablaufdatum.grid(row=1, column=1, padx=5, pady=2)
tk.Label(frame_create, text="Produkt-ID:").grid(row=2, column=0, padx=5, pady=2)
entry_produkt_id = tk.Entry(frame_create, width=30)
entry_produkt_id.grid(row=2, column=1, padx=5, pady=2)
tk.Label(frame_create, text="Lizenzdatei:").grid(row=3, column=0, padx=5, pady=2)
entry_lizenz_datei = tk.Entry(frame_create, width=30)
entry_lizenz_datei.grid(row=3, column=1, padx=5, pady=2)
tk.Button(frame_create, text="Lizenz erstellen", command=create_license).grid(row=4, column=0, columnspan=2, pady=5)

# Frame für Lizenz prüfen
frame_check = tk.LabelFrame(fenster, text="Lizenzdatei prüfen")
frame_check.grid(row=2, column=0, padx=10, pady=5, sticky="ew")
tk.Label(frame_check, text="Lizenzdatei:").grid(row=0, column=0, pady=2, sticky="e")
entry_lizenz_datei_check = tk.Entry(frame_check, width=30)
entry_lizenz_datei_check.grid(row=0, column=1, pady=2, sticky="w")
tk.Button(frame_check, text="Lizenz prüfen", command=check_license).grid(row=1, column=0, columnspan=2, pady=5)

# Start der Hauptschleife
fenster.mainloop()