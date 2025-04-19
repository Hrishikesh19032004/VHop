import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import csv
import time

ev_keywords = ["ev", "electric vehicle", "battery", "charging", "electric mobility", "e-vehicle", "emobility"]

websites = {
    "fame2": "https://fame2.heavyindustries.gov.in",
    "autocar": "https://www.autocarindia.com/car-news/electric-cars",
    "financialexpress_ev": "https://www.financialexpress.com/auto/electric-vehicles/",
    "reddit_evindia": "https://www.reddit.com/r/EVIndia/",
    "expwithevs": "https://www.expwithevs.in/",
    "quora_ev": "https://www.quora.com/topic/Electric-Vehicles-in-India",
    "evspecs": "https://www.evspecs.org/electric-cars-battery-gross-capacity-comparison-chart",
    "pluginindia": "https://www.pluginindia.com/",
    "facebook_evgroup": "https://www.facebook.com/groups/402353732097600/",
    "evpedia": "https://www.evpedia.co.in/ev-news",
    "teambhp": "https://www.team-bhp.com/forum/electric-cars/",
    "reddit_evsearch": "https://www.reddit.com/r/electricvehicles/search/?q=India&cId=246bd653-2a94-454c-80aa-6a46bc27265f&iId=d76f1206-419d-4d93-a961-f9fdc3c34e68",
    "evindia_news": "https://evindia.online/news",
    "hindustan_ev": "https://auto.hindustantimes.com/auto/electric-vehicles",
    "evstory": "https://evstory.in/",
    "evreporter": "https://evreporter.com/",
    "cardekho_upcoming_ev": "https://www.cardekho.com/upcomingcars/electric",
    "carwale_new_ev": "https://www.carwale.com/new/electric-cars/",
    "wikipedia_ola": "https://en.wikipedia.org/wiki/Ola_Electric",
    "reuters_greenline": "https://www.reuters.com/sustainability/climate-energy/indias-greenline-mobility-invest-275-million-decarbonize-heavy-truck-fleet-2025-04-10/",
    "ft_skoda": "https://www.ft.com/content/a730b0b8-b009-4b19-a83c-fc4f54e68f1f",
    "reuters_skoda": "https://www.reuters.com/business/autos-transportation/vws-skoda-invest-manufacturing-evs-india-despite-14-bln-tax-demand-overhang-2025-03-14/",
    "wikipedia_wardwizard": "https://en.wikipedia.org/wiki/Wardwizard_Innovations_%26_Mobility_Limited",
    "evtechnews": "https://evtechnews.in/",
    "economictimes_ev": "https://economictimes.indiatimes.com/topic/ev",
    "reuters_tradecut": "https://www.reuters.com/world/india/india-backs-ev-tariff-cuts-trump-trade-deal-defying-autos-lobby-sources-say-2025-04-02/",
    "businessinsider_byd": "https://www.businessinsider.com/byd-just-got-blocked-from-selling-evs-in-india-2025-4",
    "tatamotors_evolve": "https://evolve.tatamotors.com/events/previous",
    "spinny": "https://www.spinny.com/used-tata-nexon-ev-cars/",
    "cars24": "https://www.cars24.com/buy-used-electric-cars/",
    "olx_ev": "https://www.olx.in/items/q-electric-car"
}



def contains_ev_keywords(text):
    text = text.lower()
    return any(kw in text for kw in ev_keywords)

def setup_driver():
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--log-level=3")
    return webdriver.Chrome(options=chrome_options)

def scrape_single_page(url):
    driver = setup_driver()
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
    finally:
        driver.quit()
    return data


folder_name = "scraped_data"
os.makedirs(folder_name, exist_ok=True)

for name, url in websites.items():
    print(f" Scraping single page: {name} ({url})")
    
    result = scrape_single_page(url)

    filename = os.path.join(folder_name, f"{name}.csv")
    with open(filename, "w", newline='', encoding="utf-8") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["URL", "Title", "EV_Content"])
        writer.writerows(result)

    print(f"Saved {len(result)} EV-related entries to {filename}")
