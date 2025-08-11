# Copyright (c) 2025 Franz Steinkress
# Licensed under the MIT License - see LICENSE for details
#
# blog_app.py
# Eine Flask-basierte Blog-Anwendung mit SQLite-Datenbank

import sqlite3
from flask import Flask, render_template, request, url_for, flash, redirect
from werkzeug.exceptions import abort

# Blog-Anwendung initialisieren
blog_app = Flask(__name__)
blog_app.config.SECRET_KEY = "mein_geheimer_schluessel"
# Der Wert "mein_geheimer_schluessel" ist ein Platzhalter und sollte durch einen langen, 
# zufälligen und sicheren Schlüssel ersetzt werden.
# Der SECRET_KEY wird nur dann aktiv genutzt, wenn du Features wie Sitzungen, 
# Formulare mit CSRF-Schutz oder andere sicherheitsabhängige Funktionen in deiner Blog-Anwendung implementierst.

def get_db_connection():
    """Stellt eine Verbindung zur SQLite-Datenbank her."""
    db_connection = sqlite3.connect("database.db")
    db_connection.row_factory = sqlite3.Row
    return db_connection

def get_blog_post(post_id):
    """Holt einen Blog-Post anhand der ID."""
    db_connection = get_db_connection()
    post = db_connection.execute("SELECT * FROM posts WHERE id = ?", (post_id,)).fetchone()
    db_connection.close()
    if post is None:
        abort(404)
    return post

@blog_app.route("/")
def render_index():
    """Rendert die Startseite mit allen Blog-Posts."""
    db_connection = get_db_connection()
    posts = db_connection.execute("SELECT * FROM posts").fetchall()
    db_connection.close()
    return render_template("index.html", posts=posts)

@blog_app.route("/<int:post_id>")
def render_post(post_id):
    """Rendert einen einzelnen Blog-Post."""
    post = get_blog_post(post_id)
    return render_template("post.html", post=post)

@blog_app.route("/create", methods=["GET", "POST"])
def create_post():
    """Erstellt einen neuen Blog-Post."""
    if request.method == "POST":
        title = request.form["title"]
        content = request.form["content"]

        if not title:
            flash("Titel ist erforderlich!")
        else:
            db_connection = get_db_connection()
            db_connection.execute("INSERT INTO posts (title, content) VALUES (?, ?)", (title, content))
            db_connection.commit()
            db_connection.close()
            return redirect(url_for("render_index"))
        
    return render_template("create.html")

@blog_app.route("/<int:post_id>/edit", methods=["GET", "POST"])
def edit_post(post_id):
    """Bearbeitet einen bestehenden Blog-Post."""
    post = get_blog_post(post_id)

    if request.method == "POST":
        title = request.form["title"]
        content = request.form["content"]

        if not title:
            flash("Titel ist erforderlich!")
        else:
            db_connection = get_db_connection()
            db_connection.execute("UPDATE posts SET title = ?, content = ? WHERE id = ?", (title, content, post_id))
            db_connection.commit()
            db_connection.close()
            return redirect(url_for("render_index"))

    return render_template("edit.html", post=post)

@blog_app.route("/<int:post_id>/delete", methods=["POST"])
def delete_post(post_id):
    """Löscht einen Blog-Post."""
    post = get_blog_post(post_id)
    db_connection = get_db_connection()
    db_connection.execute("DELETE FROM posts WHERE id = ?", (post_id,))
    db_connection.commit()
    db_connection.close()
    flash(f'"{post["title"]}" wurde erfolgreich gelöscht!')
    return redirect(url_for("render_index"))

if __name__ == "__main__":
    # Starte die Blog-Anwendung
    blog_app.run(
        host="0.0.0.0",
        port=5000,
        debug=True
    )