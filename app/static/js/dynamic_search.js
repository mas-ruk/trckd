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
    let usdToAud = 1.65; // Default fallback exchange rate (USD to AUD)

    // Add a modal for version selection
    createVersionSelectionModal();

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
            // checks original face, if doesn't work (dual-sided cards) will print first face, and if all else fails, placeholder
            const imageUrl = card.image_uris?.normal || card.card_faces?.[0]?.image_uris?.normal || 'https://via.placeholder.com/223x310?text=No+Image';
            const setCode = (card.set || '').toUpperCase();
            const isDoubleFaced = !!card.card_faces?.[1] && card.layout !== 'adventure'; // Improved check for double-faced cards

            const flipButtonHTML = isDoubleFaced
                ? `<button class="card-footer-btn rounded-pill px-4 py-2" id="flip-${card.id}">
                    <i class="bi bi-arrow-repeat"></i> Flip
                </button>`
                : '';

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
            cardElement.className = 'card bg-dark text-light';
            
            // Add metadata as data attributes for filtering
            cardElement.setAttribute('data-color', card.color_identity?.join(',') || 'none');
            cardElement.setAttribute('data-type', card.type_line || 'none');
            cardElement.setAttribute('data-rarity', card.rarity || 'none');

            // Different styles based on view
            if (isGridView) {
                cardElement.classList.add('m-3');
                cardElement.style.width = '18rem';
            }

            cardElement.innerHTML = `
                <img src="${imageUrl}" class="card-img-top" alt="${card.name}" data-flip="0">
                <div class="card-body">
                    <h5 class="card-title">${card.name}</h5>
                    <p class="card-text">${card.set_name || ''} (${setCode}) | <strong>${rarity}</strong></p>
                    <p class="card-text">Price: ${priceText}</p>
                </div>
                <div class="card-footer d-flex flex-wrap justify-content-center gap-2 pt-3">
                    <button class="card-footer-btn rounded-pill px-3 py-2 select-version-btn" 
                        data-card-name="${card.name}" 
                        data-card-id="${card.id}" 
                        data-card-set="${setCode}">
                        <i class="bi bi-plus-lg"></i> Add
                    </button>
                    <button
                        class="card-footer-btn rounded-pill px-3 py-2 open-details-btn"
                        data-bs-toggle="modal"
                        data-bs-target="#detailsPage"
                        data-card-id="${card.id}"
                        data-card-data="${encodeURIComponent(JSON.stringify(card))}">
                        <i class="bi bi-info-circle"></i> Details
                    </button>
                    ${flipButtonHTML}
                </div>
            `;

            cardGrid.appendChild(cardElement);

            if (isDoubleFaced) {
                // get the flip button as a var
                const flipBtn = document.querySelector(`#flip-${card.id}`);
                const imgElement = cardElement.querySelector('img');
                
                let isFlip = false;

                // add animation to image
                imgElement.classList.add('card-flip-animation');

                // check if flip button of item is pressed - event listener
                flipBtn.addEventListener('click', () => {
                    if (isFlip) return;

                    // animation initiate
                    isFlip = true;
                    imgElement.classList.add('flipping');

                    // animation must complete before changing img
                    setTimeout(() => {
                        const img = cardElement.querySelector('img');
                        const currFlip = cardElement.querySelector('img').getAttribute('data-flip');
                        
                        if (currFlip === '0') {
                            // set the image to the other image
                            img.src = card.card_faces[1].image_uris.normal || img.src;

                            // set the value of the data-flip attribute depending on the value of data-flip
                            img.setAttribute('data-flip', '1');

                        } else if (currFlip === '1') {
                            img.src = card.card_faces[0].image_uris.normal || img.src;
                            img.setAttribute('data-flip', '0'); // Change from '1' to '0'
                        }

                        // Remove the flipping class after animation completes
                        setTimeout(() => {
                            imgElement.classList.remove('flipping');
                            isFlip = false;
                        }, 300); // Full animation duration
                    }, 600); 
                });
            }
        });

        // Add event listeners for the Add buttons
        document.querySelectorAll('.select-version-btn').forEach(button => {
            button.addEventListener('click', function() {
                const cardName = this.getAttribute('data-card-name');
                const cardId = this.getAttribute('data-card-id');
                openVersionSelector(cardName, cardId);
            });
        });
    }

    function openVersionSelector(cardName, cardId) {
        const versionModal = document.getElementById('versionSelectorModal');
        const versionModalBody = document.getElementById('version-selector-body');
        const versionModalTitle = document.getElementById('versionModalLabel');
        
        // Update modal title
        versionModalTitle.textContent = `Select Version: ${cardName}`;
        
        // Show loading state
        versionModalBody.innerHTML = `
            <div class="text-center w-100 py-5">
                <div class="spinner-border text-light" role="status">
                    <span class="visually-hidden">Loading versions...</span>
                </div>
            </div>
        `;
        
        // Show the modal
        const versionModalInstance = new bootstrap.Modal(versionModal);
        versionModalInstance.show();
        
        // Add event listeners to close buttons
        const closeButtons = versionModal.querySelectorAll('[data-bs-dismiss="modal"]');
        closeButtons.forEach(button => {
            button.addEventListener('click', () => versionModalInstance.hide());
        });
        
        // Use a more reliable search approach - search by exact name instead of ID
        const encodedName = encodeURIComponent(`!"${cardName}"`);
        fetch(`https://api.scryfall.com/cards/search?q=${encodedName}&unique=prints`)
            .then(response => {
                // Enhanced error handling
                if (!response.ok) {
                    console.error(`Error response: ${response.status} ${response.statusText}`);
                    return response.text().then(text => {
                        console.error(`Error body: ${text}`);
                        throw new Error(`Network response was not ok: ${response.status}`);
                    });
                }
                return response.json();
            })
            .then(data => {
                populateVersionSelector(data.data || [], versionModalBody, versionModalInstance);
            })
            .catch(error => {
                console.error('Error fetching card versions:', error);
                versionModalBody.innerHTML = `
                    <p class="text-danger">Error loading card versions: ${error.message}</p>
                    <p>Please try again or select a different version of this card.</p>
                `;
            });
    }

    function populateVersionSelector(versions, modalBody, modalInstance) {
        if (versions.length === 0) {
            modalBody.innerHTML = '<p class="text-light">No versions found.</p>';
            return;
        }

        // Sort versions by release date (newest first)
        versions.sort((a, b) => {
            return new Date(b.released_at) - new Date(a.released_at);
        });

        modalBody.innerHTML = `
            <div class="row row-cols-1 row-cols-md-3 g-4">
                ${versions.map((version, index) => {
                    const imageUrl = version.image_uris?.small || (version.card_faces && version.card_faces[0].image_uris?.small) || 'https://via.placeholder.com/146x204?text=No+Image';
                    const setCode = (version.set || '').toUpperCase();
                    const rarity = version.rarity
                        ? version.rarity.charAt(0).toUpperCase() + version.rarity.slice(1)
                        : '';
                    
                    // Fetch the USD price
                    const usdPrice = version.prices?.usd;
                    let priceText = 'N/A';

                    // Convert to AUD if USD price is available
                    if (usdPrice) {
                        const audPrice = (usdPrice * usdToAud).toFixed(2);
                        priceText = `A$${audPrice}`;
                    }

                    return `
                        <div class="col">
                            <div class="card bg-dark">
                                <div class="d-flex justify-content-center pt-3">
                                    <img src="${imageUrl}" class="card-img-top" alt="${version.name}" style="width: 146px; height: 204px; object-fit: contain;">
                                </div>
                                <div class="card-body">
                                    <h6 class="card-title">${version.set_name} (${setCode})</h6>
                                    <p class="card-text"><strong>${rarity}</strong></p>
                                    <p class="card-text">Price: ${priceText}</p>
                                    ${version.collector_number ? `<p class="card-text">Collector #: ${version.collector_number}</p>` : ''}
                                    ${version.frame_effects ? `<p class="card-text">Style: ${version.frame_effects.join(', ')}</p>` : ''}
                                </div>
                                <div class="card-footer flex-column align-items-start">
                                    <div class="w-100 mb-3">
                                        <!-- Language Section -->
                                        <label for="language-${index}"> Language:</label>
                                        <select name="language" id="language-${index}">
                                            <option value="english"> English </option>
                                            <option value="french"> French </option>
                                            <option value="german"> German </option>
                                            <option value="spanish"> Spanish </option>
                                            <option value="italian"> Italian </option>
                                        </select>
                                    </div>

                                    <!-- Condition Section -->
                                    <div class="w-100 mb-3">    
                                        <label for="condition-${index}"> Condition:</label>
                                        <select name="condition" id="condition-${index}">
                                            <option value="near-mint"> Near Mint </option>
                                            <option value="lightly-played"> Lightly Played </option>
                                            <option value="moderately-played"> Moderately Played </option>
                                            <option value="heavily-played"> Heavily Played </option>
                                            <option value="damaged"> Damaged </option>
                                        </select>
                                    </div>

                                    <!-- Quantity Section -->
                                    <div class="w-100 mb-3">    
                                        <label for="quantity-${index}"> Quantity:</label>
                                        <input type="number" class="form-control" id="quantity-${index}" min="1" value="1">
                                        <div class="invalid-feedback">
                                            Please enter a quantity greater than 0.
                                        </div>
                                    </div>
                                    
                                    <!-- Foiling Section -->
                                    <div class="form-check mb-3">
                                        <input class="form-check-input" type="checkbox" value="foil" id="foil-${index}">
                                        <label class="form-check-label" for="foil-${index}">Foil</label>
                                    </div>

                                    <button class="details-btn w-100 py-2 rounded-pill mt-2 add-version-btn"
                                        data-card-id="${version.id}"
                                        data-card-name="${version.name}"
                                        data-oracle-text="${getOracleText(version).replace(/"/g,'&quot;')}"
                                        data-set-code="${setCode}"
                                        data-set-name="${version.set_name}"
                                        data-rarity="${rarity}"
                                        data-collector-number="${version.collector_number || ''}"
                                        data-price="${priceText}"
                                        data-image="${imageUrl}"
                                        data-index="${index}">
                                        <i class="bi bi-plus-lg"></i> Add to Collection
                                    </button>
                                </div>
                            </div>
                        </div>
                    `;
                }).join('')}
            </div>
        `;

        // Add event listeners for the version selection buttons
        modalBody.querySelectorAll('.add-version-btn').forEach(button => {
            button.addEventListener('click', function() {
                const index      = this.getAttribute('data-index');
                const language = document.getElementById(`language-${index}`).value;
                const condition = document.getElementById(`condition-${index}`).value;
                const isFoil = document.getElementById(`foil-${index}`).checked;
                const quantityInput = document.getElementById(`quantity-${index}`);
                const quantity = parseInt(quantityInput.value);
                
                // pull the description straight off the button
                const description = this.getAttribute('data-oracle-text') || '';

                // Validate quantity
                if (!quantity || quantity < 1) {
                    quantityInput.classList.add('is-invalid');
                    return;
                } else {
                    quantityInput.classList.remove('is-invalid');
                }

                const cardData = {
                    id: this.getAttribute('data-card-id'),
                    name: this.getAttribute('data-card-name'),
                    setCode: this.getAttribute('data-set-code'),
                    setName: this.getAttribute('data-set-name'),
                    rarity: this.getAttribute('data-rarity'),
                    collectorNumber: this.getAttribute('data-collector-number'),
                    price: this.getAttribute('data-price'),
                    image: this.getAttribute('data-image'),
                    language,
                    condition,
                    foil: isFoil,
                    quantity,
                    oracle_text:    description
                };
                
                addCardToCollection(cardData);
                modalInstance.hide();
            });
        });
    }

    function addCardToCollection(cardData) {
        // Prepare the data in the format expected by the backend
        const cardToAdd = {
            name: cardData.name,
            type: "", // Will be populated from API if needed
            color: "", // Will be populated from API if needed
            rarity: cardData.rarity,
            set_code: cardData.setCode,
            set_name: cardData.setName,
            collector_number: cardData.collectorNumber,
            mana_cost: "", // Will be populated from API if needed
            cmc: null, // Will be populated from API if needed
            type_line: "", // Will be populated from API if needed 
            oracle_text: "", // Will be populated from API if needed
            power: "", // Will be populated from API if needed
            toughness: "", // Will be populated from API if needed
            image_uris: JSON.stringify({normal: cardData.image}),
            color_identity: "", // Will be populated from API if needed
            lang: cardData.language,
            price: cardData.price.replace('A$', '').trim() // Extract the price without currency symbol
        };

        // Get additional card details from Scryfall API
        fetch(`https://api.scryfall.com/cards/${cardData.id}`)
            .then(response => {
                if (!response.ok) throw new Error('Network response was not ok');
                return response.json();
            })
            .then(fullCardData => {
                // Fill in the missing data from the API response
                cardToAdd.type = fullCardData.type_line ? fullCardData.type_line.split('—')[0].trim() : "";
                
                // Handle double-faced cards
                if (fullCardData.card_faces && fullCardData.card_faces.length > 0) {
                    // Get colors from the front face if not present on main card
                    cardToAdd.color = fullCardData.colors ? fullCardData.colors.join('') : 
                                     (fullCardData.card_faces[0].colors ? fullCardData.card_faces[0].colors.join('') : "");
                    
                    // Use front face mana cost if main card doesn't have it
                    cardToAdd.mana_cost = fullCardData.mana_cost || fullCardData.card_faces[0].mana_cost || "";
                    
                    // Store both faces' oracle text
                    const frontText = fullCardData.card_faces[0].oracle_text || "";
                    const backText = fullCardData.card_faces[1].oracle_text || "";
                    cardToAdd.oracle_text = frontText + "\n--\n" + backText;
                    
                    // Store both faces' types if needed
                    cardToAdd.type_line = fullCardData.type_line || fullCardData.card_faces[0].type_line || "";
                } else {
                    // Original code for single-faced cards
                    cardToAdd.color = fullCardData.colors ? fullCardData.colors.join('') : "";
                    cardToAdd.mana_cost = fullCardData.mana_cost || "";
                    cardToAdd.oracle_text = fullCardData.oracle_text || "";
                }
                
                // Common properties for all cards
                cardToAdd.cmc = fullCardData.cmc || 0;
                cardToAdd.power = fullCardData.power || "";
                cardToAdd.toughness = fullCardData.toughness || "";
                cardToAdd.color_identity = fullCardData.color_identity ? fullCardData.color_identity.join('') : "";
                
                // Now send all the data to the backend
                return fetch('/add_card', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify(cardToAdd)
                });
            })
            .then(response => {
                if (!response.ok) {
                    throw new Error('Failed to add card');
                }
                return response.json();
            })
            .then(data => {
                // Show success message
                const quantityText = cardData.quantity > 1 ? `${cardData.quantity}x ` : '';
                showToast(`Added ${quantityText}${cardData.name} (${cardData.setCode}) to your collection!`);
            })
            .catch(error => {
                console.error('Error adding card to collection:', error);
                showToast('Error adding card to collection. Please try again.', 'error');
            });
    }

    function showToast(message, type = 'success') {
        // Create toast container if it doesn't exist
        let toastContainer = document.getElementById('toast-container');
        if (!toastContainer) {
            toastContainer = document.createElement('div');
            toastContainer.id = 'toast-container';
            toastContainer.className = 'position-fixed bottom-0 end-0 p-3';
            document.body.appendChild(toastContainer);
        }

        // Create toast element
        const toastId = `toast-${Date.now()}`;
        const toastEl = document.createElement('div');
        toastEl.id = toastId;
        toastEl.className = `toast align-items-center text-white bg-${type === 'success' ? 'success' : 'danger'} border-0`;
        toastEl.setAttribute('role', 'alert');
        toastEl.setAttribute('aria-live', 'assertive');
        toastEl.setAttribute('aria-atomic', 'true');

        toastEl.innerHTML = `
            <div class="d-flex">
                <div class="toast-body">
                    ${message}
                </div>
                <button type="button" class="btn-close btn-close-white me-2 m-auto" data-bs-dismiss="toast" aria-label="Close"></button>
            </div>
        `;

        // Add toast to container
        toastContainer.appendChild(toastEl);

        // Initialize and show toast
        const toast = new bootstrap.Toast(toastEl, { autohide: true, delay: 3000 });
        toast.show();

        // Remove toast after it's hidden
        toastEl.addEventListener('hidden.bs.toast', function() {
            toastEl.remove();
        });
    }

    function createVersionSelectionModal() {
        // Create modal element if it doesn't exist
        if (!document.getElementById('versionSelectorModal')) {
            const modalEl = document.createElement('div');
            modalEl.className = 'modal fade';
            modalEl.id = 'versionSelectorModal';
            modalEl.tabIndex = '-1';
            modalEl.setAttribute('aria-labelledby', 'versionModalLabel');
            modalEl.setAttribute('aria-hidden', 'true');

            modalEl.innerHTML = `
                <div class="modal-dialog modal-xl">
                    <div class="modal-content bg-dark text-light">
                        <div class="modal-header">
                            <h5 class="modal-title" id="versionModalLabel">Select Version</h5>
                            <button type="button" class="btn-close btn-close-white" data-bs-dismiss="modal" aria-label="Close"></button>
                        </div>
                        <div class="modal-body" id="version-selector-body">
                            <!-- Content will be loaded dynamically -->
                        </div>
                        <div class="modal-footer">
                            <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Cancel</button>
                        </div>
                    </div>
                </div>
            `;

            document.body.appendChild(modalEl);
        }
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

    // Handle modal opening and content loading for details modal
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
                        
                        <div class="d-flex justify-content-between mb-3">
                            <span class="text-light">Set: ${card.set_name} (${card.set.toUpperCase()})</span>
                        </div>
                        
                        <p class="text-light">Price: ${priceText}</p>
                        
                        ${legalityHtml}
                        
                        <div class="mt-4 d-flex gap-3 flex-wrap">
                            <button class="details-btn rounded-pill px-4 py-2 select-version-btn"
                                data-card-name="${card.name}" 
                                data-card-id="${card.id}">
                                <i class="bi bi-plus-lg"></i> Add to Collection
                            </button>
                            <a href="${card.scryfall_uri}" target="_blank" class="details-btn rounded-pill px-4 py-2">
                                <i class="bi bi-link"></i> View on Scryfall
                            </a>
                        </div>
                    </div>
                </div>
            </div>
        `;

        // Add event listener for the Add to Collection button in details modal
        modalBody.querySelector('.select-version-btn').addEventListener('click', function() {
            const cardName = this.getAttribute('data-card-name');
            const cardId = this.getAttribute('data-card-id');
            openVersionSelector(cardName, cardId);
        });
    }
});

// Add this function to your code
function getOracleText(card) {
    // If the card has oracle text directly, use it
    if (card.oracle_text) {
        return card.oracle_text;
    }
    
    // For double-faced cards, combine the oracle text from both faces
    if (card.card_faces && card.card_faces.length > 0) {
        let combinedText = '';
        
        // Add front face text if available
        if (card.card_faces[0] && card.card_faces[0].oracle_text) {
            combinedText += card.card_faces[0].oracle_text;
        }
        
        // Add separator if we're going to add back face text
        if (card.card_faces[1] && card.card_faces[1].oracle_text) {
            if (combinedText) {
                combinedText += '\n--\n';
            }
            combinedText += card.card_faces[1].oracle_text;
        }
        
        return combinedText;
    }
    
    // If no oracle text is found, return empty string
    return '';
}