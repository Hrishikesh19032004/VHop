import requests
from bs4 import BeautifulSoup
import csv
import time

headers = {
    'User-Agent': 'Mozilla/5.0'
}
base_search_url = 'https://www.data.gov.in/search?title=ev&type=resources&sortby=_score'
base_site_url = 'https://data.gov.in'

def get_dataset_links(search_url):
    res = requests.get(search_url, headers=headers)
    soup = BeautifulSoup(res.content, 'html.parser')

    dataset_links = []
    cards = soup.select('.search-result .title a')
    
    for card in cards:
        link = base_site_url + card['href']
        dataset_links.append(link)
    
    return dataset_links

def extract_csv_links(dataset_url):
    res = requests.get(dataset_url, headers=headers)
    soup = BeautifulSoup(res.content, 'html.parser')
    csv_links = []

    for a in soup.find_all('a', href=True):
        href = a['href']
        if href.endswith('.csv'):
            csv_links.append(href)

    return csv_links

# Fetch dataset pages
dataset_pages = get_dataset_links(base_search_url)

# Open CSV writer
with open("ev_datasets_data_gov.csv", "w", newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
    writer.writerow(['Dataset Page', 'CSV Link'])

    for page_url in dataset_pages:
        print(f"🔍 Checking: {page_url}")
        try:
            csvs = extract_csv_links(page_url)
            for csv_link in csvs:
                writer.writerow([page_url, csv_link])
        except Exception as e:
            print(f"❌ Failed for {page_url}: {e}")
        
        time.sleep(1)  # avoid hammering the site

print("✅ Done! Saved to ev_datasets_data_gov.csv")
