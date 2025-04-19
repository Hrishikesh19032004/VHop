from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from bs4 import BeautifulSoup
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import time

urls = [
    "https://www.team-bhp.com/"
]

options = Options()
options.add_argument("--headless")
options.add_argument("--disable-gpu")
options.add_argument("--window-size=1920,1080")

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

all_data = []
article_limit = 100
article_count = 0

def extract_article_data(article_url):
    global article_count
    try:
        driver.get(article_url)
        time.sleep(3)
        soup = BeautifulSoup(driver.page_source, "html.parser")
        
        title = soup.find("h1").get_text(strip=True) if soup.find("h1") else "No title"
        date = soup.find("time").get_text(strip=True) if soup.find("time") else "No date"
        content = soup.find("div", class_="entry-content")
        
        article_content = content.get_text(strip=True) if content else "No content"
        
        article_count += 1
        return {
            "url": article_url,
            "title": title,
            "date": date,
            "content": article_content
        }
    
    except Exception as e:
        return None

def extract_article_links_from_page(url):
    driver.get(url)
    time.sleep(3)
    
    soup = BeautifulSoup(driver.page_source, "html.parser")
    
    article_links = []
    articles = soup.find_all("a", href=True)
    
    for article in articles:
        link = article["href"]
        if "/news/" in link:
            full_link = url + link if link.startswith("/") else link
            article_links.append(full_link)
    
    return article_links

def go_to_next_page():
    try:
        next_button = driver.find_element(By.CSS_SELECTOR, ".next-page-class")
        if next_button.is_enabled():
            next_button.click()
            time.sleep(5)
            return True
        else:
            return False
    except Exception as e:
        return False

for base_url in urls:
    page_num = 1
    
    while True:
        article_links = extract_article_links_from_page(base_url)
        if not article_links or article_count >= article_limit:
            break
        
        for article_url in article_links:
            if article_count >= article_limit:
                break
            article_data = extract_article_data(article_url)
            if article_data:
                all_data.append(article_data)
        
        if not go_to_next_page() or article_count >= article_limit:
            break
        
        page_num += 1

driver.quit()

if all_data:
    df = pd.DataFrame(all_data)
    df.to_csv("team_bhp_scraped_data.csv", index=False)
else:
    print("No data extracted.")
