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
  