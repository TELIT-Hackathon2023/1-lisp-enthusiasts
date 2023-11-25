// to get current year
function getYear() {
    var currentDate = new Date();
    var currentYear = currentDate.getFullYear();
    document.querySelector("#displayYear").innerHTML = currentYear;
}

getYear();


function submitForm() {
    // Get the file input and text input values
    var fileInput = document.getElementById('file-upload');
    var urlInput = document.getElementById('urlInput');

    var formData = new FormData();
    formData.append('url', urlInput.value);

    // Fetch API to send the POST request
    fetch('http://localhost:8000/api/analytics', {
      method: 'POST',
      body: formData
    })
      .then(response => response.json())
      .then(data => {
        // Handle the response data as needed
        console.log(data);
      })
      .catch(error => {
        // Handle errors
        console.error('Error:', error);
      });
  }