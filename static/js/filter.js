// Hidden selection input that we will extract value from
const selectionInput = document.getElementById("selectionInput");
// Div that is initially hidden that will show loading message
const loadingScreen = document.getElementById("loading-screen");
// Div that shows the filter options that will hide
const filterDiv = document.getElementById("filterForm");
const submit = document.getElementById("submitBtn2");
const body = document.querySelector("body");
const goBack = document.getElementById("go_back_container");

selectionInput.value = "";

// Add click event listeners to each button
document.querySelectorAll(".filter_button").forEach((button) => {
  button.addEventListener("click", function () {
    const selectionValue = this.value; // Get the button's value directly
    selectionInput.value = selectionValue; // Set the hidden input value
    console.log("Selected Value: ", selectionInput.value); // Log the selected value

    // Remove 'active' class from all buttons
    document.querySelectorAll(".filter_button").forEach((btn) => {
      btn.classList.remove("active"); // Remove active class from all buttons
    });

    // Add 'active' class to the clicked button
    this.classList.add("active"); // Add active class to the clicked button
  });
});

submit.addEventListener("click", function (event) {
  event.preventDefault(); // Prevent the default form submission

  if (selectionInput.value == "") {
    alert("Please select the data you would like to see!");
    return;
  } else {
    // Show the loading spinner immediately
    loadingScreen.style.display = "flex";
    // Hide the options div
    filterDiv.style.display = "none";

    goBack.style.display = "none";

    window.location.href =
      "/results?selection=" +
      encodeURIComponent(selectionInput.value.toLowerCase());
  }
});
body.addEventListener("click", function (event) {
  // Check if the click is outside the buttons, AllHist, and submit button
  if (
    !event.target.classList.contains("twosec_font_fade") &&
    event.target !== submitBtn2
  ) {
    document.querySelectorAll(".filter_button").forEach((button) => {
      button.classList.remove("active"); // Reset all buttons
      selectionInput.value = "";
    });
  }
});
