// JavaScript to rotate images
const images = document.querySelectorAll('.image-container img');
let currentImageIndex = 0;

function rotateImages() {
    images[currentImageIndex].style.opacity = 0;
    currentImageIndex = (currentImageIndex + 1) % images.length;
    images[currentImageIndex].style.opacity = 1;
}

setInterval(rotateImages, 3000); // Change image every 3 seconds