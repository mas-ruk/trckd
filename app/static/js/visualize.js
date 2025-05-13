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
            // Optionally: you could submit the form via AJAX or un-comment the line below
            // form.submit();
        }
    });

    // === FILTERING FUNCTIONALITY ===
    const searchBox = document.getElementById("searchBox");
    const typeFilter = document.getElementById("typeFilter");
    const colorFilter = document.getElementById("colorFilter");
    const rarityFilter = document.getElementById("rarityFilter");
    const applyBtn = document.getElementById("applyFilters");
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

    applyBtn.addEventListener("click", filterCards);
    searchBox.addEventListener("input", filterCards); // optional: live search
});


  