import requests
from bs4 import BeautifulSoup
import pandas as pd

ev_urls = [
    "https://morth.nic.in/sites/default/files/circulars_document/Incentivisation_of_Electric.pdf",
    "https://morth.nic.in/sites/default/files/ASI/320201825106PMAIS_138_Part_2_F.pdf",
    "https://morth.nic.in/sites/default/files/Finalized_Draft_AIS_138_Part_1_October_2016_for_Electric.pdf",
    "https://morth.nic.in/sites/default/files/ASI/5-AIS%20174_Electric_CEV-Specific%20Requirements.pdf",
    "https://morth.nic.in/sites/default/files/ASI/PUB_4_9_2010_2_14_36_PM_AIS-102%28Part2%29F.pdf",
    "https://morth.nic.in/sites/default/files/circulars_document/Policy%20Guidelines%20for%20Development%20of%20Wayside%20Amenities%20along%20NHs%20and%20Expressways%20%281%29.pdf"
]

titles = [
    "Incentivization of Electric Vehicles – Permit Relaxation",
    "AIS 138 Part 2 – DC EV Charging Standards",
    "AIS 138 Part 1 – AC EV Charging Standards",
    "AIS 174 – Electric Construction Equipment Vehicle Standards",
    "AIS 102 Part 2 – Hybrid Electric Vehicle Type Approval",
    "Wayside Amenities – Guidelines including EV Charging Infrastructure"
]

data = []

for title, url in zip(titles, ev_urls):
    data.append({
        "Title": title,
        "URL": url,
        "Source": "MoRTH",
        "Category": "Electric Vehicle Policy/Standards"
    })

df = pd.DataFrame(data)
df.to_csv("MoRTH_EV_Policies.csv", index=False)

print("Scraped data stored in 'MoRTH_EV_Policies.csv'")
