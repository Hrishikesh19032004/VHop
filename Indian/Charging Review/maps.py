import requests
import csv
import math
import time
import re

API_KEY = '17c6fb022f3df62879da64cfd57a29e75ef0112e23b3ecbec295bd39c023f87e'

def extract_coordinates_from_url(url):
    match = re.search(r'@([-+]?\d*\.\d+),([-+]?\d*\.\d+)', url)
    if match:
        lat, lng = float(match.group(1)), float(match.group(2))
        print(f"Extracted coordinates: {lat}, {lng}")
        return lat, lng
    print("Could not extract coordinates from URL.")
    return None, None

def haversine(lat1, lon1, lat2, lon2):
    R = 6371000
    phi1 = math.radians(lat1)
    phi2 = math.radians(lat2)
    delta_phi = math.radians(lat2 - lat1)
    delta_lambda = math.radians(lon2 - lon1)
    a = math.sin(delta_phi / 2.0) ** 2 + math.cos(phi1) * math.cos(phi2) * math.sin(delta_lambda / 2.0) ** 2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return R * c

def get_ev_chargers(lat, lng):
    params = {
        "engine": "google_maps",
        "q": "ev charging station",
        "ll": f"@{lat},{lng},16z",
        "type": "search",
        "api_key": API_KEY
    }
    try:
        response = requests.get("https://serpapi.com/search.json", params=params)
        response.raise_for_status()
        data = response.json()
    except Exception as e:
        print("Error fetching EV chargers:", e)
        return []

    places = data.get("local_results", []) or data.get("places_results", [])
    results = []
    for place in places:
        coords = place.get("gps_coordinates", {})
        lat2 = coords.get("latitude")
        lng2 = coords.get("longitude")
        if lat2 and lng2:
            dist = haversine(lat, lng, lat2, lng2)
            if dist <= 2000:
                results.append({
                    "Name": place.get("title"),
                    "Rating": place.get("rating"),
                    "Reviews": place.get("reviews"),
                    "Type": place.get("type", ""),
                    "Address": place.get("address", ""),
                    "Link": place.get("link", ""),
                    "Latitude": lat2,
                    "Longitude": lng2,
                    "Distance_meters": round(dist, 2)
                })
    return results

def get_reviews_from_link(link):
    params = {
        "engine": "google_maps_reviews",
        "hl": "en",
        "link": link,
        "api_key": API_KEY
    }
    try:
        response = requests.get("https://serpapi.com/search.json", params=params)
        response.raise_for_status()
        data = response.json()
    except Exception as e:
        print(f"Error fetching reviews for link {link}: {e}")
        return []

    reviews = []
    for r in data.get("reviews", [])[:50]:
        reviews.append({
            "User": r.get("user", ""),
            "Rating": r.get("rating", ""),
            "Snippet": r.get("snippet", ""),
            "Date": r.get("date", ""),
            "Place Name": data.get("place_info", {}).get("title", "")
        })
    return reviews

# --- Main Execution ---

url = "https://www.google.com/maps/place//@19.16645,72.8869927,15z"
latitude, longitude = extract_coordinates_from_url(url)

if latitude and longitude:
    all_chargers = get_ev_chargers(latitude, longitude)
    all_reviews = []

    print(f"Found {len(all_chargers)} EV chargers nearby.")

    for charger in all_chargers:
        link = charger.get("Link")
        name = charger.get("Name")
        if link:
            reviews = get_reviews_from_link(link)
            print(f"Fetched {len(reviews)} reviews for {name}")
            all_reviews.extend(reviews)
            time.sleep(2)  # be nice to the API

    if all_chargers:
        with open("ev_chargers_within_radius.csv", "w", newline="", encoding="utf-8") as f1:
            writer = csv.DictWriter(f1, fieldnames=all_chargers[0].keys())
            writer.writeheader()
            for row in all_chargers:
                writer.writerow(row)
        print("Station data saved to ev_chargers_within_radius.csv")

    if all_reviews:
        with open("ev_charger_reviews.csv", "w", newline="", encoding="utf-8") as f2:
            writer = csv.DictWriter(f2, fieldnames=all_reviews[0].keys())
            writer.writeheader()
            for review in all_reviews:
                writer.writerow(review)
        print("Review data saved to ev_charger_reviews.csv")
