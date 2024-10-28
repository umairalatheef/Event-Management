let currentSlide = 0;
const slides = document.querySelectorAll('.slide');

function nextSlide() {
    currentSlide = (currentSlide + 1) % slides.length;
    slides.forEach((slide, index) => {
        slide.style.transform = `translateX(-${currentSlide * 100}%)`;
    });
}

setInterval(nextSlide, 3000); // Change every 3 seconds

