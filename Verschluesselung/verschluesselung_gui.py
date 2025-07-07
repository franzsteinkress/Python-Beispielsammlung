# Copyright (c) 2025 Franz Steinkress
# Licensed under the MIT License - see LICENSE for details
#
# verschluesselung_gui.py
# Ein GUI für das AES-Verschlüsselungstool

import tkinter as tk
from tkinter import messagebox
import subprocess
import os

def encrypt():
    text = entry_text.get().strip()
    password = entry_password.get().strip()
    output_file = entry_output.get().strip() or "data/verschluesselt.bin"
    if not all([text, password]):
        messagebox.showerror("Fehler", "Bitte Text und Passwort eingeben!")
        return
    try:
        cmd = [os.path.join(os.getcwd(), ".venv", "Scripts", "python.exe"), "aesverschluesselung.py", 
               "--verschluesseln", text, "--passwort", password, "--ausgabe", output_file]
        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode == 0:
            messagebox.showinfo("Erfolg", f"Verschlüsselt in: {output_file}")
        else:
            messagebox.showerror("Fehler", f"Verschlüsselung fehlgeschlagen:\n{result.stderr}")
    except Exception as e:
        messagebox.showerror("Fehler", f"Fehler: {str(e)}")

def decrypt():
    password = entry_password_dec.get().strip()
    input_file = entry_input.get().strip() or "data/verschluesselt.bin"
    original_text = entry_original.get().strip()
    if not all([password, input_file, original_text]):
        messagebox.showerror("Fehler", "Bitte Passwort, Eingabedatei und Originaltext eingeben!")
        return
    try:
        cmd = [os.path.join(os.getcwd(), ".venv", "Scripts", "python.exe"), "aesverschluesselung.py", 
               "--entschluesseln", "--passwort", password, "--eingabe", input_file, "--original", original_text]
        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode == 0:
            output = result.stdout.strip()
            messagebox.showinfo("Erfolg", f"Entschlüsselter Text: {output}\nÜbereinstimmung: {output == original_text}")
        else:
            messagebox.showerror("Fehler", f"Entschlüsselung fehlgeschlagen:\n{result.stderr}")
    except Exception as e:
        messagebox.showerror("Fehler", f"Fehler: {str(e)}")

# Hauptfenster
fenster = tk.Tk()
fenster.title("AES Verschlüsselung GUI")
fenster.iconbitmap('resources/fs.ico')  # Benutzerdefiniertes Icon
fenster.geometry("400x300")

# Frame für Verschlüsseln
frame_encrypt = tk.LabelFrame(fenster, text="Verschlüsseln")
frame_encrypt.grid(row=0, column=0, padx=10, pady=5, sticky="ew")
tk.Label(frame_encrypt, text="Text:").grid(row=0, column=0, padx=5, pady=2, sticky="e")
entry_text = tk.Entry(frame_encrypt, width=30)
entry_text.grid(row=0, column=1, padx=5, pady=2, sticky="w")
tk.Label(frame_encrypt, text="Passwort:").grid(row=1, column=0, padx=5, pady=2, sticky="e")
entry_password = tk.Entry(frame_encrypt, width=30, show="*")
entry_password.grid(row=1, column=1, padx=5, pady=2, sticky="w")
tk.Label(frame_encrypt, text="Ausgabedatei:").grid(row=2, column=0, padx=5, pady=2, sticky="e")
entry_output = tk.Entry(frame_encrypt, width=30)
entry_output.grid(row=2, column=1, padx=5, pady=2, sticky="w")
tk.Button(frame_encrypt, text="Verschlüsseln", command=encrypt).grid(row=3, column=0, columnspan=2, pady=5)

# Frame für Entschlüsseln
frame_decrypt = tk.LabelFrame(fenster, text="Entschlüsseln")
frame_decrypt.grid(row=1, column=0, padx=10, pady=5, sticky="ew")
tk.Label(frame_decrypt, text="Passwort:").grid(row=0, column=0, padx=5, pady=2, sticky="e")
entry_password_dec = tk.Entry(frame_decrypt, width=30, show="*")
entry_password_dec.grid(row=0, column=1, padx=5, pady=2, sticky="w")
tk.Label(frame_decrypt, text="Eingabedatei:").grid(row=1, column=0, padx=5, pady=2, sticky="e")
entry_input = tk.Entry(frame_decrypt, width=30)
entry_input.grid(row=1, column=1, padx=5, pady=2, sticky="w")
tk.Label(frame_decrypt, text="Originaltext:").grid(row=2, column=0, padx=5, pady=2, sticky="e")
entry_original = tk.Entry(frame_decrypt, width=30)
entry_original.grid(row=2, column=1, padx=5, pady=2, sticky="w")
tk.Button(frame_decrypt, text="Entschlüsseln", command=decrypt).grid(row=3, column=0, columnspan=2, pady=5)

# Start der Hauptschleife
fenster.mainloop()