// background.js

// Function to set the background image dynamically
function setBackgroundImage() {
    const backgroundContainer = document.getElementById("background-image");
    const imageUrl = 'https://source.unsplash.com/1920x1080/?movie'; // Change the URL as needed
    backgroundContainer.style.backgroundImage = `url(${https://unsplash.com/s/photos/movies})`;
}

// Call the function when the page loads
window.addEventListener('load', setBackgroundImage);
