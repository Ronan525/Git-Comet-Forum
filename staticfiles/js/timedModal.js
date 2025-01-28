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
});