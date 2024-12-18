const backendURL = "https://labelbox-as-a-web-app.onrender.com";
let images = [];
let currentIndex = 0;

// Fetch images from the backend
async function fetchImages() {
    const response = await fetch(`${backendURL}/images/`);
    images = await response.json();
    if (images.length > 0) {
        displayImage();
    } else {
        alert("No images available for annotation.");
    }
}

// Display the current image
function displayImage() {
    if (currentIndex < images.length) {
        const imgElement = document.getElementById("image-to-annotate");
        imgElement.src = images[currentIndex].url;
    } else {
        alert("No more images.");
    }
}

// Save annotation to the backend
async function saveAnnotation() {
    const labelInput = document.getElementById("label-input");
    const label = labelInput.value.trim();
    if (!label) {
        alert("Please enter a label.");
        return;
    }

    const annotation = {
        image_id: images[currentIndex]._id,
        label: label,
    };

    const response = await fetch(`${backendURL}/annotations/`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(annotation),
    });

    if (response.ok) {
        alert("Annotation saved!");
        labelInput.value = "";
    } else {
        alert("Failed to save annotation.");
    }
}

// Handle next button click
function nextImage() {
    currentIndex++;
    if (currentIndex < images.length) {
        displayImage();
    } else {
        alert("No more images.");
    }
}

// Attach event listeners
document.getElementById("save-btn").addEventListener("click", saveAnnotation);
document.getElementById("next-btn").addEventListener("click", nextImage);

// Initialize app
fetchImages();
