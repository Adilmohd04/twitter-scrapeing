# Twitter Trending Data Scraper

This project is a web scraping tool that fetches Twitter (X) trending topics using Selenium, proxies, and stores the results in MongoDB. It logs in to the platform, scrapes trending topics, and saves them along with the IP address of the used proxy.

## Features
- Scrapes the top 5 trending topics from Twitter (X).
- Stores the trending data (name and post count) in MongoDB.
- Uses ProxyMesh to access the site through proxies.
- Logs in using Twitter credentials and handles errors during login.
- Saves data with timestamp and IP address of the proxy used.

## Prerequisites
- Python 3.11
- MongoDB (locally or cloud-based like MongoDB Atlas)
- Selenium
- ProxyMesh account for proxy access
- Add your current I/P Address in proxy ip address section
- Chrome WebDriver
- `dotenv` to manage environment variables
- MongoDB URI

## Installation

1. Clone the repository:
    ```bash
    git clone https://github.com/Adilmohd04/twitter-scraping.git
    cd twitter-scraping
    ```

2. Install the required Python dependencies:
    ```bash
    pip install -r requirements.txt
    ```

3. Create a `.env` file in the root of the project and add your credentials and MongoDB URI:
    ```env
    TWITTER_EMAIL=your_twitter_email
    TWITTER_USERNAME=your_twitter_username
    TWITTER_PASSWORD=your_twitter_password
    MONGO_URI=mongodb://your_mongo_uri
    ```

## Usage

1. Run the scraper by executing the script:
    ```bash
    python app.py
    ```

2. The script will log in to Twitter (X), navigate to the trending section, and extract the trending data.
![image](https://github.com/user-attachments/assets/be1df399-4ecc-4892-839b-e084a777d03b)

## Troubleshooting

- If you encounter login issues, make sure to disable any privacy-related browser extensions or retry after refreshing the page.
- Ensure that the ProxyMesh proxy server is working and accessible.

