import os
import time
import csv
from urllib.parse import urlparse, urljoin
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup

ev_keywords = ["ev", "electric vehicle", "battery", "charging", "electric mobility", "e-vehicle", "emobility"]

websites = {
    "spinny": "https://www.spinny.com/used-tata-nexon-ev-cars/",
        "cars24": "https://www.cars24.com/buy-used-electric-cars/",
        "olx_query1": "https://www.olx.in/items/q-electric-car",
}

def contains_ev_keywords(text):
    text = text.lower()
    return any(kw in text for kw in ev_keywords)

def setup_driver():
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--log-level=3")
    return webdriver.Chrome(options=options)

def get_sub_links(base_url, soup, limit=5):
    sub_links = set()
    base_domain = urlparse(base_url).netloc
    for link in soup.find_all('a', href=True):
        href = link['href']
        full_url = urljoin(base_url, href)
        if base_domain in full_url and full_url != base_url and full_url not in sub_links:
            sub_links.add(full_url)
        if len(sub_links) >= limit:
            break
    return list(sub_links)

def scrape_page_content(driver, url):
    data = []
    try:
        driver.get(url)
        time.sleep(2)
        soup = BeautifulSoup(driver.page_source, "html.parser")
        title = soup.title.string.strip() if soup.title else ""
        body_text = soup.get_text(separator=' ', strip=True)

        if contains_ev_keywords(body_text):
            data.append([url, title, body_text])
    except Exception as e:
        print(f"Error scraping {url}: {e}")
    return data

def scrape_with_subpages(name, url):
    driver = setup_driver()
    all_data = []
    try:
        driver.get(url)
        time.sleep(2)
        soup = BeautifulSoup(driver.page_source, "html.parser")

        all_data.extend(scrape_page_content(driver, url))

        sub_links = get_sub_links(url, soup)
        for sub_url in sub_links:
            all_data.extend(scrape_page_content(driver, sub_url))

    finally:
        driver.quit()

    return all_data

def save_to_csv(folder, filename, data):
    os.makedirs(folder, exist_ok=True)
    filepath = os.path.join(folder, filename)
    with open(filepath, "w", newline='', encoding="utf-8") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["URL", "Title", "EV_Content"])
        writer.writerows(data)
    return filepath

for name, url in websites.items():
    print(f"Scraping category: {name} ({url})")
    domain_folder = urlparse(url).netloc.replace("www.", "")
    full_folder = os.path.join("scraped_data", domain_folder, name)
    result = scrape_with_subpages(name, url)

    if result:
        csv_path = save_to_csv(full_folder, f"{name}.csv", result)
        print(f"Saved {len(result)} EV-related entries to {csv_path}")
    else:
        print(f"No EV-related content found for {name}")
