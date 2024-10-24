/* Need to fix bugs with rejecting already uploaded files. Drag and Drop wrongly
allows old files to be redropped. Browse won't let old files come in, if it's the only file selected.
But if there is a 'new' file with it, it will bypass the logic and allow it to be displayed.

The issue lies in the fact that the Display File Name function doesn't check for old files. So if it works it will 
display all names. I wonder if we could ad a check inside function.*/

let droppedFiles = [];
let formData = new FormData();

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
        alert(`File named: "${file.name}" is invalid. Please upload file of type .JSON`);
        fileExtensionCheckFailed = true;
        continue;
      }
      if (!isFileAlreadyUploaded(file)) {
        droppedFiles.push(file);
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
  }
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
          displayFileNames(file);
        }
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
  document.getElementById("uploadForm").submit();
});
