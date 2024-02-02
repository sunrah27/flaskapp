fetch('testData.json')
  .then(response => response.json())
  .then(testData => {
    // Loop through the test data and make a POST request for each entry
    testData.forEach(data => {
      fetch('http://127.0.0.1:5000/api/register', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(data),
      })
        .then(response => response.json())
        .then(responseData => console.log(responseData))
        .catch(error => console.error('Error:', error));
    });
  })
  .catch(error => console.error('Error fetching testData:', error));