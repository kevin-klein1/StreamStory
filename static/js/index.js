let droppedFiles = [];
let formData = new FormData(); 

document.getElementById('drop-area').addEventListener('dragover', function(event) {
    event.preventDefault();
    this.style.backgroundColor = '#f0f0f0';
});

document.getElementById('drop-area').addEventListener('dragleave', function(event) {
    event.preventDefault();
    this.style.backgroundColor = 'rgb(228, 175, 228)';
});

    
    document.getElementById('drop-area').addEventListener('drop', function(event) {
        event.preventDefault();
        


        let files = event.dataTransfer.files;
     
        if (files.length > 0)  {
            fileExtensionCheckFailed = false;
            for (let i = 0; i < files.length; i++) {
                let file = files[i];
                const ApprovedExt = 'json'
                let fileName = file['name'];
                let fileExtension = fileName.split('.').pop().toLowerCase();


                if(!ApprovedExt.includes(fileExtension)) {
                    alert("Please upload file of type .JSON");
                    fileExtensionCheckFailed = true;
                    break;
                }
                if ((!isFileAlreadyUploaded(file)) && (droppedFiles.length < 10)) {
                    droppedFiles.push(file);
                }

            }
            console.log(fileExtensionCheckFailed);

            if (!fileExtensionCheckFailed) {
                displayFileNames(droppedFiles);
                this.style.backgroundColor = '#f0f0f0';
                this.style.borderColor = 'green';
                let button = document.getElementById('browseButton');
                button.style.color = '#1DB954';
                button.style.fontWeight = "bold";
              }
              this.style.backgroundColor = "rgb(228, 175, 228)";
              this.style.border = "2px dashed #CFF56A";
              this.style.color = "black";
            
        }
        
        let file_input = document.getElementById('fileInput2');
        file_input.files = files; 
    });

    document.getElementById('browseButton').addEventListener('click', function() {
        document.getElementById('fileInput').click();

    });

    document.getElementById('fileInput').addEventListener('change', function(event) {
        event.preventDefault();
        this.style.backgroundColor = '#f0f0f0';

        let button = document.getElementById('browseButton');
        button.style.color = '#1DB954';
        button.style.fontWeight = "bold";


        let files = this.files;
    
        if (files.length > 0)  {
            for (let i = 0; i < files.length; i++) {
                let file = files[i];
                if ((!isFileAlreadyUploaded(file)) && (droppedFiles.length < 10)) {
                    droppedFiles.push(file);
                    
                }
            }
            displayFileNames(droppedFiles);
        }
    
    });


    function isFileAlreadyUploaded(file) {
        for (var i = 0; i < droppedFiles.length; i++) {
            if (droppedFiles[i].name === file.name && droppedFiles[i].size === file.size) {
                return true;
            }
        }
        return false;
    }

    function displayFileNames(files) {
        var fileNames = [];
        for (var i = 0; i < files.length; i++) {
            fileNames.push(files[i].name);
        }


    


document.getElementById('file-list').innerHTML = fileNames.join('<br>');
document.getElementById('file-list').style.textDecoration = 'underline'
document.getElementById('file-list').style.fontWeight = 'bold'
document.getElementById('file-list').style.fontSize = '14px'
document.getElementById('file-list').style.color = 'purple'
document.getElementById('file-list').style.fontStyle = 'italic'
document.getElementById('file-list').style.padding = '1px'
document.getElementById('file-list').style.display = 'block'
document.getElementById('submitBtn').style.display = 'block';

}
