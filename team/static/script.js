
// Function to toggle problem description
function toggleDescription(problemId) {
    const description = document.getElementById(`description-${problemId}`);
    description.style.display = (description.style.display === "none") ? "block" : "none";
}

// Function to toggle solutions visibility
function toggleSolutions(problemId) {
    const solContainer = document.getElementById(`solutions-${problemId}`);
    solContainer.style.display = (solContainer.style.display === "none") ? "block" : "none";
}

// Function to show and hide the post popup
function showPopup() {
    document.getElementById('popup').style.display = 'flex';
}

function closePopup() {
    document.getElementById('popup').style.display = 'none';
}
