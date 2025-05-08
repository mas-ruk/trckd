// app\static\js\dynamic_search.js

document.addEventListener('DOMContentLoaded', function() {
    const searchInput = document.querySelector('.add-cards-search');
    const cardGrid = document.getElementById('card-grid');
    const filterButton = document.querySelector('.filter-button');
    const filterDropdown = document.getElementById('filter-dropdown');
    const clearFiltersButton = document.getElementById('clear-filters-btn');

    let activeFilters = [];
    let usdToAud = 1.65; // Default fallback exchange rate (USD to AUD)

    // Fetch real-time exchange rate from USD to AUD using Exchangerate-API
    fetch('https://v6.exchangerate-api.com/v6/YOUR-API-KEY/latest/USD')
        .then(res => res.json())
        .then(data => {
            if (data.result === "success") {
                usdToAud = data.rates.AUD; // Update the exchange rate if the API call is successful
            } else {
                console.error('Error fetching exchange rate');
            }
        })
        .catch(err => console.error('Failed to load exchange rate:', err));

    // Toggle filter dropdown visibility
    filterButton.addEventListener('click', function() {
        filterDropdown.style.display = filterDropdown.style.display === 'block' ? 'none' : 'block';
    });

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
    clearFiltersButton.addEventListener('click', function() {
        activeFilters = [];
        document.querySelectorAll('.filter-option.selected').forEach(opt => opt.classList.remove('selected'));
        fetchCards();
    });

    // Debounced input listener for search bar
    searchInput.addEventListener('input', debounce(fetchCards, 300));

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

        cards.forEach(card => {
            const imageUrl = card.image_uris?.normal || 'https://via.placeholder.com/223x310?text=No+Image';
            const setCode = (card.set || '').toUpperCase();
            const rarity = card.rarity
                ? card.rarity.charAt(0).toUpperCase() + card.rarity.slice(1)
                : '';
            
            // Fetch the USD price
            const usdPrice = card.prices?.usd;
            let priceText = 'Price data not available';

            // Convert to AUD if USD price is available
            if (usdPrice) {
                const audPrice = (usdPrice * usdToAud).toFixed(2);
                priceText = `A$${audPrice}`;
            }

            const cardElement = document.createElement('div');
            cardElement.className = 'card bg-dark text-light m-3';
            cardElement.style.width = '18rem';

            cardElement.innerHTML = `
                <img src="${imageUrl}" class="card-img-top" alt="${card.name}">
                <div class="card-body">
                    <h5 class="card-title">${card.name}</h5>
                    <p class="card-text">${card.set_name || ''} (${setCode}) | <strong>${rarity}</strong></p>
                    <p class="card-text">Price: ${priceText}</p>
                </div>
                <div class="card-footer d-flex justify-content-between pt-3">
                    <button class="card-footer-btn rounded-pill px-4 py-2" id="add-${card.id}">
                        <i class="bi bi-plus-lg"></i> Add
                    </button>
                    <button
                        class="card-footer-btn rounded-pill px-4 py-2 open-details-btn"
                        data-bs-toggle="modal"
                        data-bs-target="#detailsPage"
                        data-card-id="${card.id}">
                        <i class="bi bi-info-circle"></i> Details
                    </button>
                </div>
            `;

            cardGrid.appendChild(cardElement);
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

    // Details Button Listener
    document.addEventListener('click', function (event) {
        const detailsButton = event.target.closest('.open-details-btn');
        if (!detailsButton) return;
    
        // Get the card ID from the data attribute
        const cardId = detailsButton.getAttribute('data-card-id');
        
        // Dynamically populate the modal content if needed (optional)
        const modalBody = document.getElementById("details-modal-body");
        modalBody.innerHTML = `<p>Details for card with ID: ${cardId}</p>`; // You can fetch more card details here
    
        // Find and show the modal
        const modal = new bootstrap.Modal(document.getElementById("detailsPage"));
        modal.show();
    });

    // On Modal Cancel
    const modalElement = document.getElementById('detailsPage');
    const modal = new bootstrap.Modal(modalElement);

    // Listen for the modal's 'hidden' event
    modalElement.addEventListener('hidden.bs.modal', function () {
        // This will ensure the backdrop is removed when the modal is closed
        document.body.classList.remove('modal-open');
        document.querySelector('.modal-backdrop').remove();
    });

    // You can also add your existing logic for opening the modal
    document.querySelectorAll('.open-details-btn').forEach(button => {
        button.addEventListener('click', function (event) {
            modal.show();
        });
    });
    
});
