function submitPersonas() {
    var urlInput = document.getElementById('urlInput');
    var formData = new FormData();
    formData.append('url', urlInput.value);
  
    fetch('http://localhost:8000/api/personas', {
        method: 'POST',
        body: formData
      })
        .then(response => response.json())
        .then(data => {
          renderPersonas(data)
        })
        .catch(error => {
          console.error('Error:', error);
        });
  
    // fetch('../text_files/personas.json')
    // .then(response => response.json())
    // .then(data => {
    //   renderPersonas(data);
    // })
    // .catch(error => console.error('Error fetching data:', error));
  return false
  }
  
  function main() {
    var fileInput = document.getElementById('file-upload');
    var urlInput = document.getElementById('urlInput');
    var formData = new FormData();
    formData.append('url', urlInput.value);

    submitPersonas(formData)
    
    renderObsolete(formData)
    renderContrast(formData)
    
    submitForm(formData)
    renderTips(formData)
    return false
  }
  
function renderTips() {
  fetch('http://localhost:8000/api/tips', {
      method: 'GET',
    })
      .then(response => response.json())
      .then(data => {
        displayTips(data)
      })
      .catch(error => {
        console.error('Error:', error);
      });
}
  
  function displayTips(data) {
    const outputDiv = document.getElementById('custom');
    var tempElement = document.createElement('div');
    tempElement.innerHTML = "<strong>"+data+"</strong>";
    outputDiv.appendChild(tempElement)
  }
  
  function submitForm(formData) {
      fetch('http://localhost:8000/api/analytics', {
        method: 'POST',
        body: formData
      })
        .then(response => response.json())
        .then(data => {
            renderData(data);
        })
        .catch(error => {
          // Handle errors
          console.error('Error:', error);
        });

        // fetch('../text_files/data.json')
        // .then(response => response.json())
        // .then(data => {
        //   renderData(data);
        // })
        // .catch(error => console.error('Error fetching data:', error));
    }
  
  
  
  function displayContrast(contrast) {
    const outputDiv = document.getElementById('custom');
    var tempElement = document.createElement('div');
    tempElement.innerHTML = "The contrast index of your websites dominant colors is: " + contrast.contrast;
    outputDiv.appendChild(tempElement)
  }
  
  
  function renderContrast() {
    var urlInput = document.getElementById('urlInput');
    var formData = new FormData();
    formData.append('url', urlInput.value);
  
    fetch('http://localhost:8000/api/contrast', {
        method: 'POST',
        body: formData
      })
        .then(response => response.json())
        .then(data => {
          displayContrast(data)
          console.log(data)
      })
      .catch(error => {
        console.error('Error:', error);
      });
  }
  
  
  
  
  
  function renderObsolete(formData) {
    // var urlInput = document.getElementById('urlInput');
    // var formData = new FormData();
    // formData.append('url', urlInput.value);
  
    // fetch('../text_files/html.txt',) 
    //     .then(response => response.json())
    //     .then(data => {
    //       findObsoleteTags(data)
    //   })
    //   .catch(error => {
    //     console.error('Error:', error);
    //   });

      fetch('http://localhost:8000/api/html', {
        method: 'POST',
        body: formData
      })
        .then(response => response.json())
        .then(data => {
          findObsoleteTags(data)
      })
      .catch(error => {
        console.error('Error:', error);
      });

      return false;
  }
  
  
  function findObsoleteTags(data) {
      const obsoleteTags = ['font', 'center', 'strike', 's', 'u', 'applet', 'basefont', 'big', 'blink', 'marquee'];
  
      var tempElement = document.createElement('div');
      tempElement.innerHTML = data;
  
      const allElements = tempElement.getElementsByTagName('*');
      const obsoleteTagsFound = [];
  
      for (let i = 0; i < allElements.length; i++) {
        const tagName = allElements[i].tagName.toLowerCase();
  
        if (obsoleteTags.includes(tagName)) {
          obsoleteTagsFound.push(tagName);
        }
      }
  
      var uniqueArray = Array.from(new Set(obsoleteTagsFound));
      const outputDiv = document.getElementById('custom');
      const containerDiv = document.createElement('div');
      const loremParagraph = document.createElement('p');
  
      if (uniqueArray.length > 0) {
         loremParagraph.innerText = 'Obsolete HTML tags found: ' + uniqueArray.join(', ')
      } else {
        loremParagraph.innerText ='No obsolete HTML tags found.';
      }
  
      containerDiv.appendChild(loremParagraph)
      outputDiv.appendChild(containerDiv)
  }
  
  
  function renderPersonas(data) {
    renderType(data)
    renderAudience(data)
  }
  
  
  function renderAudience(data) {
    data = data.response
    const outputDiv = document.getElementById('personas');
  
    for (const key in data) {
      if (data.hasOwnProperty(key)) {
        const listItem = document.createElement('p');
        listItem.textContent = `${key} - ${data[key]}`;
        outputDiv.appendChild(listItem);
      }
    }
  }
  
  
  function renderType(data) {
    const outputDiv = document.getElementById('personas');
    const containerDiv = document.createElement('div');
    const fcpLabel = document.createElement('strong');
    fcpLabel.textContent = "Audience of this website mostly consists of " + data.type + " people!";
    const loremParagraph = document.createElement('p');
    
    if (data.type == 'technical') {
      loremParagraph.textContent = "For technical people the UI simplicity is less necessary. On the other hand, we advise to focus on security and responsivity aspects more.";
    }
    if (data.type == "non-technical") {
      loremParagraph.textContent = "For non-technical we advise to create very simple and intuitive UI/UX. Latest functionality, animations and advanced interactivity in general might be less important.";
    }
    if (data.type == "artists") {
      loremParagraph.textContent = "Artists tend to value carefully chosen color palette and smooth animations of the website.";
    }
  
    containerDiv.appendChild(fcpLabel);
    containerDiv.appendChild(loremParagraph);
    outputDiv.appendChild(containerDiv);
  }
  
  
  function renderData(data) {
    render_time_metrics(data)
    render_score(data)
    render_metrics(data)
  }
  
  
  function append_div_turbo(title, value, category, description) {
    const containerDiv = document.createElement('div');
    containerDiv.classList.add('grid-item');
    if (value >= 80) {
      containerDiv.classList.add('g');
    }
    else {
      containerDiv.classList.add('o');
    }
    const fcpLabel = document.createElement('strong');
    fcpLabel.textContent = title + ' (' + category + ') = ' + value;
    const loremParagraph = document.createElement('p');
    loremParagraph.textContent = description;
  
    containerDiv.appendChild(fcpLabel);
    containerDiv.appendChild(loremParagraph);
    const outputDiv = document.getElementById('output');
    outputDiv.appendChild(containerDiv);
  }
  
  
  function append_div(title, value, category, description) {
    const containerDiv = document.createElement('div');

    
    containerDiv.classList.add('grid-item');
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
      append_div_turbo("Overall score", data.overall_score, category, 'Overall performance and design score')
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

    if (score >= 0.9) {
      containerDiv.classList.add('g');
    }
    else {
      containerDiv.classList.add('o');
    }
  

    containerDiv.classList.add('grid-item');
    const fcpLabel = document.createElement('strong');
    fcpLabel.textContent = title + ' (' + category + " score: " + score + ')';
    const loremParagraph = document.createElement('p');
    loremParagraph.textContent = description;
  
    containerDiv.appendChild(fcpLabel);
    containerDiv.appendChild(loremParagraph);
    const outputDiv = document.getElementById('output');
    outputDiv.appendChild(containerDiv);
  }