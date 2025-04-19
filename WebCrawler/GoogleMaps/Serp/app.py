import requests
import csv
import time

cities = ["Mumbai", "Delhi", "Bengaluru", "Chennai", "Hyderabad", "Kolkata", "Pune"]

api_key = "17c6fb022f3df62879da64cfd57a29e75ef0112e23b3ecbec295bd39c023f87e"

for city in cities:
    print(f"Fetching EV charger data for {city}...")
    params = {
        "engine": "google_maps",
        "type": "search",
        "q": f"EV chargers near {city}",
        "api_key": api_key
    }

    response = requests.get("https://serpapi.com/search", params=params)
    data = response.json()

    filename = f"ev_chargers_{city.lower()}.csv"

    with open(filename, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(["Title", "Address", "Rating"])

        for place in data.get('local_results', []):
            title = place.get('title', '')
            address = place.get('address', '')
            rating = place.get('rating', 'N/A')
            writer.writerow([title, address, rating])

    print(f"Data for {city} saved to {filename}")
    
    time.sleep(2)  
