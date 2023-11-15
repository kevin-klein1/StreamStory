    let answers = []

    const year_button = document.querySelectorAll('.twosec_font_fade');
    const all = document.getElementById("all");
    const outside = document.getElementById("clicker");
    let years_list = document.getElementById("hiddenInput");
    const AllHist = document.getElementById("AllHist");
    let isGreen = false;

    const form = document.getElementById('yearForm');
    
    // Function to update hiddenInput value based on answers array
    function updateHiddenInput() {
        years_list.value = answers.join(',');
    }
   
    

    for (let i = 0; i < year_button.length; i++) {
        const button_color = year_button[i];
        let isGreen = false;

        button_color.addEventListener('click', function (event) {
            if (isGreen) {
                button_color.style.backgroundColor = "white"; // Change to the second color
                button_color.style.boxShadow = "";
                value = event.target.value;
                answers = answers.filter(item => item !== value);
            

            } else {
                button_color.style.backgroundColor = "#CFF56A"; // Change to the first color
                button_color.style.boxShadow = "inset -2px -2px 5px  black";
                value = event.target.value;
                answers.push(value);
            }
            
            // Toggle the state
            
            isGreen = !isGreen;
            
            console.log(answers);
            
        });

        // Outside reset broken

        /* outside.addEventListener('click', function(event) {
            if (!event.target.classList.contains("twosec_font_fade")) { 
            console.log("SUP BITCH");
            for (let i = 0; i < year_button.length; i++) {
                let button_color = year_button[i];
                button_color.style.backgroundColor = "white";
              
            }
                answers = [];
                isGreen = false;
            }

    

        }); */


    }

    AllHist.addEventListener("click", function(event) {

        let button = event.target.value;
        
            if (isGreen) {
                answers = [];
                for (let i = 0; i < year_button.length; i++) {
                    let button_color = year_button[i];
                    button_color.style.backgroundColor = "white";
                    button_color.style.boxShadow = "";
                }
                console.log(answers);
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
                answers = ['2012', '2013','2014','2015','2016','2017','2018','2019','2020','2021','2022','2023'];
               
            }
            isGreen = !isGreen;
            
    
        // Get the array to the hidden input value 
  
        console.log(answers);

    });

    form.addEventListener('submit', function(event) {
        // Prevent the default form submission behavior
        event.preventDefault();
    
        // Update hiddenInput value before form submission based on answers array
        updateHiddenInput();

        form.submit();
    
    });
  



    


