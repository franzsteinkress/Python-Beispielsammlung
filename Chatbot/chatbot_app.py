# Copyright (c) 2025 Franz Steinkress
# Licensed under the MIT License - see LICENSE for details
#
# chatbot_app.py
# Eine Flask-Webanwendung mit einem einfachen Chatbot Simulator

from flask import Flask, render_template, request, session

# Chatbot-Simulator initialisieren
web_app = Flask(__name__)
web_app.secret_key = "mein_geheimer_schluessel_123"  # Setze einen sicheren, eindeutigen Schlüssel

def simple_chatbot_response(user_input):
    responses = {
        "hallo": "Hallo! Wie kann ich dir helfen?",
        "Hallo": "Hallo! Wie kann ich dir helfen?",
        "hilfe": "Ich bin hier, um zu antworten. Was möchtest du wissen?",
        "Hilfe": "Ich bin hier, um zu antworten. Was möchtest du wissen?",
        "bye": "Tschüss, bis bald!",
        "Bye": "Tschüss, bis bald!"
    }
    user_input = user_input.lower()
    for key, response in responses.items():
        if key in user_input:
            return response
    return f"Antwort: Du hast '{user_input}' gesagt!"

# Routen definieren
@web_app.route("/")
def render_home():
    """Rendert die Startseite."""
    return render_template("index.html")

@web_app.route("/get")
def fetch_bot_response():
    user_input = request.args.get("msg")
    if "chat_history" not in session:
        session["chat_history"] = []
    response = simple_chatbot_response(user_input)
    session["chat_history"].append({"user": user_input, "bot": response})
    session.modified = True
    return response

@web_app.route("/clear")
def clear_history():
    """Löscht die Chat-Historie aus der Session."""
    session.pop("chat_history", None)  # Entfernt chat_history aus der Session
    session.modified = True
    return "Chat-Historie gelöscht!"

if __name__ == "__main__":
    # Starte die Chatbot-Simulator
    web_app.run(
        host="0.0.0.0",
        port=5000,
        debug=True
    )