document.addEventListener("DOMContentLoaded", function () {
    const slider = document.getElementById("cardSlider");
    const leftBtn = document.querySelector(".slide-btn.left");
    const rightBtn = document.querySelector(".slide-btn.right");
  
    leftBtn.addEventListener("click", () => {
      slider.scrollBy({ left: -220, behavior: 'smooth' });
    });
  
    rightBtn.addEventListener("click", () => {
      slider.scrollBy({ left:220, behavior: 'smooth' });
    });
  });

  document.addEventListener("DOMContentLoaded", () => {
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
});

  