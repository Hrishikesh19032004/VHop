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
    "morth_vehicle_regulations": "https://morth.nic.in/sites/default/files/ASI/53201963840PMAIS_137_Part_4_F.pdf",
    "morth_safety_committee_report": "https://morth.nic.in/sites/default/files/Click_for_the_Sundar_Committee_Report",
    "morth_safety_working_groups": "https://morth.nic.in/sites/default/files/Synthesis_Report_of_four_Working_Groups_on_Road_Safety.pdf",
    "morth_safety_engg_vehicles": "https://morth.nic.in/sites/default/files/Report_of_WG_on_Engg_Vehicles-2296564859.pdf",
    "morth_driving_training_guidelines": "https://morth.nic.in/sites/default/files/circulars_document/Revised-scheme-guidelines-for-setting-up-merged.pdf",
    "morth_ev_charging_notification": "https://morth.nic.in/sites/default/files/notifications_document/Notification-EV-Charging-Infra.pdf",
    "morth_draft_ev_policy": "https://morth.nic.in/sites/default/files/notifications_document/Draft-Electric-Mobility-Policy.pdf"
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
