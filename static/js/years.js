/* Need to fix bug that is 
apparent when all years is selected and submitted. Submits as empty. 
*/

let answers = [];
let lastSelectedIndex = -1; // Track the last selected button index
let shiftPressed = false; // Track if the Shift key is pressed
let isGreen = false; // Track AllHist button state

const year_buttons = document.querySelectorAll(".twosec_font_fade");
const years_list = document.getElementById("hiddenInput");
const AllHist = document.getElementById("AllHist");
const submit = document.getElementById("submitBtn2");
const form = document.getElementById("yearForm");
const body = document.querySelector("body");
const span = document.getElementById("subSpan");

// Add event listeners for the shift key
document.addEventListener("keydown", (event) => {
    if (event.key === "Shift") {
        shiftPressed = true; // Shift key is pressed
    }
});

document.addEventListener("keyup", (event) => {
    if (event.key === "Shift") {
        shiftPressed = false; // Shift key is released
    }
});

// Add click event listeners to year buttons
year_buttons.forEach((button, index) => {
    button.addEventListener("click", function (event) {
        const v = event.target.value;

        // Toggle active class based on the button state
        if (answers.includes(v)) {
            button.classList.remove('active'); // Remove active class
            answers = answers.filter((item) => item !== v); // Remove from answers
        } else {
            button.classList.add('active'); // Add active class
            answers.push(v); // Add to answers only if it's not already present
        }

        // Handle Shift key for multi-selection
        if (shiftPressed && lastSelectedIndex !== -1) {
            const start = Math.min(lastSelectedIndex, index);
            const end = Math.max(lastSelectedIndex, index);
            for (let i = start; i <= end; i++) {
                const yearValue = year_buttons[i].value;
                if (!answers.includes(yearValue)) { // Check for duplicates
                    year_buttons[i].classList.add('active'); // Select all buttons between
                    answers.push(yearValue); // Add to answers if not included
                }
            }
        }

        // Check if all year buttons are selected
        if (answers.length === year_buttons.length) {
            AllHist.classList.add('active'); // Set AllHist to selected
            isGreen = true; // Mark AllHist as selected
        } else {
            AllHist.classList.remove('active'); // Reset AllHist button
            isGreen = false; // Mark AllHist as not selected
        }

        lastSelectedIndex = index; // Update last selected index
    });
});

// Click event listener for outside clicks
body.addEventListener("click", function (event) {
    // Check if the click is outside the buttons, AllHist, and submit button
    if (
        !event.target.classList.contains("twosec_font_fade") &&
        event.target !== AllHist &&
        event.target !== span &&
        event.target !== submit
    ) {
        year_buttons.forEach((button) => {
            button.classList.remove('active'); // Reset all buttons
        });
        AllHist.classList.remove('active'); // Reset AllHist button
        isGreen = false; // Reset isGreen state
        answers = []; // Clear answers
        lastSelectedIndex = -1; // Reset last selected index
    }
});

// AllHist button event listener
AllHist.addEventListener("click", function (event) {
    event.stopPropagation();

    if (isGreen) {
        answers = [];
        year_buttons.forEach((button) => {
            button.classList.remove('active'); // Reset all buttons
        });
        AllHist.classList.remove('active'); // Reset AllHist button
    } else {
        year_buttons.forEach((button) => {
            button.classList.add('active'); // Set all to selected
            answers.push(button.value); // Add all years to answers
        });
        AllHist.classList.add('active'); // Set AllHist to selected
    }
    isGreen = !isGreen; // Toggle isGreen state
    console.log(answers);
});

// Function to update hiddenInput value based on answers array
function updateHiddenInput() {
    years_list.value = answers.join(",");
}

// Submit the form
form.addEventListener("submit", function (event) {
    event.preventDefault(); // Prevent default submission
    updateHiddenInput(); // Update hidden input with answers

    if (answers.length < 1) {
        alert("Please choose at least one year to view.");
    } else {
        form.submit(); // Submit the form
    }
});
