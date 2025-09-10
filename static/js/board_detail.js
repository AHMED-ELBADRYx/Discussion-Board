class BoardDetail {
    constructor() {
        this.init();
    }

    init() {
        // Check if elements exist before setting up event handlers
        if (this.isBoardDetailPage()) {
            this.setupEventListeners();
            this.setupKeyboardShortcuts();
        }
    }

    isBoardDetailPage() {
        // Verify that we are on the board details page
        return document.querySelector('.topic-row') !== null || 
               document.querySelector('input[name="sort"]') !== null;
    }

    setupEventListeners() {
        this.setupSortButtons();
        this.setupTopicRows();
        this.setupSortableHeaders();
        this.setupPaginationLinks();
    }

    setupSortButtons() {
        const sortButtons = document.querySelectorAll('input[name="sort"]');
        
        sortButtons.forEach(button => {
            button.addEventListener('change', (e) => {
                this.handleSortChange(e.target.value);
            });
        });
    }

    setupTopicRows() {
        const topicRows = document.querySelectorAll('.topic-row');
        
        topicRows.forEach(row => {
            row.addEventListener('click', (e) => {
                if (this.shouldIgnoreClick(e)) return;
                
                const href = row.dataset.href;
                if (href) {
                    this.navigateTo(href);
                }
            });
            
            // Change cursor style on row hover
            row.addEventListener('mouseenter', () => {
                row.style.cursor = 'pointer';
            });
            
            row.addEventListener('mouseleave', () => {
                row.style.cursor = 'default';
            });
        });
    }

    setupSortableHeaders() {
        const sortableHeaders = document.querySelectorAll('.sortable-header');
        
        sortableHeaders.forEach(header => {
            header.addEventListener('click', () => {
                const currentSort = new URLSearchParams(window.location.search).get('sort');
                const newSort = currentSort === 'oldest' ? 'newest' : 'oldest';
                this.handleSortChange(newSort);
            });
            
            header.addEventListener('mouseenter', () => {
                header.style.cursor = 'pointer';
            });
            
            header.addEventListener('mouseleave', () => {
                header.style.cursor = 'default';
            });
        });
    }

    setupPaginationLinks() {
        const paginationLinks = document.querySelectorAll('.pagination a');
        
        paginationLinks.forEach(link => {
            link.addEventListener('click', () => {
                this.showLoading();
            });
        });
    }

    setupKeyboardShortcuts() {
        document.addEventListener('keydown', (e) => {
            // Ctrl + N to create new topic (only on board page)
            if (e.key === 'n' && e.ctrlKey && this.isBoardDetailPage()) {
                e.preventDefault();
                this.createNewTopic();
            }
            
            // Esc to clear filters (only on board page)
            if (e.key === 'Escape' && this.isBoardDetailPage()) {
                e.preventDefault();
                this.clearFilters();
            }
        });
    }

    handleSortChange(sortValue) {
        const url = new URL(window.location);
        url.searchParams.set('sort', sortValue);
        url.searchParams.delete('page');
        this.navigateTo(url.toString());
    }

    shouldIgnoreClick(event) {
        return event.target.tagName === 'A' || 
               event.target.closest('a') ||
               event.target.tagName === 'BUTTON' ||
               event.target.closest('button') ||
               event.target.tagName === 'INPUT' ||
               event.target.closest('input');
    }

    navigateTo(url) {
        window.location.href = url;
    }

    showLoading() {
        const cardBody = document.querySelector('.card-body');
        if (cardBody) {
            cardBody.style.opacity = '0.5';
            cardBody.style.pointerEvents = 'none';
        }
    }

    createNewTopic() {
        const newTopicBtn = document.querySelector('a[href*="new_topic"]');
        if (newTopicBtn) {
            newTopicBtn.click();
        }
    }

    clearFilters() {
        const url = new URL(window.location);
        url.searchParams.delete('sort');
        url.searchParams.delete('page');
        this.navigateTo(url.toString());
    }
}

// Initialize object when content is loaded
document.addEventListener('DOMContentLoaded', function() {
    new BoardDetail();
});