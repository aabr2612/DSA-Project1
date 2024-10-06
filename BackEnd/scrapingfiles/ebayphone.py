import os  # Import os to check if the file exists
import re
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
chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")

driver = webdriver.Chrome(service=service, options=chrome_options)

# Initialize lists to store extracted data
products = []
prices = []
ratings = []
watchers = []
product_countries = []
discounts = []
shipping_prices = []
conditions = []
seller_names = []
seller_sold_products = []
seller_ratings = []

for i in range(1, 43):
    driver.get(
        f"https://www.ebay.com/sch/i.html?_from=R40&_nkw=phone&_sacat=0&_ipg=240&_pgn={i}&rt=nc"
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

        seller_info_span = a.find("span", attrs={"class": "s-item__seller-info-text"})
        if seller_info_span:
            seller_info_text = seller_info_span.text.strip()
            # Using regular expressions to capture the parts
            match = re.match(r"(.+?)\s\(([\d,]+)\)\s([\d.]+%)", seller_info_text)
            if match:
                seller_name = match.group(1).strip()
                seller_product = match.group(2).replace(",", "")
                seller_rating = match.group(3)
                seller_product = int(seller_product)  # Optionally, convert to integer
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
            price_numeric = re.sub(r"[^\d]", "", price.text)
            prices.append(int(price_numeric) if price_numeric else 0)
            ratings.append(ratingspan.text if ratingspan else "Not available")
            product_countries.append(country.text if country else "Not available")
            # Modify the line as follows
            if shipping:
                shipping_price_text = re.sub(r"[^\d]", "", shipping.text)
                shipping_price = int(shipping_price_text) if shipping_price_text.isdigit() else 0
            else:
                shipping_price = 0
            shipping_prices.append(shipping_price)

            watchers.append(watcher.text if watcher else "Not available")
            discounts.append(discount.text if discount else "Not available")
            conditions.append(condition.text if condition else "Not available")
            seller_names.append(seller_name)
            seller_sold_products.append(seller_product)
            seller_ratings.append(seller_rating)

# Create and save the DataFrame if there's data
if products:
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

    # Check if the CSV file already exists
    file_exists = os.path.isfile("TotalData.csv")

    # Write to the CSV file
    df.to_csv("TotalData.csv", mode="a", header=not file_exists, index=False, encoding="utf-8", errors="replace")

driver.quit()
