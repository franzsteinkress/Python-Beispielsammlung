# Copyright (c) 2025 Franz Steinkress
# Licensed under the MIT License - see LICENSE for details
#
# notizen_app.py
# Eine Flask-basierte REST-API für Notizenverwaltung mit Weboberfläche

import sqlite3
import os
from flask import Flask, jsonify, request, render_template
from flask_cors import CORS
from datetime import datetime

class NotizenAPI:
    """Hauptklasse für die Notizen-REST-API."""

    def __init__(self):
        """Initialisiert die Flask-API. Konfiguriert Datenbank. Aktiviert CORS."""
        self.notizen_app = Flask(__name__)
        CORS(self.notizen_app)  # Erlaubt Cross-Origin-Anfragen
        self.notizen_app.config.DATENBANK_PFAD = "database.db"
        
        # Routen definieren
        self.erstelle_routen()
    
    def hole_datenbank_verbindung(self):
        """Stellt eine Verbindung zur SQLite-Datenbank her."""
        datenbank_verbindung = sqlite3.connect(self.notizen_app.config.DATENBANK_PFAD)
        datenbank_verbindung.row_factory = sqlite3.Row
        return datenbank_verbindung
    
    def hole_notiz(self, notiz_id):
        """Holt eine Notiz anhand der ID."""
        datenbank_verbindung = self.hole_datenbank_verbindung()
        notiz = datenbank_verbindung.execute(
            "SELECT * FROM notizen WHERE id = ?", (notiz_id,)
        ).fetchone()
        datenbank_verbindung.close()
        return notiz
    
    def erstelle_routen(self):
        """Definiert die API- und Weboberflächen-Routen."""
        
        @self.notizen_app.route("/api/notizen", methods=["GET"])
        def liste_notizen():
            """Listet alle Notizen."""
            datenbank_verbindung = self.hole_datenbank_verbindung()
            notizen = datenbank_verbindung.execute(
                "SELECT * FROM notizen ORDER BY erstellt DESC"
            ).fetchall()
            datenbank_verbindung.close()
            notizen_liste = [
                {
                    "id": notiz["id"],
                    "titel": notiz["titel"],
                    "inhalt": notiz["inhalt"],
                    "erstellt": notiz["erstellt"]
                } for notiz in notizen
            ]
            return jsonify(notizen_liste), 200
        
        @self.notizen_app.route("/api/notizen/<int:notiz_id>", methods=["GET"])
        def hole_notiz(notiz_id):
            """Ruft eine spezifische Notiz ab."""
            notiz = self.hole_notiz(notiz_id)
            if notiz is None:
                return jsonify({"fehler": "Notiz nicht gefunden"}), 404
            return jsonify({
                "id": notiz["id"],
                "titel": notiz["titel"],
                "inhalt": notiz["inhalt"],
                "erstellt": notiz["erstellt"]
            }), 200
        
        @self.notizen_app.route("/api/notizen", methods=["POST"])
        def erstelle_notiz():
            """Erstellt eine neue Notiz."""
            if not request.is_json:
                return jsonify({"fehler": "JSON-Daten erforderlich"}), 400
            daten = request.get_json()
            titel = daten.get("titel")
            inhalt = daten.get("inhalt", "")
            
            if not titel:
                return jsonify({"fehler": "Titel ist erforderlich"}), 400
            
            datenbank_verbindung = self.hole_datenbank_verbindung()
            cursor = datenbank_verbindung.cursor()
            cursor.execute(
                "INSERT INTO notizen (titel, inhalt) VALUES (?, ?)",
                (titel, inhalt)
            )
            datenbank_verbindung.commit()
            neue_id = cursor.lastrowid
            datenbank_verbindung.close()
            
            return jsonify({
                "id": neue_id,
                "titel": titel,
                "inhalt": inhalt,
                "erstellt": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }), 201
        
        @self.notizen_app.route("/api/notizen/<int:notiz_id>", methods=["PUT"])
        def aktualisiere_notiz(notiz_id):
            """Aktualisiert eine bestehende Notiz."""
            if not request.is_json:
                return jsonify({"fehler": "JSON-Daten erforderlich"}), 400
            notiz = self.hole_notiz(notiz_id)
            if notiz is None:
                return jsonify({"fehler": "Notiz nicht gefunden"}), 404
            
            daten = request.get_json()
            titel = daten.get("titel", notiz["titel"])
            inhalt = daten.get("inhalt", notiz["inhalt"])
            
            if not titel:
                return jsonify({"fehler": "Titel ist erforderlich"}), 400
            
            datenbank_verbindung = self.hole_datenbank_verbindung()
            datenbank_verbindung.execute(
                "UPDATE notizen SET titel = ?, inhalt = ? WHERE id = ?",
                (titel, inhalt, notiz_id)
            )
            datenbank_verbindung.commit()
            datenbank_verbindung.close()
            
            return jsonify({
                "id": notiz_id,
                "titel": titel,
                "inhalt": inhalt,
                "erstellt": notiz["erstellt"]
            }), 200
        
        @self.notizen_app.route("/api/notizen/<int:notiz_id>", methods=["DELETE"])
        def loesche_notiz(notiz_id):
            """Löscht eine Notiz."""
            notiz = self.hole_notiz(notiz_id)
            if notiz is None:
                return jsonify({"fehler": "Notiz nicht gefunden"}), 404
            
            datenbank_verbindung = self.hole_datenbank_verbindung()
            datenbank_verbindung.execute(
                "DELETE FROM notizen WHERE id = ?", (notiz_id,)
            )
            datenbank_verbindung.commit()
            datenbank_verbindung.close()
            
            return jsonify({"nachricht": f"Notiz {notiz_id} gelöscht"}), 200
        
        @self.notizen_app.route("/notizen")
        def zeige_weboberflaeche():
            """Rendert die Weboberfläche für die Notizenverwaltung."""
            return render_template("notizen.html")
    
    def starte(self):
        """Startet die Flask-API."""
        self.notizen_app.run(
            host="0.0.0.0",
            port=5000,
            debug=True
        )

if __name__ == "__main__":
    # Starte die Anwendung
    notizen_api = NotizenAPI()
    notizen_api.starte()