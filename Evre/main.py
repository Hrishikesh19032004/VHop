import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import csv
import os
import re
import time

websites = {
    "EV Battery": "https://evreporter.com/tag/ev-battery/",
    
}





ev_keywords = ["ev", "electric vehicle", "battery", "charging", "electric mobility", "e-vehicle", "emobility"]


def contains_ev_keywords(text):
    text = text.lower()
    return any(kw in text for kw in ev_keywords)


def crawl_site(base_url, domain_name, max_pages=10):
    visited = set()
    to_visit = [base_url]
    all_data = []

    while to_visit and len(visited) < max_pages:
        url = to_visit.pop(0)
        if url in visited:
            continue
        visited.add(url)

        try:
            response = requests.get(url, timeout=10)
            if response.status_code != 200:
                continue
            soup = BeautifulSoup(response.text, "html.parser")

            
            title = soup.title.string.strip() if soup.title else ""
            body_text = soup.get_text(separator=' ', strip=True)
            if contains_ev_keywords(body_text):
                all_data.append([url, title, body_text[:500]])  

            
            for link_tag in soup.find_all("a", href=True):
                href = link_tag["href"]
                full_url = urljoin(url, href)
                if urlparse(full_url).netloc == urlparse(base_url).netloc:
                    if full_url not in visited:
                        to_visit.append(full_url)

            time.sleep(1)
        except Exception as e:
            print(f"Error visiting {url}: {e}")

    return all_data


for name, base_url in websites.items():
    print(f"🔍 Crawling: {name} ({base_url})")
    scraped_data = crawl_site(base_url, name)

    
    filename = f"{name}_ev_data.csv"
    with open(filename, "w", newline='', encoding="utf-8") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["URL", "Title", "EV_Content"])
        writer.writerows(scraped_data)

    print(f" Saved {len(scraped_data)} EV-related entries to {filename}")
