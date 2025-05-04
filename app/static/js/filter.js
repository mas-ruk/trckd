// app\static\js\filter.js

document.addEventListener("DOMContentLoaded", function () {
    const toggleBtn = document.getElementById("filterToggle");
    const popup = document.getElementById("filterPopup");
    const filterOptions = document.querySelectorAll(".filter-option");

    // Toggle the dropdown visibility on button click
    toggleBtn.addEventListener("click", function () {
        popup.classList.toggle("show");
    });

    // Close the dropdown if clicked outside
    document.addEventListener("click", function (e) {
        if (!popup.contains(e.target) && !toggleBtn.contains(e.target)) {
            popup.classList.remove("show");
        }
    });
});
