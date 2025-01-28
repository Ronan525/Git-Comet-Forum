document.addEventListener('DOMContentLoaded', function() {
    const voteForms = document.querySelectorAll('.vote-form');
    voteForms.forEach(form => {
        form.addEventListener('submit', function(event) {
            if (!document.body.classList.contains('authenticated')) {
                event.preventDefault();
                var authModal = new bootstrap.Modal(document.getElementById('authModal'));
                authModal.show();
            }
        });
    });
});