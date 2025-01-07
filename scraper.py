import os
import time
import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options as ChromeOptions
from pymongo import MongoClient
import requests
from dotenv import load_dotenv
from webdriver_manager.chrome import ChromeDriverManager

load_dotenv()

MONGODB_URI = os.getenv('MONGO_URI')
client = MongoClient(MONGODB_URI)
db = client.twitter_trends
collection = db.trends


def get_proxy():
    return f"us-ca.proxymesh.com:31280"


def current_ip_address():
    proxy_url = get_proxy()
    try:
        response = requests.get(
            'https://api.ipify.org/?format=json',
            proxies={"http": proxy_url, "https": proxy_url},
            timeout=10
        )
        ip_address = response.json().get('ip', 'N/A')
        print(f"Connected to ProxyMesh. IP Address: {ip_address}")
        return ip_address
    except requests.RequestException as e:
        print(f"Error connecting to ProxyMesh: {e}")
        return 'N/A'


def get_driver(proxy_url):
    service = ChromeService(ChromeDriverManager().install())
    options = ChromeOptions()
    options.add_argument(f'--proxy-server={proxy_url}')
    options.add_argument('--disable-blink-features=AutomationControlled')
    options.add_argument('--disable-extensions')
    options.add_argument('--disable-popup-blocking')
    options.add_argument('start-maximized')
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)
    # JavaScript to avoid detection
    options.add_argument("--disable-infobars")
    return webdriver.Chrome(service=service, options=options)

def handle_pre_login_error(driver):
    """Handle the 'Something went wrong' error before the login process."""
    retries = 3
    while retries > 0:
        try:
            if "Something went wrong" in driver.page_source:
                print("Detected 'Something went wrong' error.")
                
                try_again_button = WebDriverWait(driver, 5).until(
                    EC.element_to_be_clickable((By.XPATH, "//span[text()='Try again']"))
                )
                print("Clicking 'Try Again' button...")
                try_again_button.click()
                time.sleep(5)
            else:
                print("No pre-login error detected. Proceeding to login...")
                return
        except Exception as e:
            print(f"Retrying... {retries} attempts left. Error: {e}")
            retries -= 1
            driver.refresh()
            time.sleep(5)
    raise Exception("Failed to resolve 'Something went wrong' error after multiple attempts.")


def attempt_login(driver):
    retries = 3
    while retries > 0:
        try:
            print("Attempting login...")
            WebDriverWait(driver, 15).until(
                EC.presence_of_element_located((By.NAME, 'text'))
            ).send_keys(os.getenv('TWITTER_EMAIL'))
            driver.find_element(By.NAME, 'text').send_keys(Keys.RETURN)
            time.sleep(2)

            WebDriverWait(driver, 15).until(
                EC.presence_of_element_located((By.NAME, 'text'))
            ).send_keys(os.getenv('TWITTER_USERNAME'))
            driver.find_element(By.NAME, 'text').send_keys(Keys.RETURN)
            time.sleep(2)

            WebDriverWait(driver, 15).until(
                EC.presence_of_element_located((By.NAME, 'password'))
            ).send_keys(os.getenv('TWITTER_PASSWORD'))
            driver.find_element(By.NAME, 'password').send_keys(Keys.RETURN)
            time.sleep(5)
            print("Login successful.")
            return True
        except Exception as e:
            print(f"Login failed. Retrying... {retries} attempts left. Error: {e}")
            retries -= 1
    return False


def scrape_trending_data():
    proxy = get_proxy()
    driver = get_driver(proxy)
    try:
        print("Starting browser session with proxy...")
        driver.get('https://x.com/login')

        handle_pre_login_error(driver)

        if not attempt_login(driver):
            print("Login process failed.")
            return

        print("Navigating to Twitter trending topics...")
        driver.get('https://x.com/explore/tabs/for_you')
        time.sleep(5)

        print("Extracting trending data...")
        trends = []

        trend_elements = WebDriverWait(driver, 15).until(
            EC.presence_of_all_elements_located((By.XPATH, "//div[@data-testid='trend']"))
        )

        for i, trend_element in enumerate(trend_elements[:5]):
            try:
                trend_name = trend_element.find_element(By.XPATH, ".//div[contains(@style, 'color: rgb(231, 233, 234);')]//span").text

                try:
                    post_count = trend_element.find_element(By.XPATH, ".//span[contains(text(), 'Tweets') or contains(text(), 'posts')]").text
                except:
                    post_count = "No post count available"

                trends.append({'name': trend_name, 'posts': post_count})

            except Exception as e:
                print(f"Error extracting trend {i + 1}: {e}")

        if trends:
            record = {
                "trends": trends,
                "date": datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                "ip_address": current_ip_address(),
            }

            collection.insert_one(record)
            print("Trending data successfully saved to MongoDB:", record)
            return record
        else:
            print("No trends found.")
    except Exception as e:
        print(f"Error during scraping: {e}")
    finally:
        print("Closing the browser...")
        driver.quit()


if __name__ == "__main__":
    scrape_trending_data()
