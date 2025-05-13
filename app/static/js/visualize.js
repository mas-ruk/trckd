document.addEventListener("DOMContentLoaded", function () {
    // === SLIDER FUNCTIONALITY ===
    const slider = document.getElementById("cardSlider");
    const leftBtn = document.querySelector(".slide-btn.left");
    const rightBtn = document.querySelector(".slide-btn.right");

    leftBtn.addEventListener("click", () => {
        slider.scrollBy({ left: -220, behavior: 'smooth' });
    });

    rightBtn.addEventListener("click", () => {
        slider.scrollBy({ left: 220, behavior: 'smooth' });
    });

    // === FORM SUBMIT FOR COLLECTION CREATION ===
    const form = document.getElementById("createCollectionForm");
    form.addEventListener("submit", (e) => {
        e.preventDefault();
        const name = document.getElementById("collectionName").value.trim();
        const desc = document.getElementById("collectionDescription").value.trim();

        if (name === "" || desc === "") {
            alert("Please fill in all fields.");
        } else {
            alert("Collection created successfully!");
        }
    });

    // === FILTERING FUNCTIONALITY ===
    const searchBox = document.getElementById("searchBox");
    const typeFilter = document.getElementById("typeFilter");
    const colorFilter = document.getElementById("colorFilter");
    const rarityFilter = document.getElementById("rarityFilter");
    const applyBtn = document.getElementById("applyFilters");
    const resetBtn = document.getElementById("resetFilters"); // Add the reset button element
    const cards = document.querySelectorAll(".card");

    function filterCards() {
        const searchValue = searchBox.value.toLowerCase();
        const selectedType = typeFilter.value.toLowerCase();
        const selectedColor = colorFilter.value.toLowerCase();
        const selectedRarity = rarityFilter.value.toLowerCase();

        cards.forEach(card => {
            const name = card.getAttribute("data-name");
            const type = card.getAttribute("data-type");
            const color = card.getAttribute("data-color");
            const rarity = card.getAttribute("data-rarity");

            const matchesSearch = name.includes(searchValue);
            const matchesType = !selectedType || type.includes(selectedType);
            const matchesColor = !selectedColor || color.includes(selectedColor);
            const matchesRarity = !selectedRarity || rarity.includes(selectedRarity);

            if (matchesSearch && matchesType && matchesColor && matchesRarity) {
                card.style.display = "block";
            } else {
                card.style.display = "none";
            }
        });
    }

    // Apply filters on click and input change
    applyBtn.addEventListener("click", filterCards);
    searchBox.addEventListener("input", filterCards);
    typeFilter.addEventListener("change", filterCards);
    colorFilter.addEventListener("change", filterCards);
    rarityFilter.addEventListener("change", filterCards);

    // === RESET FILTERS FUNCTIONALITY ===
    resetBtn.addEventListener("click", () => {
        searchBox.value = "";
        typeFilter.value = "";
        colorFilter.value = "";
        rarityFilter.value = "";

        // Shows all cards after resetting the filters
        cards.forEach(card => {
            card.style.display = "block";
        });
    });

    // === CHART FUNCTIONALITY ===
    const chartCanvas = document.getElementById('chartCanvas').getContext('2d');

    // Fetch collection stats for chart rendering (dummy data here, update from backend)
    const rarityData = {
        "Common": 5,
        "Rare": 3,
        "Famous": 2
    };

    const chartData = {
        labels: Object.keys(rarityData),
        datasets: [{
            label: 'Rarity Distribution',
            data: Object.values(rarityData),
            backgroundColor: ['#FF6384', '#36A2EB', '#FFCE56'],
            borderColor: ['#FF6384', '#36A2EB', '#FFCE56'],
            borderWidth: 1
        }]
    };

    // Create chart
    const myChart = new Chart(chartCanvas, {
        type: 'pie', 
        data: chartData,
        options: {
            responsive: true,
            plugins: {
                legend: {
                    position: 'top',
                },
                tooltip: {
                    callbacks: {
                        label: function(tooltipItem) {
                            return tooltipItem.label + ': ' + tooltipItem.raw + ' cards';
                        }
                    }
                }
            }
        }
    });

});



  