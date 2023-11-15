document.addEventListener('DOMContentLoaded', function() {
              
    let fadeElement1 = document.getElementsByClassName('font_fade');
    let fadeElement2 = document.getElementsByClassName('body_fade');
    
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
        let fadeElement3 = document.getElementsByClassName('twosec_font_fade');
      
        for (let i = 0; i < fadeElement3.length; i++) {
          (function(i) {
            setTimeout(function() {
              fadeElement3[i].style.opacity = 1;
            }, i * 100); // Adjust the delay (1000 milliseconds = 1 second in this example)
          })(i);
        }
      }
      
      
      

    setTimeout(fadeIn2, 500);
    setTimeout(fadeIn1, 1000); 
    setTimeout(fadeIn3, 1500);// Delay the fade-in effect by 1 second (1000 milliseconds)
    });

    window.onbeforeunload = function () {
    window.scrollTo(0, 0);
    }