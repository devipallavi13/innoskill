document.addEventListener("DOMContentLoaded", () => {
    const skillFinderRadio = document.getElementById("skill-finder");
    const problemSolverRadio = document.getElementById("problem-solver");
    const skillSection = document.getElementById("skill-section");

    // Toggle skill section visibility
    skillFinderRadio.addEventListener("change", () => {
        skillSection.classList.remove("hidden");
    });

    problemSolverRadio.addEventListener("change", () => {
        skillSection.classList.add("hidden");
    });
});

function addSkill() {
    const skillList = document.getElementById("skill-list");

    const skillDiv = document.createElement("div");
    skillDiv.classList.add("skill-item");

    const skillInput = document.createElement("input");
    skillInput.type = "text";
    skillInput.placeholder = "Enter skill";
    skillInput.classList.add("skill-input");

    const ratingInput = document.createElement("input");
    ratingInput.type = "number";
    ratingInput.placeholder = "Rating (1-5)";
    ratingInput.classList.add("rating-input");
    ratingInput.min = 1;
    ratingInput.max = 5;

    skillDiv.appendChild(skillInput);
    skillDiv.appendChild(ratingInput);

    skillList.appendChild(skillDiv);
}
