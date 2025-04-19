from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import time
import csv

# Setup headless Chrome
chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--no-sandbox")

# Initialize WebDriver
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

# Open URL
url = "https://www.plugshare.com/location/357525"
driver.get(url)

# Wait until the reviews section loads
try:
    WebDriverWait(driver, 15).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, '.review-container'))  # Replace with real class
    )
except:
    print("Review section not found.")

# Scroll to load more reviews (if needed)
last_height = driver.execute_script("return document.body.scrollHeight")
while True:
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(2)
    new_height = driver.execute_script("return document.body.scrollHeight")
    if new_height == last_height:
        break
    last_height = new_height

# Extract reviews
reviews = []
review_elements = driver.find_elements(By.CSS_SELECTOR, '.review')  # Replace with correct selector
for review in review_elements:
    try:
        user = review.find_element(By.CSS_SELECTOR, '.user-name').text
        rating = review.find_element(By.CSS_SELECTOR, '.rating').text
        comment = review.find_element(By.CSS_SELECTOR, '.comment').text
        reviews.append({
            "User": user,
            "Rating": rating,
            "Comment": comment,
        })
    except:
        continue

# Save to CSV
if reviews:
    with open("reviews.csv", "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["User", "Rating", "Comment"])
        writer.writeheader()
        for review in reviews:
            writer.writerow(review)
    print("Reviews saved to reviews.csv")

driver.quit()
