// scripts.js
// static/js/scripts.js

// Globale Funktionen definieren
window.ladeNotizen = function() {
    fetch('http://127.0.0.1:5000/api/notizen')
        .then(response => response.json())
        .then(notizen => {
            const tbody = document.getElementById('notizen_tabelle');
            tbody.innerHTML = '';
            notizen.forEach(notiz => {
                const row = document.createElement('tr');
                row.innerHTML = `
                    <td>${notiz.id}</td>
                    <td>${notiz.titel}</td>
                    <td>${notiz.inhalt}</td>
                    <td>${notiz.erstellt}</td>
                    <td>
                        <button class="btn btn-info btn-sm" onclick="zeigeDetails(${notiz.id})">Details</button>
                        <button class="btn btn-warning btn-sm" onclick="bearbeitenNotiz(${notiz.id})">Bearbeiten</button>
                        <button class="btn btn-danger btn-sm" onclick="loescheNotiz(${notiz.id})">Löschen</button>
                    </td>
                `;
                tbody.appendChild(row);
            });
        })
        .catch(error => zeigeFehler('Fehler beim Laden der Notizen: ' + error.message));
};

window.erstelleNotiz = function() {
    const titel = document.getElementById('post_titel').value;
    const inhalt = document.getElementById('post_inhalt').value;

    if (!titel) {
        zeigeFehler('Titel ist erforderlich!');
        return;
    }

    fetch('http://127.0.0.1:5000/api/notizen', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ titel, inhalt })
    })
    .then(response => response.json())
    .then(data => {
        if (data.fehler) throw new Error(data.fehler);
        ladeNotizen();
        document.getElementById('post_titel').value = '';
        document.getElementById('post_inhalt').value = '';
        alert('Notiz erstellt!');
    })
    .catch(error => zeigeFehler(error.message));
};

window.zeigeDetails = function(notizId) {
    fetch(`http://127.0.0.1:5000/api/notizen/${notizId}`)
        .then(response => response.json())
        .then(notiz => {
            document.getElementById('modal_id').textContent = notiz.id;
            document.getElementById('modal_titel').textContent = notiz.titel;
            document.getElementById('modal_inhalt').textContent = notiz.inhalt;
            document.getElementById('modal_erstellt').textContent = notiz.erstellt;
            new bootstrap.Modal(document.getElementById('notizModal')).show();
        })
        .catch(error => zeigeFehler('Fehler beim Laden der Details: ' + error.message));
};

window.bearbeitenNotiz = function(notizId) {
    fetch(`http://127.0.0.1:5000/api/notizen/${notizId}`)
        .then(response => response.json())
        .then(notiz => {
            document.getElementById('put_id').value = notiz.id;
            document.getElementById('put_titel').value = notiz.titel;
            document.getElementById('put_inhalt').value = notiz.inhalt;
            document.getElementById('bearbeiten_formular').style.display = 'block';
        })
        .catch(error => zeigeFehler('Fehler beim Laden der Notiz: ' + error.message));
};

window.aktualisiereNotiz = function() {
    const notizId = document.getElementById('put_id').value;
    const titel = document.getElementById('put_titel').value;
    const inhalt = document.getElementById('put_inhalt').value;

    if (!titel) {
        zeigeFehler('Titel ist erforderlich!');
        return;
    }

    fetch(`http://127.0.0.1:5000/api/notizen/${notizId}`, {
        method: 'PUT',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ titel, inhalt })
    })
    .then(response => response.json())
    .then(() => {
        ladeNotizen();
        schließeBearbeiten();
        alert('Notiz aktualisiert!');
    })
    .catch(error => zeigeFehler('Fehler beim Aktualisieren: ' + error.message));
};

window.loescheNotiz = function(notizId) {
    if (confirm('Möchtest du die Notiz wirklich löschen?')) {
        fetch(`http://127.0.0.1:5000/api/notizen/${notizId}`, {
            method: 'DELETE'
        })
        .then(response => response.json())
        .then(() => {
            ladeNotizen();
            alert('Notiz gelöscht!');
        })
        .catch(error => zeigeFehler('Fehler beim Löschen: ' + error.message));
    }
};

window.schließeBearbeiten = function() {
    document.getElementById('bearbeiten_formular').style.display = 'none';
    document.getElementById('put_titel').value = '';
    document.getElementById('put_inhalt').value = '';
};

window.zeigeFehler = function(nachricht) {
    const fehler = document.getElementById('fehler_meldung');
    fehler.textContent = nachricht;
    fehler.style.display = 'block';
    setTimeout(() => fehler.style.display = 'none', 5000);
};

// Event-Listener
document.addEventListener('DOMContentLoaded', () => {
    ladeNotizen(); // Jetzt funktioniert dies, da ladeNotizen global ist
});