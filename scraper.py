import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime

def scrape_api_update_date(url, date_selector):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    date_element = soup.select_one(date_selector)
    if date_element:
        return date_element.text.strip()
    return None

# List of APIs to scrape (add more as needed)
apis = [
    {
        "name": "GitHub REST API",
        "url": "https://docs.github.com/en/rest",
        "selector": ".last-updated"
    },
    {
        "name": "Twitter API",
        "url": "https://developer.twitter.com/en/docs/twitter-api",
        "selector": ".last-updated"
    },
    # Add more APIs here
]

results = []

for api in apis:
    update_date = scrape_api_update_date(api['url'], api['selector'])
    results.append({
        "name": api['name'],
        "url": api['url'],
        "last_updated": update_date,
        "scraped_at": datetime.now().isoformat()
    })

# Save results to a CSV file
df = pd.DataFrame(results)
df.to_csv("api_update_dates.csv", index=False)

print("Scraping completed. Results saved to api_update_dates.csv")
