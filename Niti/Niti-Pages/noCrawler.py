from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import csv
import time

ev_keywords = ["ev", "electric vehicle", "battery", "charging", "electric mobility", "e-vehicle", "emobility"]

websites = {
    "niti": "https://e-amrit.niti.gov.in/benefits-of-electric-vehicles"
}
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import csv
import time

ev_keywords = ["ev", "electric vehicle", "battery", "charging", "electric mobility", "e-vehicle", "emobility"]

websites = {
    
  "benefits": "https://e-amrit.niti.gov.in/benefits-of-electric-vehicles",
  "myths": "https://e-amrit.niti.gov.in/busting-common-electric-vehicle-myths",
  "types": "https://e-amrit.niti.gov.in/types-of-electric-vehicles",
  "financing_options": "https://e-amrit.niti.gov.in/financing-options",
  "insurance_options": "https://e-amrit.niti.gov.in/insurance-options",
  "incentives": "https://e-amrit.niti.gov.in/electric-vehicle-incentives",
  "zevtc_declaration": "https://e-amrit.niti.gov.in/zevtc-declaration",
  "business_models": "https://e-amrit.niti.gov.in/business-models",
  "manufacturers": "https://e-amrit.niti.gov.in/Manufacturers",
  "service_providers": "https://e-amrit.niti.gov.in/service-providers",
  "new_businesses": "https://e-amrit.niti.gov.in/new-e-mobility-businesses",
  "invest_india": "https://e-amrit.niti.gov.in/invest-india",
  "vehicle_selector": "https://e-amrit.niti.gov.in/choose-my-electric-vehicle",
  "home_charging_calculator": "https://e-amrit.niti.gov.in/home-charging-calculator",
  "public_charging_calculator": "https://e-amrit.niti.gov.in/public-charging-calculator",
  "journey_cost_calculator": "https://e-amrit.niti.gov.in/journey-cost-calculator",
  "co2_calculator": "https://e-amrit.niti.gov.in/co2-calculator",
  "tax_savings_calculator": "https://e-amrit.niti.gov.in/tax-savings-calculator",
  "crude_oil_savings_calculator": "https://e-amrit.niti.gov.in/crude-oil-savings-calculator",
  "charging_station_locators": "https://e-amrit.niti.gov.in/charging-station-locators",
  "national_policy": "https://e-amrit.niti.gov.in/national-level-policy",
  "state_policies": "https://e-amrit.niti.gov.in/state-level-policies",
  "charging_cost": "https://e-amrit.niti.gov.in/electricity-cost-for-charging",
  "standards_specifications": "https://e-amrit.niti.gov.in/standards-and-specifications",
  "reports_articles": "https://e-amrit.niti.gov.in/reports-and-articles",
  "media": "https://e-amrit.niti.gov.in/media",
  "useful_links": "https://e-amrit.niti.gov.in/useful-links",
  "skill_center": "https://e-amrit.niti.gov.in/skill-center",
  "international_best_practices": "https://e-amrit.niti.gov.in/international-best-practices-on-policies",
  "ev_awareness_portal": "https://e-amrit.niti.gov.in/ev-awareness-web-portal/"


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

for name, url in websites.items():
    print(f"🔍 Scraping single page: {name} ({url})")
    result = scrape_single_page(url)

    filename = f"{name}.csv"
    with open(filename, "w", newline='', encoding="utf-8") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["URL", "Title", "EV_Content"])
        writer.writerows(result)

    print(f" Saved {len(result)} EV-related entries to {filename}")

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

for name, url in websites.items():
    print(f"🔍 Scraping single page: {name} ({url})")
    result = scrape_single_page(url)

    filename = f"{name}.csv"
    with open(filename, "w", newline='', encoding="utf-8") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["URL", "Title", "EV_Content"])
        writer.writerows(result)

    print(f" Saved {len(result)} EV-related entries to {filename}")
