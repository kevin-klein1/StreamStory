    let answers = []

    const year_button = document.querySelectorAll('.twosec_font_fade');
    const all = document.getElementById("all");
    const body = document.getElementById("clicker");
    let years_list = document.getElementById("hiddenInput").value;
    

    for (let i = 0; i < year_button.length; i++) {
        let button_color = year_button[i];
        let isGreen = false;


        button_color.addEventListener('click', function (event) {
            if (isGreen) {
                button_color.style.backgroundColor = "white"; // Change to the second color
                value = event.target.value;
                answers = answers.filter(item => item !== value);


                if (value === "All Your History") {
                    for (let k = 0; k < year_button.length; k++) {
                        let button_color = year_button[k];
                        button_color.style.backgroundColor = "white";
                        answers = [];
                    }
                   
                }



            } else {
                button_color.style.backgroundColor = "#CFF56A"; // Change to the first color
                value = event.target.value;
                answers.push(value);

            
                if (value === "All Your History") {
                    answers = [];
                    answers.push('2012', '2013','2014','2015','2016','2017','2018','2019','2020','2021','2022','2023');
                    for (let j = 0; j < year_button.length; j++) {
                        const button_color = year_button[j];
                        button_color.style.backgroundColor = "#CFF56A";
                        
                    }
                
                }
               
            }
            
            // Toggle the state
            let years_list = document.getElementById('hiddenInput').value = answers.join(',');
            console.log(years_list)
            isGreen = !isGreen;
           
            console.log(answers);
          
            
        });

        body.addEventListener('click', function(event) {
            if ((!event.target.classList.contains('twosec_font_fade'))) {
            console.log("SUP BITCH");
            for (let i = 0; i < year_button.length; i++) {
                let button_color = year_button[i];
                button_color.style.backgroundColor = "white";
              
            }
                answers = [];
                isGreen = false;
            }

    

        });


    }

