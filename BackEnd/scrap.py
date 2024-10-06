import os
import re
import threading
import time
import keyboard 
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import pandas as pd

# Set up Chrome WebDriver

service = Service("D:/software/chromedriver-win64/chromedriver.exe")
chrome_options = Options()
chrome_options.add_argument("--ignore-certificate-errors")
chrome_options.add_argument("--ignore-ssl-errors")
chrome_options.add_argument("--disable-web-security")
chrome_options.add_argument("--allow-running-insecure-content")
chrome_options.add_argument(
    "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
)

driver = webdriver.Chrome(service=service, options=chrome_options)

# Pause, resume, and stop flags
pause_event = threading.Event()
stop_flag = False
pause_event.set()  

# Function to handle scraping with pause/resume/stop functionality
def scrape_products():
    global stop_flag  # Declare global at the beginning of the function

    # Initialize lists to store extracted data
    products, prices, ratings, watchers, product_countries, discounts = [], [], [], [], [], []
    shipping_prices, conditions, seller_names, seller_sold_products, seller_ratings = [], [], [], [], []

    ProductNameToBeSearched = "water bottle"
    total_pages = 1

    try:
        for i in range(1, total_pages + 1):
            # Stop if the stop flag is set
            if stop_flag:
                print("Scraping has been stopped.")
                break

            # Pause if the pause event is cleared
            while not pause_event.is_set():
                print("Scraping is paused...")
                time.sleep(1)  # Delay to prevent excessive CPU usage

            driver.get(
                f"https://www.ebay.com/sch/i.html?_from=R40&_nkw={ProductNameToBeSearched}&_sacat=0&_ipg=240&_pgn={i}&rt=nc"
            )
            soup = BeautifulSoup(driver.page_source, "html.parser")

            for a in soup.find_all("li", attrs={"class": "s-item s-item__pl-on-bottom"}):
                # Extract required data
                name = a.find("div", attrs={"class": "s-item__title"})
                price = a.find("span", attrs={"class": "s-item__price"})
                rating = a.find("span", attrs={"class": "s-item__reviews-count"})
                ratingspan = rating.find("span") if rating else None
                country = a.find("span", attrs={"class": "s-item__location s-item__itemLocation"})
                shipping = a.find("span", attrs={"class": "s-item__shipping s-item__logisticsCost"})
                condition = a.find("span", attrs={"class": "SECONDARY_INFO"})
                watch = a.find("span", attrs={"class": "s-item__dynamic s-item__watchCountTotal"})
                watcher = watch.find("span", attrs={"class": "BOLD"}) if watch else None
                disc = a.find("span", attrs={"class": "s-item__discount s-item__discount"})
                discount = disc.find("span", attrs={"class": "BOLD"}) if disc else None

                # Seller Info
                seller_info_span = a.find("span", attrs={"class": "s-item__seller-info-text"})
                if seller_info_span:
                    seller_info_text = seller_info_span.text.strip()
                    match = re.match(r"(.+?)\s\(([\d,]+)\)\s([\d.]+%)", seller_info_text)
                    if match:
                        seller_name = match.group(1).strip()
                        seller_product = match.group(2).replace(",", "")
                        seller_rating = match.group(3)
                        seller_product = int(seller_product)
                    else:
                        seller_name = "Not available"
                        seller_product = 0
                        seller_rating = "Not available"
                else:
                    seller_name = "Not available"
                    seller_product = 0
                    seller_rating = "Not available"

                # Only process if name and price exist
                if name and price:
                    products.append(name.text.strip() if name else "Not available")

                    # Handle price conversion with default value if empty
                    price_numeric = re.sub(r"[^\d]", "", price.text)
                    try:
                        prices.append(int(price_numeric) if price_numeric else 0)
                    except ValueError:
                        prices.append(0)

                    ratings.append(ratingspan.text if ratingspan else "Not available")
                    product_countries.append(country.text if country else "Not available")

                    # Handle shipping price conversion with default value if empty
                    shipping_numeric = re.sub(r"[^\d]", "", shipping.text) if shipping else ""
                    try:
                        shipping_prices.append(int(shipping_numeric) if shipping_numeric else 0)
                    except ValueError:
                        shipping_prices.append(0)

                    watchers.append(watcher.text if watcher else "Not available")
                    discounts.append(discount.text if discount else "Not available")
                    conditions.append(condition.text if condition else "Not available")
                    seller_names.append(seller_name)
                    seller_sold_products.append(seller_product)
                    seller_ratings.append(seller_rating)

            # Print progress
            progress = (i / total_pages) * 100
            print(f"Progress: {progress:.2f}%")

    except Exception as e:
        print(f"Error occurred: {e}")

    finally:
        # Ensure the WebDriver is properly closed
        driver.quit()

        # Pad the lists to have consistent lengths
        max_length = max(len(products), len(prices), len(ratings), len(watchers), len(product_countries),
                         len(discounts), len(shipping_prices), len(conditions), len(seller_names),
                         len(seller_sold_products), len(seller_ratings))

        # Add padding with default values
        def pad_list(lst, default_value):
            while len(lst) < max_length:
                lst.append(default_value)
        
        pad_list(products, "Not available")
        pad_list(prices, 0)
        pad_list(ratings, "Not available")
        pad_list(watchers, "Not available")
        pad_list(product_countries, "Not available")
        pad_list(discounts, "Not available")
        pad_list(shipping_prices, 0)
        pad_list(conditions, "Not available")
        pad_list(seller_names, "Not available")
        pad_list(seller_sold_products, 0)
        pad_list(seller_ratings, "Not available")

        # Create and save the DataFrame even if it's empty
        df = pd.DataFrame({
            "Product Name": products,
            "Price": prices,
            "Ratings": ratings,
            "Watchers": watchers,
            "Country": product_countries,
            "Discount": discounts,
            "Shipping Price": shipping_prices,
            "Condition": conditions,
            "Seller Name": seller_names,
            "Seller Sold Products": seller_sold_products,
            "Seller Ratings": seller_ratings
        })

        # Check if the CSV file exists
        file_path = f".\Data\{ProductNameToBeSearched}.csv"


        if os.path.exists(file_path):
            print("File exists, appending data.")
            df.to_csv(file_path, mode="a", header=False, index=False, encoding="utf-8", errors="replace")
        else:
            print("File does not exist, creating file and writing data.")
            df.to_csv(file_path, mode="w", header=True, index=False, encoding="utf-8", errors="replace")

        # Stop the main loop if an error occurs or scraping finishes
        stop_flag = True

# Thread to run the scraper
scraper_thread = threading.Thread(target=scrape_products)

# Start the scraper thread
scraper_thread.start()

# Listen for key presses to control the scraper
while True:
    if stop_flag:
        print("Terminating program.")
        break

    if keyboard.is_pressed('p'):  # Press 'p' to pause
        pause_event.clear()
        print("Pause key pressed.")

    elif keyboard.is_pressed('r'):  # Press 'r' to resume
        pause_event.set()
        print("Resume key pressed.")

    elif keyboard.is_pressed('s'):  # Press 's' to stop
        stop_flag = True
        pause_event.set()  # Ensure it's not paused when stopping
        print("Stop key pressed.")
        break

    time.sleep(0.1)  # Short delay to prevent high CPU usage
