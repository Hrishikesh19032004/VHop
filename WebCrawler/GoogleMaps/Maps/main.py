import requests
import csv
import math
import time

API_KEY = '17c6fb022f3df62879da64cfd57a29e75ef0112e23b3ecbec295bd39c023f87e'  

locations = [
    {"lat": 27.96598624, "lng": 76.38014493},
    {"lat": 27.001655, "lng": 75.87600311}
]

def haversine(lat1, lon1, lat2, lon2):
    R = 6371000
    phi1 = math.radians(lat1)
    phi2 = math.radians(lat2)
    delta_phi = math.radians(lat2 - lat1)
    delta_lambda = math.radians(lon2 - lon1)
    a = math.sin(delta_phi / 2.0) ** 2 + math.cos(phi1) * math.cos(phi2) * math.sin(delta_lambda / 2.0) ** 2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return R * c

def get_nearest_stations(lat, lng):
    params = {
        "engine": "google_maps",
        "q": "filling station",
        "ll": f"@{lat},{lng},16z",
        "type": "search",
        "api_key": API_KEY
    }
    try:
        response = requests.get("https://serpapi.com/search.json", params=params)
        response.raise_for_status()
        data = response.json()
    except Exception as e:
        print("Error fetching stations:", e)
        return []

    places = data.get("local_results", []) or data.get("places_results", [])
    if not places:
        print(f"No stations found by Google Maps near {lat}, {lng}")
        return []

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
                    "Distance_meters": round(dist, 2),
                    "data_id": place.get("data_id"),
                    "place_id": place.get("place_id")
                })
    return results

def get_reviews(data_id, place_id):
    params = {
        "engine": "google_maps_reviews",
        "data_id": data_id,
        "place_id": place_id,
        "api_key": API_KEY
    }
    try:
        response = requests.get("https://serpapi.com/search.json", params=params)
        response.raise_for_status()
        data = response.json()
    except Exception as e:
        print(f"Error fetching reviews for {data_id}: {e}")
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

all_stations = []
all_reviews = []

for loc in locations:
    stations = get_nearest_stations(loc["lat"], loc["lng"])
    print(f"Found {len(stations)} stations near {loc['lat']},{loc['lng']}")
    for s in stations:
        all_stations.append(s)
        data_id = s.get("data_id")
        place_id = s.get("place_id")
        if data_id and place_id:
            reviews_batch = get_reviews(data_id, place_id)
            print(f"Fetched {len(reviews_batch)} reviews for {s.get('Name')}")
            all_reviews.extend(reviews_batch)
            time.sleep(1.5)

if all_stations:
    with open("stations_within_radius.csv", "w", newline="", encoding="utf-8") as f1:
        writer = csv.DictWriter(f1, fieldnames=all_stations[0].keys())
        writer.writeheader()
        for row in all_stations:
            writer.writerow(row)
    print("Station data saved to stations_within_radius.csv")

if all_reviews:
    with open("station_reviews.csv", "w", newline="", encoding="utf-8") as f2:
        writer = csv.DictWriter(f2, fieldnames=all_reviews[0].keys())
        writer.writeheader()
        for review in all_reviews:
            writer.writerow(review)
    print("Review data saved to station_reviews.csv")
