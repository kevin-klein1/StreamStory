/* Need to fix bugs with rejecting already uploaded files. Drag and Drop wrongly
allows old files to be redropped. Browse won't let old files come in, if it's the only file selected.
But if there is a 'new' file with it, it will bypass the logic and allow it to be displayed.

The issue lies in the fact that the Display File Name function doesn't check for old files. So if it works it will 
display all names. I wonder if we could ad a check inside function.*/

let droppedFiles = [];
let formData = new FormData();

// Add DataTransfer object to track all files
let allFiles;

// Check if DataTransfer is supported by the browser
if (typeof DataTransfer !== "undefined") {
  allFiles = new DataTransfer();
} else {
  console.warn(
    "Your browser may not fully support batched file uploads. Please upload all files at once."
  );
  // Simple fallback object with no-op functions
  allFiles = {
    items: {
      add: function () {}, // No-op function
    },
    files: [],
  };
}

const browseButton = document.getElementById("browseButton");

// Get Hex value for dynamically changing drag and drop
const purple = document.querySelector(".background");
const computedStyle = getComputedStyle(purple);
const mainColor = computedStyle.getPropertyValue("--main-color").trim();
const secColor = computedStyle.getPropertyValue("--sec-color").trim();

const dropArea = document.getElementById("drop-area");

const dropText = "Drop!";

document
  .getElementById("drop-area")
  .addEventListener("dragover", function (event) {
    event.preventDefault();
    this.style.backgroundColor = secColor;
    this.style.color = "black";
    this.style.borderColor = mainColor;
    browseButton.style.color = mainColor;
  });

document
  .getElementById("drop-area")
  .addEventListener("dragleave", function (event) {
    event.preventDefault();
    this.style.backgroundColor = mainColor;
    this.style.color = "white";
    this.style.borderColor = secColor;
    browseButton.style.color = secColor;
  });

document.getElementById("drop-area").addEventListener("drop", function (event) {
  event.preventDefault();

  let files = event.dataTransfer.files;

  if (files.length > 0) {
    fileExtensionCheckFailed = false;
    for (let i = 0; i < files.length; i++) {
      let file = files[i];
      const ApprovedExt = "json";
      let fileName = file["name"];
      let fileExtension = fileName.split(".").pop().toLowerCase();

      if (!ApprovedExt.includes(fileExtension)) {
        alert(
          `File named: "${file.name}" is invalid. Please upload file of type .JSON`
        );
        fileExtensionCheckFailed = true;
        continue;
      }
      if (!isFileAlreadyUploaded(file)) {
        droppedFiles.push(file);
        // Add to our DataTransfer object to collect all files
        if (typeof DataTransfer !== "undefined") {
          allFiles.items.add(file);
        }
        displayFileNames(file);
      }
      // if (!fileExtensionCheckFailed) {
      //   displayFileNames(file);
      // }
    }
    this.style.backgroundColor = mainColor;
    this.style.color = "white";
    this.style.borderColor = secColor;
    browseButton.style.color = secColor;

    // Update the file input with ALL files collected so far
    if (typeof DataTransfer !== "undefined") {
      document.getElementById("fileInput").files = allFiles.files;
    }
  }

  // Still keep this for backward compatibility, but primary submission will use fileInput
  let file_input = document.getElementById("fileInput2");
  file_input.files = files;
  console.log(files);
});

document.getElementById("browseButton").addEventListener("click", function () {
  document.getElementById("fileInput").click();
});

document
  .getElementById("fileInput")
  .addEventListener("change", function (event) {
    event.preventDefault();

    let files = this.files;

    if (files.length > 0) {
      for (let i = 0; i < files.length; i++) {
        let file = files[i];
        if (!isFileAlreadyUploaded(file)) {
          droppedFiles.push(file);
          // Add to our DataTransfer object
          if (typeof DataTransfer !== "undefined") {
            allFiles.items.add(file);
          }
          displayFileNames(file);
        }
      }

      // Update the fileInput element with all accumulated files
      if (typeof DataTransfer !== "undefined") {
        // We need to do this in a setTimeout to avoid recursive change events
        setTimeout(() => {
          document.getElementById("fileInput").files = allFiles.files;
        }, 0);
      }
    }
  });

function isFileAlreadyUploaded(file) {
  for (var i = 0; i < droppedFiles.length; i++) {
    if (
      droppedFiles[i].name === file.name &&
      droppedFiles[i].size === file.size
    ) {
      return true;
    }
  }
  return false;
}

function displayFileNames(file) {
  // Access the file name directly
  document.getElementById("file-list").innerHTML += "<br>" + file.name;
  document.getElementById("file-list").style.display = "flex";
  document.getElementById("submitBtn").style.display = "flex";
}

document.getElementById("submitBtn").addEventListener("click", function () {
  console.log("Files in droppedFiles array:", droppedFiles.length);
  console.log(
    "Files in fileInput:",
    document.getElementById("fileInput").files.length
  );
  console.log(
    "Files in fileInput2:",
    document.getElementById("fileInput2").files.length
  );

  // Submit the form with all collected files
  document.getElementById("uploadForm").submit();
});
