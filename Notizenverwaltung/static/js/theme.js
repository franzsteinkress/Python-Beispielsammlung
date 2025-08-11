document.addEventListener('DOMContentLoaded', function() {
    // Alle Modal-Trigger Buttons/Links (hier noch keine im Beispiel, falls du mal brauchst)
    // Modals sind per ID referenziert

    // Funktion: Modal öffnen
    function openModal(modal) {
        if (!modal) return;
        modal.style.display = 'block';
        // Kurze Verzögerung, um CSS-Transitions zu triggern
        setTimeout(() => modal.classList.add('show'), 10);
        // Scroll verhindern (optional)
        document.body.style.overflow = 'hidden';
    }

    // Funktion: Modal schließen
    function closeModal(modal) {
        if (!modal) return;
        modal.classList.remove('show');
        // Warte bis CSS-Transition vorbei (300ms)
        setTimeout(() => {
            modal.style.display = 'none';
            document.body.style.overflow = '';
        }, 300);
    }

    // Alle modalen Close-Buttons mit data-bs-dismiss="modal"
    document.querySelectorAll('[data-bs-dismiss="modal"]').forEach(btn => {
        btn.addEventListener('click', function() {
            const modal = btn.closest('.modal');
            closeModal(modal);
        });
    });

    // Optional: Modals auch durch Klick auf den Hintergrund schließen
    document.querySelectorAll('.modal').forEach(modal => {
        modal.addEventListener('click', e => {
            if (e.target === modal) closeModal(modal);
        });
    });

    // Beispiel: Funktion zum Öffnen eines Modals per ID
    window.showModalById = function(id) {
        const modal = document.getElementById(id);
        openModal(modal);
    };
});
