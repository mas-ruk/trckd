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
            let priceText = 'N/A';

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
                        data-card-id="${card.id}"
                        data-card-data="${encodeURIComponent(JSON.stringify(card))}">
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

    // Handle modal opening and content loading
    document.addEventListener('click', function(event) {
        const detailsButton = event.target.closest('.open-details-btn');
        if (!detailsButton) return;

        // Get the card ID from the data attribute
        const cardId = detailsButton.getAttribute('data-card-id');
        
        // Try to get the card data from the data attribute first
        let cardData = null;
        try {
            const encodedCardData = detailsButton.getAttribute('data-card-data');
            if (encodedCardData) {
                cardData = JSON.parse(decodeURIComponent(encodedCardData));
            }
        } catch (error) {
            console.error('Error parsing card data:', error);
        }

        // If we have the card data, show it immediately
        if (cardData) {
            showCardDetails(cardData);
        } else {
            // Otherwise fetch it from the API
            fetchCardDetails(cardId);
        }
    });

    function fetchCardDetails(cardId) {
        const modalBody = document.getElementById("details-modal-body");
        
        // Show loading state
        modalBody.innerHTML = `
            <div class="text-center w-100 py-5">
                <div class="spinner-border text-light" role="status">
                    <span class="visually-hidden">Loading card details...</span>
                </div>
            </div>
        `;

        // Fetch the card details from Scryfall API
        fetch(`https://api.scryfall.com/cards/${cardId}`)
            .then(response => {
                if (!response.ok) throw new Error('Network response was not ok');
                return response.json();
            })
            .then(card => {
                showCardDetails(card);
            })
            .catch(error => {
                console.error('Error fetching card details:', error);
                modalBody.innerHTML = '<p class="text-danger">Error loading card details. Please try again.</p>';
            });
    }

    function showCardDetails(card) {
        const modalBody = document.getElementById("details-modal-body");
        
        // Get image URL (handle double-faced cards)
        let imageUrl = 'https://via.placeholder.com/223x310?text=No+Image';
        let backImageHtml = '';
        
        if (card.image_uris && card.image_uris.normal) {
            imageUrl = card.image_uris.normal;
        } else if (card.card_faces && card.card_faces[0].image_uris) {
            // For double-faced cards
            imageUrl = card.card_faces[0].image_uris.normal;
            
            if (card.card_faces[1].image_uris) {
                backImageHtml = `
                    <div class="mt-3">
                        <h6 class="text-light">Back Face:</h6>
                        <img src="${card.card_faces[1].image_uris.normal}" class="img-fluid rounded" alt="${card.card_faces[1].name}">
                    </div>
                `;
            }
        }

        // Calculate price in AUD
        const usdPrice = card.prices?.usd;
        let priceText = 'N/A';

        if (usdPrice) {
            const audPrice = (usdPrice * usdToAud).toFixed(2);
            priceText = `A$${audPrice} (US$${usdPrice})`;
        }

        // Format legality information
        let legalityHtml = '';
        if (card.legalities) {
            const formats = ['standard', 'modern', 'commander', 'legacy', 'vintage'];
            legalityHtml = '<div class="mt-3"><h6>Legality:</h6><ul class="list-group">';
            
            formats.forEach(format => {
                const status = card.legalities[format];
                const statusClass = status === 'legal' ? 'text-success' : 'text-danger';
                
                legalityHtml += `
                    <li class="list-group-item bg-dark text-light border-secondary">
                        ${format.charAt(0).toUpperCase() + format.slice(1)}: 
                        <span class="${statusClass}">${status.charAt(0).toUpperCase() + status.slice(1)}</span>
                    </li>
                `;
            });
            
            legalityHtml += '</ul></div>';
        }

        // Format mana cost and type line
        const manaCost = card.mana_cost || '';
        const typeLine = card.type_line || '';
        
        // Create card text content
        let cardText = '';
        if (card.oracle_text) {
            cardText = `<div class="card bg-dark border-secondary mt-3">
                <div class="card-body">
                    <p class="card-text">${card.oracle_text.replace(/\n/g, '<br>')}</p>
                </div>
            </div>`;
        }

        // Populate the modal with card details
        modalBody.innerHTML = `
            <div class="container-fluid">
                <div class="row">
                    <!-- Card Image Pane -->
                    <div class="col-md-5">
                        <img src="${imageUrl}" class="img-fluid rounded" alt="${card.name}">
                        ${backImageHtml}
                    </div>
                    
                    <!-- Details Pane -->
                    <div class="col-md-7">
                        <h3 style="font-weight: bold;" class="text-light">${card.name}</h3>
                        <p class="text-light">${manaCost}</p>
                        <p class="text-light">${typeLine}</p>
                        
                        <div class="d-flex justify-content-between mb-3">
                            <span class="text-light">Set: ${card.set_name} (${card.set.toUpperCase()})</span>
                            <span class="text-light">Rarity: ${card.rarity.charAt(0).toUpperCase() + card.rarity.slice(1)}</span>
                        </div>
                        
                        <p class="text-light">Price: ${priceText}</p>
                        
                        ${cardText}
                        
                        ${legalityHtml}
                        
                        <div class="mt-4">
                            <button class="btn btn-primary" id="add-to-collection-${card.id}">
                                <i class="bi bi-plus-lg"></i> Add to Collection
                            </button>
                            <a href="${card.scryfall_uri}" target="_blank" class="btn btn-secondary ms-2">
                                <i class="bi bi-link"></i> View on Scryfall
                            </a>
                        </div>
                    </div>
                </div>
            </div>
        `;
    }
});