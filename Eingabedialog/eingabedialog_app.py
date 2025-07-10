# Copyright (c) 2025 Franz Steinkress
# Licensed under the MIT License - see LICENSE for details
#
# eingabedialog_app.py
# Ein einfaches Tkinter-Programm für einen Eingabedialog mit Hauptfenster

import tkinter as tk
from tkinter import ttk

class DialogWindow(tk.Frame):
    """Hauptfenster für die Dialoganwendung."""
    
    def __init__(self, master):
        """Initialisiert das Hauptfenster."""
        super().__init__(master)
        self.master = master
        self.master.title("Eingabedialog")
        self.master.geometry("300x100")
        self.master.configure(bg="#2D74B2")
        self.master.iconbitmap('resources/fs.ico')
        self._center_window(self.master)
        
        # Eingabetext und UI-Elemente
        self.input_text = tk.StringVar()
        self.input_text.set("Ihre Eingabe ...")
        
        # Label für die Eingabeanzeige
        tk.Label(
            self.master, 
            bg="turquoise",
            textvariable=self.input_text
            ).pack(ipady=15)
        
        # Button zum Öffnen des Dialogs
        tk.Button(self.master, text="Eingabe ändern", command=self.open_dialog).pack()
        
        # Horizontale Trennlinie
        ttk.Separator(self.master, orient='horizontal').place(relwidth=1)
    
    def _center_window(self, window):
        """Zentriert ein Fenster auf dem Bildschirm."""
        window.update_idletasks()
        width = window.winfo_width()
        height = window.winfo_height()
        x = (window.winfo_screenwidth() // 2) - (width // 2)
        y = (window.winfo_screenheight() // 2) - (height // 2)
        window.geometry(f'{width}x{height}+{x}+{y}')
    
    def open_dialog(self):
        """Öffnet den Eingabedialog."""
        dialog = InputDialog(self.master, self.input_text, "Eingabedialog", "Ihre Eingabe ...")
        self.master.wait_window(dialog.dialog_window)

class InputDialog:
    """Dialogfenster für Benutzereingaben."""
    
    def __init__(self, parent, input_text, title, label_text=''):
        """Initialisiert den Eingabedialog."""
        self.input_text = input_text
        self.dialog_window = tk.Toplevel(parent)
        self.dialog_window.transient(parent)
        self.dialog_window.grab_set()
        self.dialog_window.iconbitmap('resources/fs.ico')
        self._center_window(self.dialog_window)
        
        if title:
            self.dialog_window.title(title)
        if not label_text:
            label_text = "Wert"
        
        # Label für den Dialog
        tk.Label(self.dialog_window, text=label_text).pack(ipady=15)
        
        # Eingabefeld
        self.entry_field = tk.Entry(self.dialog_window, text=self.input_text.get())
        self.entry_field.pack(padx=15, pady=5)
        self.entry_field.focus_set()
        
        # Tastenbindungen
        self.dialog_window.bind("<Return>", self.confirm)
        self.dialog_window.bind("<Escape>", self.cancel)
        self.entry_field.bind("<Return>", self.confirm)
        self.entry_field.bind("<Escape>", self.cancel)
        
        # Buttons
        confirm_button = tk.Button(self.dialog_window, text="OK", width=10, command=self.confirm)
        confirm_button.pack(side=tk.LEFT, padx=15, pady=10)
        
        cancel_button = tk.Button(self.dialog_window, text="Abbrechen", width=10, command=self.cancel)
        cancel_button.pack(side=tk.RIGHT, padx=15, pady=10)
        
        # Horizontale Trennlinie
        ttk.Separator(self.dialog_window, orient='horizontal').place(relwidth=1)
    
    def _center_window(self, window):
        """Zentriert ein Fenster auf dem Bildschirm."""
        window.update_idletasks()
        width = window.winfo_width()
        height = window.winfo_height()
        x = (window.winfo_screenwidth() // 2) - (width // 2)
        y = (window.winfo_screenheight() // 2) - (height // 2)
        window.geometry(f'{width}x{height}+{x}+{y}')
    
    def confirm(self, event=None):
        """Bestätigt die Eingabe und schließt den Dialog."""
        self.input_text.set(self.entry_field.get())
        self.dialog_window.destroy()
    
    def cancel(self, event=None):
        """Schließt den Dialog ohne Speichern."""
        self.dialog_window.destroy()

# Hauptprogramm
if __name__ == "__main__":
    main_window = tk.Tk()
    app = DialogWindow(main_window)
    main_window.mainloop()