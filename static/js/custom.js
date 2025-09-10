document.addEventListener('DOMContentLoaded', function() {
    
    // Auto-hide alerts after 5 seconds (only if they exist)
    const alerts = document.querySelectorAll('.alert:not(.alert-danger, .alert-permanent)');
    if (alerts.length > 0) {
        setTimeout(function() {
            alerts.forEach(function(alert) {
                try {
                    const bsAlert = new bootstrap.Alert(alert);
                    bsAlert.close();
                } catch (error) {
                    // Fallback if Bootstrap not available
                    alert.style.display = 'none';
                }
            });
        }, 5000);
    }
    
    // Smooth scrolling for anchor links
    const anchorLinks = document.querySelectorAll('a[href^="#"]');
    anchorLinks.forEach(function(link) {
        link.addEventListener('click', function(e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                target.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });
});