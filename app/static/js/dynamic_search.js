// app\static\js\dynamic_search.js

document.addEventListener('DOMContentLoaded', function() {
    // Initialize elements
    const searchInput = document.querySelector('.add-cards-search');
    const cardGrid = document.getElementById('card-grid');
    const filterButton = document.querySelector('.filter-button');
    const filterDropdown = document.getElementById('filter-dropdown');
    const clearFiltersButton = document.getElementById('clear-filters-btn');
    const toggleViewBtn = document.getElementById('toggleViewBtn');
    
    // Track current view state (default: grid view)
    let isGridView = true;
    
    // Track active filters
    let activeFilters = [];
    
    // Toggle filter dropdown visibility
    if (filterButton && filterDropdown) {
        filterButton.addEventListener('click', function() {
            filterDropdown.style.display = filterDropdown.style.display === 'block' ? 'none' : 'block';
        });
    }
    
    // Handle filter option selection
    document.querySelectorAll('.filter-option').forEach(option => {
        option.addEventListener('click', function() {
            const filter = option.getAttribute('data-filter');
            
            if (option.classList.contains('selected')) {
                option.classList.remove('selected');
                activeFilters = activeFilters.filter(f => f !== filter);
            } else {
                option.classList.add('selected');
                if (!activeFilters.includes(filter)) {
                    activeFilters.push(filter);
                }
            }
            
            fetchCards();
        });
    });
    
    // Clear filters
    if (clearFiltersButton) {
        clearFiltersButton.addEventListener('click', function() {
            activeFilters = [];
            document.querySelectorAll('.filter-option.selected').forEach(opt => opt.classList.remove('selected'));
            fetchCards();
        });
    }
    
    // Debounced input listener for search bar
    if (searchInput) {
        searchInput.addEventListener('input', debounce(fetchCards, 300));
    }
    
    // Toggle view functionality
    if (toggleViewBtn) {
        toggleViewBtn.addEventListener('click', function() {
            isGridView = !isGridView;
            
            if (isGridView) {
                cardGrid.classList.remove('list-view');
                cardGrid.classList.add('grid-view');
                toggleViewBtn.innerHTML = '<i class="bi bi-list"></i> List View / <i class="bi bi-grid"></i> Grid View';
            } else {
                cardGrid.classList.remove('grid-view'); 
                cardGrid.classList.add('list-view');
                toggleViewBtn.innerHTML = '<i class="bi bi-grid"></i> Grid View / <i class="bi bi-list"></i> List View';
            }
            
            // If we have cards displayed, refresh the view without re-fetching
            const cards = cardGrid.querySelectorAll('.card');
            if (cards.length > 0 && !cardGrid.querySelector('.spinner-border')) {
                updateCardDisplay();
            }
        });
    }

    function fetchCards() {
        let query = searchInput.value.trim();

        // Wrap multi-word search in quotes
        if (query.includes(' ')) {
            query = `"${query}"`;
        }

        let filters = activeFilters.join(' ');
        let searchQuery = query ? `name:${query}` : '';

        // If both are empty, show default message and return
        if (!query && activeFilters.length === 0) {
            cardGrid.innerHTML = '<p class="text-light">Start typing to search for Magic cards.</p>';
            return;
        }

        // Combine query + filters
        if (filters) {
            searchQuery += ` ${filters}`;
        }

        // Show loading spinner
        cardGrid.innerHTML = `
            <div class="text-center w-100">
                <div class="spinner-border text-light" role="status">
                    <span class="visually-hidden">Loading...</span>
                </div>
            </div>
        `;

        const url = `https://api.scryfall.com/cards/search?q=${encodeURIComponent(searchQuery.trim())}`;

        fetch(url)
            .then(response => {
                if (!response.ok) throw new Error('Network response was not ok');
                return response.json();
            })
            .then(data => {
                updateCardGrid(data.data || []);
            })
            .catch(error => {
                console.error('Error fetching search results:', error);
                cardGrid.innerHTML = '<p class="text-danger">Error loading cards. Please try again.</p>';
            });
    }

    function updateCardGrid(cards) {
        cardGrid.innerHTML = '';

        if (cards.length === 0) {
            cardGrid.innerHTML = '<p class="text-light">No cards found.</p>';
            return;
        }
        
        // Apply current view class
        cardGrid.classList.add(isGridView ? 'grid-view' : 'list-view');

        cards.forEach(card => {
            const imageUrl = card.image_uris?.normal || 'https://via.placeholder.com/223x310?text=No+Image';
            const setCode = (card.set || '').toUpperCase();
            const rarity = card.rarity
                ? card.rarity.charAt(0).toUpperCase() + card.rarity.slice(1)
                : '';

            const cardElement = document.createElement('div');
            cardElement.className = 'card bg-dark text-light';
            
            // Different styles based on view
            if (isGridView) {
                cardElement.classList.add('m-3');
                cardElement.style.width = '18rem';
            }

            cardElement.innerHTML = `
                <img src="${imageUrl}" class="card-img-top" alt="${card.name}">
                <div class="card-body">
                    <h5 class="card-title">${card.name}</h5>
                    <p class="card-text">${card.set_name || ''} (${setCode}) | <strong>${rarity}</strong></p>
                </div>
                <div class="card-footer d-flex justify-content-between pt-3">
                    <button class="card-footer-btn rounded-pill px-4 py-2" id="add-${card.id}">
                        <i class="bi bi-plus-lg"></i> Add
                    </button>
                    <button class="card-footer-btn rounded-pill px-4 py-2" id="details-${card.id}">
                        <i class="bi bi-info-circle"></i> Details
                    </button>
                </div>
            `;

            cardGrid.appendChild(cardElement);
        });
    }
    
    // Function to update display without re-fetching cards
    function updateCardDisplay() {
        const cards = Array.from(cardGrid.querySelectorAll('.card'));
        
        cards.forEach(card => {
            if (isGridView) {
                card.classList.add('m-3');
                card.style.width = '18rem';
            } else {
                card.classList.remove('m-3');
                card.style.width = 'auto';
            }
        });
    }

    function debounce(func, wait) {
        let timeout;
        return function(...args) {
            clearTimeout(timeout);
            timeout = setTimeout(() => func.apply(this, args), wait);
        };
    }

    // Initial message
    cardGrid.innerHTML = '<p class="text-light">Start typing to search for Magic cards.</p>';
});
