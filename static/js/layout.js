document.addEventListener("DOMContentLoaded", function () {
  let fadeElement1 = document.getElementsByClassName("font_fade");
  let fadeElement2 = document.getElementsByClassName("body_fade");

  function fadeIn1() {
    for (let i = 0; i < fadeElement1.length; i++) {
      fadeElement1[i].style.opacity = 1;
    }
  }

  function fadeIn2() {
    for (let i = 0; i < fadeElement2.length; i++) {
      fadeElement2[i].style.opacity = 1;
    }
  }

  function fadeIn3() {
    let fadeElement3 = document.getElementsByClassName("twosec_font_fade");
    let fadeElement4 = document.getElementById("AllHist");

    for (let i = 0; i < fadeElement3.length; i++) {
      (function (i) {
        setTimeout(function () {
          fadeElement3[i].style.opacity = 1;
        }, i * 100);
        // Adjust the delay (1000 milliseconds = 1 second in this example)
      })(i);
    }

    setTimeout(function () {
      fadeElement4.style.opacity = 1;
    }, fadeElement3.length * 100); // Use a timeout that accommodates the total delay of the loop
  }

  setTimeout(fadeIn1, 1000);
  setTimeout(fadeIn2, 500);
  setTimeout(fadeIn3, 1500); // Delay the fade-in effect by 1 second (1000 milliseconds)
});

window.onbeforeunload = function () {
  window.scrollTo(0, 0);
};
