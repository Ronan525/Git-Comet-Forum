document.addEventListener('DOMContentLoaded', function() {
    const excludedPaths = [
        '/post_detail/', // Adjust the path as needed
        '/contact_us/',  // Adjust the path as needed
        '/login/',       // Adjust the path as needed
        '/signup/'       // Adjust the path as needed
    ];

    const currentPath = window.location.pathname;

    if (!excludedPaths.some(path => currentPath.includes(path))) {
        setTimeout(function() {
            var signUpModal = new bootstrap.Modal(document.getElementById('signUpModal'));
            signUpModal.show();
        }, 5000); // 5 seconds
    }

    // Add event listener to hide the modal and set inert attribute
    document.getElementById('signUpModal').addEventListener('hidden.bs.modal', function() {
        document.querySelectorAll('[inert]').forEach(function(element) {
            element.removeAttribute('inert');
        });
    });

    // Add event listener to show the modal and set inert attribute
    document.getElementById('signUpModal').addEventListener('show.bs.modal', function() {
        document.querySelectorAll('body > *:not(#signUpModal)').forEach(function(element) {
            element.setAttribute('inert', '');
        });
    });
});