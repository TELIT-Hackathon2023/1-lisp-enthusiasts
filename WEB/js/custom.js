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
    /*
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
      */
      fetch('data.json')
      .then(response => response.json())
      .then(data => {
        // Do something with the data
        console.log(data);
        // Call a function to render the data
        renderData(data);
      })
      .catch(error => console.error('Error fetching data:', error));
  }


function renderData(data) {
  render_time_metrics(data)
  render_score(data)
  render_metrics(data)
}


function append_div(title, value, category, description) {
  const containerDiv = document.createElement('div');
  const fcpLabel = document.createElement('strong');
  fcpLabel.textContent = title + ' (' + category + ') = ' + value;
  const loremParagraph = document.createElement('p');
  loremParagraph.textContent = description;

  containerDiv.appendChild(fcpLabel);
  containerDiv.appendChild(loremParagraph);
  const outputDiv = document.getElementById('output');
  outputDiv.appendChild(containerDiv);
}


function render_metrics(data) {
  const keysWithSpecificValue = [];
  
  for (const key in data) {
    if (data.hasOwnProperty(key) && key.includes("_score")) {
      keysWithSpecificValue.push(key);
    }
  
  }

  for (let i = 0; i < keysWithSpecificValue.length; i++) {

    let lastIndex = keysWithSpecificValue[i].lastIndexOf("_");

    let val = keysWithSpecificValue[i].substring(0, lastIndex);
    description = val + "_description"
    console.log(keysWithSpecificValue[i])
    append_metric(val, data[keysWithSpecificValue[i]], data[description])

  }
}

function render_time_metrics(data) {
  if (data && 'fcp' in data) {
    append_div("FCP Value", data.fcp, data.fcp_category, 'The First Contentful Paint (FCP) metric measures the time from when the page starts loading to when any part of the pages content is rendered on the screen.')
  }

  if (data && 'fid' in data) {
    append_div("FID Value", data.fid, data.fid_category, 'FID measures the time from when a user first interacts with a page to the time when the browser is actually able to begin processing event handlers in response to that interaction.')
  }

  if (data && 'lcp' in data) {
    append_div("LCP Value", data.lcp, data.lcp_category, 'The Largest Contentful Paint (LCP) metric reports the render time of the largest image or text block visible within the viewport, relative to when the page first started loading.')
  }

  if (data && 'cls' in data) {
    append_div("CLS Value", data.cls, data.cls_category, 'CLS is a measure of the largest burst of layout shift scores for every unexpected layout shift that occurs during the entire lifespan of a page.')
  }
}


function render_score(data) {
  if (data && 'overall_score' in data) {
    category = ""
    if (data.overall_score > 50) {
      category = "GOOD"
    }
    else {
      category = "BAD"
    }
    append_div("Overall score", data.overall_score, category, 'Overall performance and design score')
  }

  total_tasks_time = data.total_tasks_time
  num_requests = data.num_requests
  num_requests_description = data.num_requests_description
  append_div("Total tasks time", total_tasks_time, num_requests, num_requests_description)
}


function append_metric(title, score, description) {
  category = ""
  if (score > 0.8) {
    category = "GOOD"
    description = ""
  }
  else {
    category = "BAD"
  }

  const containerDiv = document.createElement('div');
  const fcpLabel = document.createElement('strong');
  fcpLabel.textContent = title + ' (' + category + " score: " + score + ')';
  const loremParagraph = document.createElement('p');
  loremParagraph.textContent = description;

  containerDiv.appendChild(fcpLabel);
  containerDiv.appendChild(loremParagraph);
  const outputDiv = document.getElementById('output');
  outputDiv.appendChild(containerDiv);
}