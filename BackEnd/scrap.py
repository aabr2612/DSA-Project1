import os
import re
import threading
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import pandas as pd
from PyQt5.QtCore import pyqtSignal, QObject


class ScraperThread(QObject):
    progress_signal = pyqtSignal(int)

    def __init__(self, product_name, total_pages):
        super().__init__()
        self.product_name = product_name
        self.total_pages = total_pages
        self.driver = None
        self.thread = None
        self.stop_flag = threading.Event()
        self.pause_event = threading.Event()
        self.pause_event.set()

    def setup_driver(self):
        service = Service("C:/Program Files (x86)/chromedriver-win64/chromedriver.exe")
        chrome_options = Options()
        chrome_options.add_argument("--ignore-certificate-errors")
        chrome_options.add_argument("--ignore-ssl-errors")
        chrome_options.add_argument("--disable-web-security")
        chrome_options.add_argument("--allow-running-insecure-content")
        chrome_options.add_argument(
            "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        )
        self.driver = webdriver.Chrome(service=service, options=chrome_options)

    def scrape_products(self):
        products, prices, ratings, watchers, product_countries, discounts = [], [], [], [], [], []
        shipping_prices, conditions, seller_names, seller_sold_products, seller_ratings = [], [], [], [], []

        try:
            self.setup_driver()

            for i in range(1, self.total_pages + 1):
                if self.stop_flag.is_set():
                    print("Scraping has been stopped.")
                    break

                while not self.pause_event.is_set():
                    print("Scraping is paused...")
                    time.sleep(1)

                self.driver.get(
                    f"https://www.ebay.com/sch/i.html?_from=R40&_nkw={self.product_name}&_sacat=0&_ipg=240&_pgn={i}&rt=nc"
                )
                soup = BeautifulSoup(self.driver.page_source, "html.parser")

                for a in soup.find_all("li", attrs={"class": "s-item s-item__pl-on-bottom"}):
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

                    if name and price:
                        products.append(name.text.strip() if name else "Not available")

                        price_numeric = re.sub(r"[^\d]", "", price.text)
                        try:
                            prices.append(int(price_numeric) if price_numeric else 0)
                        except ValueError:
                            prices.append(0)

                        ratings.append(ratingspan.text if ratingspan else "Not available")
                        product_countries.append(country.text if country else "Not available")

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

                progress = int((i / self.total_pages) * 100)
                self.progress_signal.emit(progress)

        except Exception as e:
            print(f"Error occurred: {e}")

        finally:
            if self.driver:
                self.driver.quit()

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

            file_path = f"./backend/data/{self.product_name}.csv"
            if os.path.exists(file_path):
                print("File exists, appending data.")
                df.to_csv(file_path, mode="a", header=False, index=False, encoding="utf-8", errors="replace")
            else:
                print("File does not exist, creating file and writing data.")
                df.to_csv(file_path, mode="w", header=True, index=False, encoding="utf-8", errors="replace")

    def start(self):
        self.thread = threading.Thread(target=self.scrape_products)
        self.thread.start()

    def stop(self):
        self.stop_flag.set()

    def pause(self):
        self.pause_event.clear()

    def resume(self):
        self.pause_event.set()