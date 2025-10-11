// Global search functionality
class GlobalSearch {
    constructor() {
        this.searchInput = document.querySelector('#global-search-input');
        this.searchResults = document.querySelector('#search-results-container');
        this.searchDropdown = document.querySelector('#search-dropdown');
        this.currentQuery = '';
        this.debounceTimer = null;
        
        if (this.searchInput) {
            this.init();
        }
    }
    
    init() {
        // Add event listeners
        this.searchInput.addEventListener('input', (e) => {
            this.handleInput(e.target.value);
        });
        
        this.searchInput.addEventListener('focus', () => {
            if (this.searchDropdown) {
                this.searchDropdown.classList.remove('hidden');
            }
        });
        
        this.searchInput.addEventListener('blur', () => {
            // Add a small delay to allow clicking on results
            setTimeout(() => {
                if (this.searchDropdown) {
                    this.searchDropdown.classList.add('hidden');
                }
            }, 200);
        });
        
        // Add keyboard navigation
        this.searchInput.addEventListener('keydown', (e) => {
            this.handleKeydown(e);
        });
    }
    
    handleInput(query) {
        // Clear previous timer
        clearTimeout(this.debounceTimer);
        
        // Debounce search requests
        this.debounceTimer = setTimeout(() => {
            if (query.length >= 2) {
                this.performAutocomplete(query);
            } else {
                if (this.searchDropdown) {
                    this.searchDropdown.classList.add('hidden');
                }
            }
        }, 300); // 300ms debounce
    }
    
    async performAutocomplete(query) {
        if (this.currentQuery === query) return; // Prevent duplicate requests
        this.currentQuery = query;
        
        try {
            const response = await fetch(`/search/autocomplete/?q=${encodeURIComponent(query)}`);
            const data = await response.json();
            
            if (data.results && data.results.length > 0) {
                this.displayAutocompleteResults(data.results);
            } else {
                this.displayNoResults();
            }
        } catch (error) {
            console.error('Search error:', error);
            this.hideResults();
        }
    }
    
    displayAutocompleteResults(results) {
        if (!this.searchResults) return;
        
        // Clear previous results
        this.searchResults.innerHTML = '';
        
        // Create result groups by category
        const groupedResults = this.groupByCategory(results);
        
        // Create HTML for each group
        let html = '';
        for (const [category, items] of Object.entries(groupedResults)) {
            html += `
                <div class="border-b border-gray-200 dark:border-gray-700 last:border-b-0">
                    <div class="px-4 py-2 text-xs font-semibold text-gray-500 dark:text-gray-400 uppercase tracking-wider">
                        ${category}
                    </div>
                    <div class="divide-y divide-gray-100 dark:divide-gray-700">
                        ${items.map(item => `
                            <a href="${item.url}" class="block px-4 py-3 hover:bg-gray-50 dark:hover:bg-gray-700/50 transition-colors" onclick="this.parentElement.parentElement.parentElement.querySelector('#search-dropdown').classList.add('hidden');">
                                <div class="font-medium text-gray-900 dark:text-white truncate">${item.title}</div>
                                <div class="mt-1 text-sm text-gray-500 dark:text-gray-400 line-clamp-2">${item.content}</div>
                            </a>
                        `).join('')}
                    </div>
                </div>
            `;
        }
        
        this.searchResults.innerHTML = html;
        
        // Show the dropdown
        if (this.searchDropdown) {
            this.searchDropdown.classList.remove('hidden');
        }
    }
    
    groupByCategory(results) {
        const grouped = {};
        results.forEach(item => {
            if (!grouped[item.category]) {
                grouped[item.category] = [];
            }
            grouped[item.category].push(item);
        });
        return grouped;
    }
    
    displayNoResults() {
        if (!this.searchResults) return;
        
        this.searchResults.innerHTML = `
            <div class="px-4 py-8 text-center">
                <i class="fas fa-search text-3xl text-gray-300 dark:text-gray-600 mb-2"></i>
                <p class="text-gray-500 dark:text-gray-400">No results found</p>
            </div>
        `;
        
        if (this.searchDropdown) {
            this.searchDropdown.classList.remove('hidden');
        }
    }
    
    hideResults() {
        if (this.searchDropdown) {
            this.searchDropdown.classList.add('hidden');
        }
    }
    
    handleKeydown(event) {
        // Handle keyboard navigation if needed
        switch(event.key) {
            case 'Escape':
                this.hideResults();
                break;
            case 'Enter':
                // If we have results, go to the first one
                if (this.searchDropdown && !this.searchDropdown.classList.contains('hidden')) {
                    const firstResult = this.searchDropdown.querySelector('a');
                    if (firstResult) {
                        event.preventDefault();
                        firstResult.click();
                    }
                }
                break;
        }
    }
}

// Initialize global search when DOM is loaded
document.addEventListener('DOMContentLoaded', function() {
    // Initialize if search input exists
    const searchInput = document.querySelector('#global-search-input');
    if (searchInput) {
        window.globalSearch = new GlobalSearch();
    }
});

// Add search functionality to navbar if search icon exists
function initNavbarSearch() {
    const searchIcon = document.querySelector('[data-search-toggle]');
    if (searchIcon) {
        searchIcon.addEventListener('click', function() {
            const searchContainer = document.querySelector('#navbar-search-container');
            if (searchContainer) {
                searchContainer.classList.toggle('hidden');
                if (!searchContainer.classList.contains('hidden')) {
                    const searchInput = searchContainer.querySelector('input');
                    if (searchInput) {
                        setTimeout(() => searchInput.focus(), 100);
                    }
                }
            }
        });
    }
}

document.addEventListener('DOMContentLoaded', initNavbarSearch);