document.addEventListener("DOMContentLoaded", function () {
  // Hidden selection that we will extract value from
  const selectionInput = document.getElementById("selectionInput");
  // Div that is initial hidden that will show loading message
  const loadingScreen = document.getElementById("loading-screen");
  // Div that shows the filter option that will will hide
  const filter_div = document.getElementById("filter_div");

  // Add click event listeners to each button
  document.querySelectorAll(".filter_button").forEach((button) => {
    button.addEventListener("click", function () {
      const selectionValue = this.getAttribute("data-value");
      selectionInput.value = selectionValue; // Set the hidden input value

      // Show the loading spinner immediately
      loadingScreen.style.display = "flex";
      // Hide the options div
      filter_div.style.display = "none";

      //  redirect the browser to the results page
      // Store the selected option in the URL query string
      window.location.href =
        "/results?selection=" + encodeURIComponent(selectionValue);
    });
  });
});
