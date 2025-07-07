# Copyright (c) 2025 Franz Steinkress
# Licensed under the MIT License - see LICENSE for details
#
# bestaetigung_app.py
# Eine Tkinter-Anwendung mit einem nicht modalen Bestätigungsdialog

import tkinter as tk
from tkinter import ttk

class ConfirmationApp:
    """Hauptklasse für die Dialoganwendung."""
    
    def __init__(self, main_window):
        """Initialisiert das Hauptfenster."""
        self.main_window = main_window
        self.main_window.title("Dialog - Nicht modal")
        self.main_window.geometry("700x300")
        self._center_window(self.main_window)
        
        # Stil für ttk-Widgets
        self.theme_style = ttk.Style()
        self.theme_style.theme_use("classic")
        self.theme_style.configure("Custom.TButton", background='#40E0D0', bordercolor='#0000FF', borderwidth=2)
        self.theme_style.map("Custom.TButton", background=[('active', '#40E0D0')])
        self.main_window.configure(bg="turquoise")
        self.main_window.iconbitmap('resources/fs.ico')

        # Label im Hauptfenster
        info_label = tk.Label(
            master=self.main_window,
            text="Drücken öffnet einen nicht modalen Dialog",
            bg="turquoise",
            font="Arial 12"
        )
        info_label.pack(pady=40)
        
        # Button zum Öffnen des Dialogs
        ttk.Button(
            master=self.main_window,
            text="Drücken Sie hier",
            command=self.open_dialog,
            style="Custom.TButton"
        ).pack()
    
    def _center_window(self, window):
        """Zentriert ein Fenster auf dem Bildschirm."""
        window.update_idletasks()
        width = window.winfo_width()
        height = window.winfo_height()
        x = (window.winfo_screenwidth() // 2) - (width // 2)
        y = (window.winfo_screenheight() // 2) - (height // 2)
        window.geometry(f"{width}x{height}+{x}+{y}")
    
    def open_dialog(self):
        """Öffnet einen nicht modalen Bestätigungsdialog."""
        dialog_window = tk.Toplevel(self.main_window)
        dialog_window.title("Bestätigung")
        dialog_window.geometry("300x150")
        dialog_window.configure(bg="turquoise")
        dialog_window.iconbitmap('resources/fs.ico')
        self._center_window(dialog_window)
        
        # Label im Dialog
        info_label = tk.Label(
            master=dialog_window,
            text="Möchten Sie gerne fortfahren?",
            fg="white",
            bg="turquoise",
            font="Arial 12"
        )
        info_label.pack(pady=20)
        
        # Frame für Buttons
        button_frame = tk.Frame(dialog_window, bg="turquoise")
        button_frame.pack(pady=10)
        
        # Bestätigungs-Button
        confirm_button = tk.Button(
            master=button_frame,
            text="Ja",
            width=10,
            command=lambda: self.handle_selection("yes", dialog_window),
            bg="lightgray",
            fg="black"
        )
        confirm_button.grid(row=0, column=1, padx=5)
        
        # Abbrechen-Button
        cancel_button = tk.Button(
            master=button_frame,
            text="Nein",
            width=10,
            command=lambda: self.handle_selection("no", dialog_window),
            bg="lightgray",
            fg="black"
        )
        cancel_button.grid(row=0, column=2, padx=5)
    
    def handle_selection(self, option, dialog_window):
        """Verarbeitet die Auswahl des Benutzers."""
        dialog_window.destroy()
        if option == "no":
            self.main_window.destroy()

if __name__ == "__main__":
    main_window = tk.Tk()
    app = ConfirmationApp(main_window)
    main_window.mainloop()