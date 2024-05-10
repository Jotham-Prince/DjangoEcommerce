document.addEventListener("DOMContentLoaded", function() {
    const fileInput = document.getElementById("file-input");
    const uploadArea = document.querySelector(".upload-area");
    const uploadButton = document.querySelector(".btn-capture"); // Correct selector for the upload button

    // Function to update upload area when files are selected
    fileInput.addEventListener("change", function() {
        const files = fileInput.files;
        if (files.length > 0) {
            // Clear previous content
            uploadArea.innerHTML = '';

            // Iterate over selected files
            for (let i = 0; i < files.length; i++) {
                const file = files[i];
                
                // Create img element
                const img = document.createElement('img');
                img.classList.add('upload-image');
                img.file = file;
                uploadArea.appendChild(img);

                // Display file name
                const fileName = file.name;
                const fileNameElement = document.createElement('span');
                fileNameElement.textContent = fileName;
                uploadArea.appendChild(fileNameElement);

                // Display image preview
                const reader = new FileReader();
                reader.onload = (function(aImg) {
                    return function(e) {
                        aImg.src = e.target.result;
                    };
                })(img);
                reader.readAsDataURL(file);
            }
        }
    });

    // Function to handle click event for "Upload File" button
    uploadButton.addEventListener("click", function() {
        // Add code to upload files here
        console.log("Uploading files...");
    });
});
