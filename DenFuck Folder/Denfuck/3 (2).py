import aiohttp
import asyncio
import json
import urllib.parse
import pandas as pd
import os
import subprocess
from datetime import datetime

# Function to generate location variations with a minimum of 3 words
def generate_location_variations(location):
    location = location.replace(',', '')  # Remove all commas
    parts = location.split()
    variations = []

    # Create variations by removing one part at a time if the remaining parts are 3 or more
    for i in range(len(parts)):
        variation = ' '.join(parts[:i] + parts[i + 1:]).strip()
        if len(variation.split()) >= 3:
            variations.append(variation)

    unique_variations = list(filter(None, list(set(variations))))
    return unique_variations


# Function to correct URL encoding
def correct_encoding(location):
    return urllib.parse.quote_plus(location)  # Ensure spaces are encoded as '+'


# Function to fetch and extract links and phone numbers for persons
async def fetch_and_extract_links(session, url, expected_name):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36',
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'Accept-Language': 'en-US,en;q=0.5',
        'Accept-Encoding': 'gzip, deflate, br',
        'Connection': 'keep-alive',
        'Referer': 'https://map.krak.dk/',
        'TE': 'Trailers'
    }

    async with session.get(url, headers=headers) as response:
        if response.status == 200:
            response_text = await response.text()

            json_str = response_text[response_text.index('(') + 1: response_text.rindex(')')]
            data = json.loads(json_str)
            links = []
            phone_numbers = []
            for feature in data.get('search', {}).get('wp', {}).get('features', []):
                name = feature.get('name', '')
                if expected_name.lower().replace(" ", "") in name.lower().replace(" ", "") or name.lower().replace(" ", "") in expected_name.lower().replace(" ", ""):
                    for link in feature.get('links', []):
                        if link.get('type') == 'INFOPAGE':
                            links.append(link.get('href'))
                    for phone in feature.get('phoneNumbers', []):
                        phone_numbers.append(phone)
            return links, phone_numbers
        else:
            return [], []


# Function to fetch links for a location
async def fetch_links_for_location(session, location, expected_name):
    if not isinstance(location, str):
        location = str(location) if not pd.isna(location) else ''

    location_variations = generate_location_variations(location)
    base_url_personer = "https://mapsearch.eniro.com/search/search.json?callback=jQuery211007513183039970128_1720919994854&phase=first&index=wp&profile=dk_krak&q={}&reverseLookup=true&center=9.763712882995605%2C55.582492765155564&zoom=14&sortOrder=default&viewPx=963%2C991&adjPx=0%2C0%2C0%2C0&pageSize=10&version=4&offset={}"

    tasks = []
    links_personer = []
    phone_numbers_personer = []

    for variation in location_variations:
        encoded_variation = correct_encoding(variation)
        for offset in [0, 1]:
            url_personer = base_url_personer.format(encoded_variation, offset)
            tasks.append(fetch_and_extract_links(session, url_personer, expected_name))

    results = await asyncio.gather(*tasks)

    for links, phones in results:
        if links and phones:
            links_personer.extend(links)
            phone_numbers_personer.extend(phones)
            break  # Stop if a match is found

    return links_personer, phone_numbers_personer


# Main function to handle the entire process
async def main(input_file, output_dir):
    df = pd.read_excel(input_file)

    # **Modification Start**
    # Filter out rows where 'Address' is 'Address not found' or 'Name' is empty or NaN
    df = df[
        (df['Address'].notna()) &
        (df['Address'] != 'Address not found') &
        (df['Name'].notna()) &
        (df['Name'] != '')
    ]
    # **Modification End**

    locations = df['Address'].tolist()
    results = []

    async with aiohttp.ClientSession() as session:
        tasks = [
            fetch_links_for_location(session, location, row.Name)
            for row, location in zip(df.itertuples(index=False), locations)
        ]
        responses = await asyncio.gather(*tasks)

        for row, (links_personer, phone_numbers_personer) in zip(df.itertuples(index=False), responses):
            results.append({
                'cvr': row.CVR,  # Adjust the column names as per your DataFrame
                'address': row.Address,
                'name': row.Name,
                'links_personer': ', '.join(links_personer),
                'phone_numbers': ', '.join(phone_numbers_personer)
            })

    results_df = pd.DataFrame(results)
    output_file = os.path.join(output_dir, 'output_links.xlsx')
    results_df.to_excel(output_file, index=False)

    # Run script 1.py after saving the output file
    # subprocess.run(["python", "1.py"], check=True)


if __name__ == "__main__":
    input_file = "output_data.xlsx"  # Replace with your input file path

    # Create a new directory with the current timestamp
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    output_dir = os.path.join(os.getcwd(), f'run_{timestamp}')
    os.makedirs(output_dir, exist_ok=True)

    try:
        asyncio.run(main(input_file, output_dir))
    except Exception as e:
        print(f"An error occurred: {e}")
