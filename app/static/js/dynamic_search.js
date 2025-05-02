document.addEventListener('DOMContentLoaded', function() {
    const searchInput = document.querySelector('.add-cards-search');
    const cardGrid = document.getElementById('card-grid');

    // Debounced input listener
    searchInput.addEventListener('input', debounce(function() {
        const query = searchInput.value.trim();
        fetchCards(query);
    }, 300));

    // Fetch cards from the Scryfall API
    function fetchCards(query) {
        // Show loading spinner
        cardGrid.innerHTML = `
            <div class="text-center w-100">
                <div class="spinner-border text-light" role="status">
                    <span class="visually-hidden">Loading...</span>
                </div>
            </div>
        `;

        // Empty query? Search all cards (or show message)
        if (!query) {
            cardGrid.innerHTML = '<p class="text-light">Start typing to search cards by name.</p>';
            return;
        }

        const url = `https://api.scryfall.com/cards/search?q=name:${encodeURIComponent(query)}`;

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
