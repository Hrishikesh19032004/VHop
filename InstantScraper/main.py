from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from bs4 import BeautifulSoup
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import time

# Define URLs to scrape
urls = [
    "https://e-amrit.niti.gov.in/home",
    "https://siam.in",
    "https://smev.in",
    
]

options = Options()
options.add_argument("--headless")
options.add_argument("--disable-gpu")
options.add_argument("--window-size=1920,1080")

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

# Data containers for each category
policy_data = []
roadmap_data = []
subsidy_data = []
infrastructure_data = []
sales_data = []

# Function to extract tables and categorize the data
def extract_tables(soup, base_url):
    tables = soup.find_all("table")
    page_data = []
    for table in tables:
        rows = table.find_all("tr")
        for row in rows:
            cols = [col.get_text(strip=True) for col in row.find_all(['td', 'th'])]
            if cols:
                page_data.append([base_url] + cols)
    return page_data

# Function to extract data related to specific descriptions
def extract_descriptions(soup, base_url):
    # Define keywords for different categories
    keywords = {
        "policy": ["official policy", "regulation", "policy document", "transportation policy"],
        "roadmap": ["EV roadmap", "future plans", "EV plans"],
        "subsidy": ["subsidy", "government incentives", "financial support", "FAME scheme"],
        "infrastructure": ["charging stations", "EV infrastructure", "charging points", "EV stations"],
        "sales": ["EV sales", "vehicle sales", "adoption rate", "market share"]
    }

    descriptions = soup.find_all(["p", "div", "section"])
    categorized_data = {
        "policy": [],
        "roadmap": [],
        "subsidy": [],
        "infrastructure": [],
        "sales": []
    }

    for desc in descriptions:
        text = desc.get_text(strip=True)
        if text:
            for category, cat_keywords in keywords.items():
                if any(keyword.lower() in text.lower() for keyword in cat_keywords):
                    categorized_data[category].append({"url": base_url, "description": text})

    return categorized_data

# Function to extract article links
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

# Scrape the website
for base_url in urls:
    try:
        driver.get(base_url)
        time.sleep(5)
        soup = BeautifulSoup(driver.page_source, "html.parser")

        # Extract tables
        table_data = extract_tables(soup, base_url)
        if table_data:
            print(f"Extracted {len(table_data)} table rows from {base_url}")

        # Extract descriptions and categorize them
        categorized_data = extract_descriptions(soup, base_url)
        
        # Add data to respective categories
        policy_data.extend(categorized_data["policy"])
        roadmap_data.extend(categorized_data["roadmap"])
        subsidy_data.extend(categorized_data["subsidy"])
        infrastructure_data.extend(categorized_data["infrastructure"])
        sales_data.extend(categorized_data["sales"])

    except Exception as e:
        print(f"Error scraping {base_url}: {str(e)}")

driver.quit()

# Save each category to a separate CSV file
def save_to_csv(data, filename):
    if data:
        df = pd.DataFrame(data)
        df.to_csv(filename, index=False)
        print(f"Data saved to {filename}")
    else:
        print(f"No data extracted for {filename}")

# Save data in separate CSV files
save_to_csv(policy_data, "policy_data.csv")
save_to_csv(roadmap_data, "roadmap_data.csv")
save_to_csv(subsidy_data, "subsidy_data.csv")
save_to_csv(infrastructure_data, "infrastructure_data.csv")
save_to_csv(sales_data, "sales_data.csv")
