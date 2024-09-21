let answers = [];
let selected = [];

const year_button = document.querySelectorAll(".twosec_font_fade");
const all = document.getElementById("all");
const outside = document.getElementById("clicker");
let years_list = document.getElementById("hiddenInput");
const AllHist = document.getElementById("AllHist");
const submit = document.getElementById("submit_button");
let isGreen = false;

const form = document.getElementById("yearForm");

// Function to update hiddenInput value based on answers array
function updateHiddenInput() {
  years_list.value = answers.join(",");
}

for (let i = 0; i < year_button.length; i++) {
  const button_color = year_button[i];

  button_color.addEventListener("click", function (event) {
    v = event.target.value;

    if (answers.indexOf(v) >= 0) {
      button_color.style.backgroundColor = "white"; // Change to the second color
      button_color.style.boxShadow = "";
      value = event.target.value;
      answers = answers.filter((item) => item !== value);
    } else {
      button_color.style.backgroundColor = "#CFF56A"; // Change to the first color
      button_color.style.boxShadow = "inset -2px -2px 5px  black";
      value = event.target.value;
      answers.push(value);
    }
    console.log(answers);
  });
}

outside.addEventListener("click", function (event) {
  if (
    !event.target.classList.contains("twosec_font_fade") &&
    event.target.getAttribute("id") != "AllHist" &&
    event.target.getAttribute("id") != "submit_button"
  ) {
    console.log("SUP BITCH");

    for (let i = 0; i < year_button.length; i++) {
      let button_color = year_button[i];
      button_color.style.backgroundColor = "white";
      button_color.style.boxShadow = "";
    }
    answers = [];
  }

  // isGreen = !isGreen;
});

AllHist.addEventListener("click", function (event) {
  let button = event.target.value;

  if (isGreen) {
    answers = [];
    for (let i = 0; i < year_button.length; i++) {
      let button_color = year_button[i];
      button_color.style.backgroundColor = "white";
      button_color.style.boxShadow = "";
    }
    AllHist.style.backgroundColor = "white";
    AllHist.style.boxShadow = "";

    // Bug in the fact that you can't click a single year while they are all selected
  } else {
    for (let i = 0; i < year_button.length; i++) {
      let button_color = year_button[i];
      button_color.style.backgroundColor = "#CFF56A";
      button_color.style.boxShadow = "inset -2px -2px 5px  black";
    }
    AllHist.style.backgroundColor = "#CFF56A";
    AllHist.style.boxShadow = "inset -2px -2px 5px  black";
    answers = [
      "2012",
      "2013",
      "2014",
      "2015",
      "2016",
      "2017",
      "2018",
      "2019",
      "2020",
      "2021",
      "2022",
      "2023",
      "2024",
    ];
  }
  isGreen = !isGreen;

  // Get the array to the hidden input value

  console.log(answers);
});

console.log(answers);
// Submit the form
form.addEventListener("submit", function (event) {
  // Prevent the default form submission behavior
  event.preventDefault();

  // Update hiddenInput value before form submission based on answers array
  updateHiddenInput();
  console.log(new FormData(form));

  form.submit();
});
