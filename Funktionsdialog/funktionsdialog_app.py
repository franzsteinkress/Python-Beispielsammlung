# Copyright (c) 2025 Franz Steinkress
# Licensed under the MIT License - see LICENSE for details
#
# funktionsdialog_app.py
# Ein Tkinter-basierter Funktionsdialog mit Texteditor und verschiedenen Werkzeugen

import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from PIL import Image, ImageTk
import hashlib
import os
import time

class Funktionsdialog:
    """Hauptklasse für die Funktionsdialog-Anwendung."""
    
    def __init__(self, main_window):
        """Initialisiert das Hauptfenster."""
        self.main_window = main_window
        self.main_window.title("Funktionsdialog - Keine Datei")
        self.main_window.iconbitmap('resources/fs.ico')
        self.file_path = ""
        self.content_hash = ""
        
        # Fenstergröße und Zentrierung
        width = 600
        height = 600
        screen_width = self.main_window.winfo_screenwidth()
        screen_height = self.main_window.winfo_screenheight()
        x = (screen_width - width) // 2
        y = (screen_height - height) // 2
        self.main_window.geometry(f"{width}x{height}+{x}+{y}")
        self.main_window.resizable(False, False)
        
        # Textbereich und Scrollleiste
        self.text_area = tk.Text(self.main_window, wrap="word", font="Calibri 12", width=72)
        self.text_area.pack(expand=True, fill="both", side=tk.LEFT)
        self.scroll_bar = tk.Scrollbar(self.main_window, width=16)
        self.scroll_bar.pack(expand=True, fill="both", side=tk.LEFT)
        self.text_area.config(yscrollcommand=self.scroll_bar.set)
        self.scroll_bar.config(command=self.text_area.yview)
        
        # Anfangshash berechnen
        self.content_hash = self.calculate_hash(self.text_area.get(1.0, tk.END))
        
        # Menü erstellen
        self.setup_menu()
    
    def setup_menu(self):
        """Konfiguriert das Hauptmenü."""
        menu_bar = tk.Menu(self.main_window)
        self.main_window.config(menu=menu_bar)
        
        # Dateimenü
        file_menu = tk.Menu(menu_bar, tearoff=0)
        menu_bar.add_cascade(label="Datei", menu=file_menu)
        file_menu.add_command(label="Neu", command=self.create_new_file)
        file_menu.add_command(label="Öffnen...", command=self.open_file)
        file_menu.add_command(label="Speichern", command=self.save_file)
        file_menu.add_command(label="Speichern unter...", command=self.save_as_file)
        file_menu.add_separator()
        file_menu.add_command(label="Beenden", command=self.exit_app)
        
        # Werkzeugmenü
        tools_menu = tk.Menu(menu_bar, tearoff=0)
        menu_bar.add_cascade(label="Werkzeuge", menu=tools_menu)
        tools_menu.add_command(label="Uhr", command=self.show_clock)
        tools_menu.add_command(label="Fortschrittsbalken", command=self.show_progressbar)
        tools_menu.add_command(label="Kalkulator", command=self.open_calculator)
        tools_menu.add_command(label="Bildbetrachter", command=self.show_image_viewer)
        tools_menu.add_command(label="Betriebssystem-Info", command=self.show_os_info)
        tools_menu.add_command(label="Übersetzer", command=self.show_translator)
        
        # Hilfemenü
        help_menu = tk.Menu(menu_bar, tearoff=0)
        menu_bar.add_cascade(label="Hilfe", menu=help_menu)
        help_menu.add_command(label="Über...", command=self.show_about_info)
    
    def calculate_hash(self, content):
        """Berechnet den SHA-224-Hash eines Inhalts."""
        return hashlib.sha224(content.encode("utf-8")).hexdigest()
    
    def create_new_file(self):
        """Erstellt eine neue, leere Datei."""
        content = self.text_area.get(1.0, tk.END)
        if self.content_hash != self.calculate_hash(content):
            if not messagebox.askokcancel("Änderungen", "Nicht gespeicherte Änderungen vorhanden.\nTrotzdem neu erstellen?"):
                return
        self.file_path = ""
        self.main_window.title("Funktionsdialog - Keine Datei")
        self.text_area.delete(1.0, tk.END)
        self.content_hash = self.calculate_hash(self.text_area.get(1.0, tk.END))
    
    def open_file(self):
        """Öffnet eine Textdatei."""
        file_path = filedialog.askopenfilename(
            title="Datei auswählen",
            initialdir="demotext",
            filetypes=[("Textdateien", "*.txt"), ("Alle Dateien", "*.*")]
        )
        if file_path:
            try:
                with open(file_path, "r", encoding="utf-8") as file:
                    content = file.read()
                    self.text_area.delete(1.0, tk.END)
                    self.text_area.insert("end", content)
                    self.file_path = file_path
                    self.main_window.title(f"Funktionsdialog - {self.file_path}")
                    self.content_hash = self.calculate_hash(self.text_area.get(1.0, tk.END))
            except OSError:
                messagebox.showerror("Fehler", "Fehler beim Zugriff auf die Datei")
    
    def save_file(self):
        """Speichert die aktuelle Datei."""
        if self.file_path and os.path.exists(self.file_path):
            try:
                with open(self.file_path, "w", encoding="utf-8") as file:
                    content = self.text_area.get(1.0, tk.END)
                    file.write(content)
                    self.content_hash = self.calculate_hash(content)
            except OSError:
                messagebox.showerror("Fehler", "Fehler beim Zugriff auf die Datei")
        else:
            self.save_as_file()
    
    def save_as_file(self):
        """Speichert die Datei unter einem neuen Namen."""
        file_path = filedialog.asksaveasfilename(
            title="Datei speichern",
            initialdir="demotext",
            filetypes=[("Textdateien", "*.txt"), ("Alle Dateien", "*.*")]
        )
        if file_path:
            try:
                with open(file_path, "w", encoding="utf-8") as file:
                    content = self.text_area.get(1.0, tk.END)
                    file.write(content)
                    self.file_path = file_path
                    self.main_window.title(f"Funktionsdialog - {self.file_path}")
                    self.content_hash = self.calculate_hash(content)
            except OSError:
                messagebox.showerror("Fehler", "Fehler beim Zugriff auf die Datei")
    
    def show_about_info(self):
        """Zeigt Informationen über die Anwendung an."""
        messagebox.showinfo("Über", "Ein einfacher Texteditor mit zusätzlichen Werkzeugen")
    
    def exit_app(self):
        """Beendet die Anwendung."""
        content = self.text_area.get(1.0, tk.END)
        if self.content_hash != self.calculate_hash(content):
            if not messagebox.askokcancel("Beenden", "Nicht gespeicherte Änderungen vorhanden.\nTrotzdem beenden?"):
                return
        self.main_window.destroy()
    
    def show_clock(self):
        """Zeigt ein Fenster mit einer digitalen Uhr an."""
        tool_window = tk.Toplevel(self.main_window)
        tool_window.title("Digitale Uhr")
        tool_window.iconbitmap('resources/fs.ico')
        tool_window.geometry("300x130")
        tool_window.resizable(False, False)
        tool_window.configure(bg="#2D74B2")
        
        # Uhrzeige
        time_label = tk.Label(
            tool_window,
            font="Arial 48",
            bg="#2D74B2",
            fg="white",
            text="00:00:00"
        )
        time_label.pack(fill="x")
        
        def update_time():
            current_time = time.strftime("%H:%M:%S")
            time_label.config(text=current_time)
            time_label.after(1000, update_time)
        
        update_time()
        
        # Schließen-Button
        button_frame = tk.Frame(tool_window, bg="gray")
        button_frame.pack(pady=10)
        tk.Button(button_frame, text="Schließen", command=tool_window.destroy).pack()
    
    def show_progressbar(self):
        """Zeigt ein Fenster mit Fortschrittsbalken an."""
        tool_window = tk.Toplevel(self.main_window)
        tool_window.title("Fortschrittsbalken")
        tool_window.iconbitmap('resources/fs.ico')
        width = 310
        height = 240
        screen_width = self.main_window.winfo_screenwidth()
        screen_height = self.main_window.winfo_screenheight()
        x = (screen_width - width) // 2
        y = (screen_height - height) // 2
        tool_window.geometry(f"{width}x{height}+{x}+{y}")
        tool_window.resizable(False, False)
        tool_window.configure(bg="white", padx=5, pady=5)
        tool_window.transient(self.main_window)
        tool_window.grab_set()
        
        # Erster Fortschrittsbalken
        progress_bar1 = ttk.Progressbar(tool_window)
        progress_bar1.grid(column=0, row=0, columnspan=4, padx=10, pady=5)
        ttk.Button(
            tool_window,
            text="Start",
            command=progress_bar1.start
        ).grid(column=0, row=1, columnspan=4, padx=10, pady=5)
        
        # Trennlinie
        ttk.Separator(tool_window, orient="horizontal").grid(
            column=0, row=2, columnspan=4, sticky="ew",
            pady=5
        )
        
        # Zweiter Fortschrittsbalken
        progress_bar2 = ttk.Progressbar(
            tool_window,
            orient="horizontal",
            mode="indeterminate",
            length=280
        )
        progress_bar2.grid(column=0, row=3, columnspan=4, padx=10, pady=5)
        ttk.Button(
            tool_window,
            text="Start",
            command=progress_bar2.start
        ).grid(column=1, row=4, padx=5, pady=5, sticky="e")
        ttk.Button(
            tool_window,
            text="Stop",
            command=progress_bar2.stop
        ).grid(column=2, row=4, padx=5, pady=5, sticky="w")
        
        # Trennlinie
        ttk.Separator(tool_window, orient="horizontal").grid(
            column=0, row=5, columnspan=4, sticky="ew",
            pady=5
        )
        
        # Schließen-Button
        tk.Button(
            tool_window,
            text="Schließen",
            command=tool_window.destroy
        ).grid(column=0, row=6, columnspan=4, padx=10, pady=10)
    
    def open_calculator(self):
        """Öffnet den Systemrechner."""
        os.system("calc")
    
    def show_image_viewer(self):
        """Zeigt ein Bild im Fenster an."""
        try:
            image_path = filedialog.askopenfilename(
                title="Bild auswählen",
                filetypes=[("Bilddateien", "*.jpg *.png *.bmp"), ("Alle Dateien", "*.*")]
            )
            if image_path:
                image = Image.open(image_path)
                image = image.resize((200, 200), Image.Resampling.LANCZOS)
                photo = ImageTk.PhotoImage(image)
                
                tool_window = tk.Toplevel(self.main_window)
                tool_window.title("Bildbetrachter")
                tool_window.iconbitmap('resources/fs.ico')
                tk.Label(tool_window, image=photo).pack(pady=5)
                tool_window.image_ref = photo
                tk.Button(
                    tool_window,
                    text="Schließen",
                    command=tool_window.destroy
                ).pack(pady=5)
        except Exception as e:
            messagebox.showerror("Fehler", f"Fehler beim Öffnen des Bildes: {e}")
    
    def show_os_info(self):
        """Zeigt Betriebssystem-Informationen im Textbereich an."""
        self.text_area.insert(tk.END, f"Betriebssystem: {os.name}\n")
        self.text_area.insert(tk.END, f"{'-' * 80}\n")
        self.text_area.insert(tk.END, f"Arbeitsverzeichnis: {os.getcwd()}\n")
        self.text_area.insert(tk.END, f"{'-' * 80}\n")
        self.text_area.insert(tk.END, f"Benutzername: {os.getlogin()}\n")
        self.text_area.insert(tk.END, f"{'-' * 80}\n")
        for key, value in os.environ.items():
            self.text_area.insert(tk.END, f"{key}: {value}\n")
        self.text_area.insert(tk.END, f"{'-' * 80}\n")
    
    def show_translator(self):
        """Zeigt ein Fenster für Textübersetzung an (vereinfacht)."""
        tool_window = tk.Toplevel(self.main_window)
        tool_window.title("Textübersetzer")
        tool_window.iconbitmap('resources/fs.ico')
        width = 600
        height = 300
        screen_width = self.main_window.winfo_screenwidth()
        screen_height = self.main_window.winfo_screenheight()
        x = (screen_width - width) // 2
        y = (screen_height - height) // 2
        tool_window.geometry(f"{width}x{height}+{x}+{y}")
        tool_window.resizable(False, False)
        tool_window.configure(bg="lightgreen")
        
        tk.Label(
            master=tool_window,
            text="TEXTÜBERSETZER",
            font="Arial 20 bold",
            bg="lightgreen"
        ).pack(pady=20)
        
        frame = tk.Frame(tool_window, bg="lightgreen")
        frame.pack(padx=10, pady=0)
        
        input_text = tk.Text(
            master=frame,
            font="Arial 10",
            height=5,
            wrap="word",
            padx=10,
            pady=5,
            width=20
        )
        input_text.grid(row=0, column=0, padx=5, pady=5)
        
        output_text = tk.Text(
            master=frame,
            font="Arial 10",
            height=5,
            wrap="word",
            padx=10,
            pady=5,
            width=20
        )
        output_text.grid(row=0, column=2, padx=5, pady=5)
        
        def translate():
            content = input_text.get(1.0, tk.END).strip()
            output_text.delete(1.0, tk.END)
            output_text.insert(tk.END, f"Übersetzt (Dummy): {content}")
            messagebox.showinfo("Hinweis", "Echte Übersetzung erfordert eine API-Verbindung.")
        
        tk.Button(
            master=frame,
            text="Übersetzen",
            width=10,
            font="Arial 12",
            command=translate
        ).grid(row=1, column=1, padx=10, pady=5)
        
        tk.Button(
            master=tool_window,
            text="Schließen",
            command=tool_window.destroy
        ).pack(pady=20)

if __name__ == "__main__":
    main_window = tk.Tk()
    app = Funktionsdialog(main_window)
    main_window.mainloop()