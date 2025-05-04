// app\static\js\dynamic_search.js

document.addEventListener('DOMContentLoaded', function() {
    const searchInput = document.querySelector('.add-cards-search');
    const cardGrid = document.getElementById('card-grid');
    const filterDropdown = document.getElementById('filter-dropdown');
    const filterButton = document.querySelector('.filter-button');
    const clearFiltersButton = document.getElementById('clear-filters-btn');
    
    let activeFilters = [];

    // Toggle filter dropdown visibility
    filterButton.addEventListener('click', function() {
        filterDropdown.style.display = filterDropdown.style.display === 'block' ? 'none' : 'block';
    });

    // Handle filter option selection
    document.querySelectorAll('.filter-option').forEach(option => {
        option.addEventListener('click', function() {
            const filter = option.getAttribute('data-filter');
    
            // Toggle 'selected' class
            option.classList.toggle('selected');
    
            // Toggle filter in activeFilters array
            const index = activeFilters.indexOf(filter);
            if (index > -1) {
                activeFilters.splice(index, 1); // Remove filter
            } else {
                activeFilters.push(filter); // Add filter
            }
    
            fetchCards();
        });
    });
    

    // Clear filters
    clearFiltersButton.addEventListener('click', function() {
        activeFilters = [];
    
        // Clear all visual highlights
        document.querySelectorAll('.filter-option').forEach(option => {
            option.classList.remove('selected');
        });
    
        fetchCards(); // Refresh the card grid with no filters
    });
    

    // Debounced input listener for search bar
    searchInput.addEventListener('input', debounce(function() {
        fetchCards();
    }, 300));

    // Fetch cards with search query and active filters
    function fetchCards() {
        const query = searchInput.value.trim();
        
        let filters = activeFilters.join(' ');
        let searchQuery = query ? `name:${encodeURIComponent(query)}` : '';
        
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

        const url = `https://api.scryfall.com/cards/search?q=${encodeURIComponent(searchQuery)}`;

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

    // Render cards into the DOM
    function updateCardGrid(cards) {
        cardGrid.innerHTML = '';

        if (cards.length === 0) {
            cardGrid.innerHTML = '<p class="text-light">No cards found.</p>';
            return;
        }

        cards.forEach(card => {
            const imageUrl = card.image_uris?.normal || 'https://via.placeholder.com/223x310?text=No+Image';

            // format set code to uppercase
            const setCode = (card.set || '').toUpperCase();
            
            // Capitalize rarity
            const rarity = card.rarity
            ? card.rarity.charAt(0).toUpperCase() + card.rarity.slice(1)
            : '';

            const cardElement = document.createElement('div');
            cardElement.className = 'card bg-dark text-light m-3';
            cardElement.style.width = '18rem';

            cardElement.innerHTML = `
                <img src="${imageUrl}" class="card-img-top" alt="${card.name}">
                <div class="card-body">
                    <h5 class="card-title">${card.name}</h5>
                    <p class="card-text">${card.set_name || ''} (${setCode}) | <strong>${rarity}</strong></p>
                </div>
                <!-- Footer with buttons -->
                <div class="card-footer d-flex justify-content-between pt-3">
                    <button class="card-footer-btn rounded-pill px-4 py-2" id="add-${card.id}"><i class="bi bi-plus-lg"></i> Add</button>
                    <button class="card-footer-btn rounded-pill px-4 py-2" id="details-${card.id}"><i class="bi bi-info-circle"></i> Details</button>
                </div>
            `;

            cardGrid.appendChild(cardElement);
        });
    }

    // Debounce helper
    function debounce(func, wait) {
        let timeout;
        return function(...args) {
            clearTimeout(timeout);
            timeout = setTimeout(() => func.apply(this, args), wait);
        };
    }

    cardGrid.innerHTML = '<p class="text-light">Start typing to search for Magic cards.</p>';
});
