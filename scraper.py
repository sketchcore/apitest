import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime
import csv

def scrape_api_update_date(url, date_selector):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    date_element = soup.select_one(date_selector)
    if date_element:
        return date_element.text.strip()
    return None

def format_date(raw_date):
    # Normalize the date formats
    try:
        # Remove HTML non-breaking spaces
        raw_date = raw_date.replace('\xa0', ' ')  # Replace non-breaking space with a regular space
        
        # Check for different formats and parse accordingly
        if "latest" in raw_date:
            # Example: "2022-11-28 (latest)"
            date_str = raw_date.split(" ")[0]  # Get the date part
            date_obj = datetime.strptime(date_str, "%Y-%m-%d")
        else:
            # Handle other formats
            date_obj = datetime.strptime(raw_date, "%B %d, %Y")  # Example: "September 3, 2024"
        
        return date_obj.strftime("%Y-%m-%d")  # Uniform format: YYYY-MM-DD
    except ValueError:
        return raw_date  # Return the raw date if parsing fails

# Read API configurations from CSV
apis = []
with open('apitest/api_config.csv', mode='r') as file:  # Updated path
    reader = csv.DictReader(file)
    for row in reader:
        apis.append({
            "name": row['name'],
            "url": row['url'],
            "selector": row['selector']
        })

results = []

# Update the path for the CSV file
csv_file_path = 'apitest/api_update_dates.csv'

# Update the path for the last run time file
last_run_file_path = 'apitest/last_run.txt'

for api in apis:
    raw_date = scrape_api_update_date(api['url'], api['selector'])
    formatted_date = format_date(raw_date) if raw_date else "Not Available"
    print(f"Scraped {api['name']} - Last Updated: {formatted_date}")  # Add this line
    results.append({
        "name": api['name'],
        "url": api['url'],
        "last_updated": formatted_date,
        "scraped_at": datetime.now().isoformat()
    })

# Save results to a CSV file
df = pd.DataFrame(results)
df.to_csv(csv_file_path, index=False)

# After saving results to CSV
with open(last_run_file_path, 'w') as f:
    f.write(datetime.now().isoformat())

print("Scraping completed. Results saved to api_update_dates.csv")