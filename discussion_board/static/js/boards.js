document.addEventListener('DOMContentLoaded', function() {
    // جعل الصفوف قابلة للنقر
    const topicRows = document.querySelectorAll('.topic-row');
    topicRows.forEach(row => {
        row.style.cursor = 'pointer';
        row.addEventListener('click', function(e) {
            if (!e.target.closest('a')) {
                window.location.href = this.dataset.href;
            }
        });
    });
});
