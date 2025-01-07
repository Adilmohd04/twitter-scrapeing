document.getElementById('run-script-btn').addEventListener('click', () => {
    const resultContainer = document.getElementById('result-container');
    const datetimeElem = document.getElementById('datetime');
    const trendList = document.getElementById('trend-list');
    const ipAddressElem = document.getElementById('ip-address');
    const jsonDataElem = document.getElementById('json-data');

    // Hide the "Run Script" button and show the result container
    document.getElementById('run-script-btn').style.display = 'none';
    resultContainer.style.display = 'block';

    // Fetch trends data from backend
    fetch('/run-scraper')
        .then(response => response.json())
        .then(data => {
            // Update the date/time
            datetimeElem.textContent = data.date_time;

            // Update the IP address
            ipAddressElem.textContent = data.ip_address;

            // Display the trend data
            trendList.innerHTML = '';
            data.trends.forEach(trend => {
                const li = document.createElement('li');
                li.textContent = `${trend.name}: ${trend.posts}`;
                trendList.appendChild(li);
            });

            // Show JSON data
            jsonDataElem.textContent = JSON.stringify(data.mongo_record, null, 2);
        })
        .catch(error => console.error('Error fetching data:', error));
});
document.getElementById('run-script-btn-again').addEventListener('click', () => {
    const resultContainer = document.getElementById('result-container');
    const datetimeElem = document.getElementById('datetime');
    const trendList = document.getElementById('trend-list');
    const ipAddressElem = document.getElementById('ip-address');
    const jsonDataElem = document.getElementById('json-data');

    // Hide the "Run Script" button and show the result container
    document.getElementById('run-script-btn').style.display = 'none';
    resultContainer.style.display = 'block';

    // Fetch trends data from backend
    fetch('/run-scraper')
        .then(response => response.json())
        .then(data => {
            // Update the date/time
            datetimeElem.textContent = data.date_time;

            // Update the IP address
            ipAddressElem.textContent = data.ip_address;

            // Display the trend data
            trendList.innerHTML = '';
            data.trends.forEach(trend => {
                const li = document.createElement('li');
                li.textContent = `${trend.name}: ${trend.posts}`;
                trendList.appendChild(li);
            });

            // Show JSON data
            jsonDataElem.textContent = JSON.stringify(data.mongo_record, null, 2);
        })
        .catch(error => console.error('Error fetching data:', error));
});
