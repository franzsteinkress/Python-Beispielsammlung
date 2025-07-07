# Copyright (c) 2025 Franz Steinkress
# Licensed under the MIT License - see LICENSE for details
#
# chatbot_app.py
# Eine Flask-Webanwendung mit einem einfachen Chatbot Simulator

from flask import Flask, render_template, request

# Chatbot-Simulator initialisieren
web_app = Flask(__name__)

def simple_chatbot_response(user_input):
    """Gibt eine einfache Antwort auf Benutzereingaben zurück."""
    return f"Antwort: Du hast '{user_input}' gesagt!"

# Routen definieren
@web_app.route("/")
def render_home():
    """Rendert die Startseite."""
    return render_template("index.html")

@web_app.route("/get")
def fetch_bot_response():
    """Holt die Antwort des Chatbot Simulators auf Benutzereingaben."""
    user_input = request.args.get("msg")
    return simple_chatbot_response(user_input)

if __name__ == "__main__":
    # Starte die Chatbot-Simulator
    web_app.run(
        host="0.0.0.0",
        port=5000,
        debug=True
    )