import aiohttp
import asyncio
import pandas as pd
from bs4 import BeautifulSoup

# Maximum number of retries for a request
MAX_RETRIES = 3


# Asynchronous function to fetch all profile links for a given CVR
async def fetch_all_profile_links(session, cvr):
    url = f"https://ownr.dk/companies/public-profile/{cvr}"
    headers = {
        "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
        "accept-language": "en-US,en;q=0.9",
        "cache-control": "max-age=0",
        "referer": f"https://ownr.dk/companies/search?query={cvr}",
        "sec-ch-ua": '"Google Chrome";v="129", "Not=A?Brand";v="8", "Chromium";v="129"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"Windows"',
        "sec-fetch-dest": "document",
        "sec-fetch-mode": "navigate",
        "sec-fetch-site": "same-origin",
        "sec-fetch-user": "?1",
        "upgrade-insecure-requests": "1",
        "user-agent": "Mozilla/5.0",
    }

    for attempt in range(MAX_RETRIES):
        try:
            async with session.get(url, headers=headers) as response:
                soup = BeautifulSoup(await response.text(), "html.parser")

                profile_links = []

                # Check if owners section is present
                li_owners = soup.find("li", class_="owners")
                if li_owners:
                    name_tags = li_owners.find_all("h5", {"itemprop": "name"})
                    for name_tag in name_tags:
                        link_tag = name_tag.find("a", href=True)
                        if link_tag:
                            profile_link = link_tag['href']
                            profile_links.append(f"https://ownr.dk{profile_link}")

                # Check if management section is present
                li_management = soup.find("li", class_="management")
                if li_management:
                    name_tags = li_management.find_all("h5", {"itemprop": "name"})
                    for name_tag in name_tags:
                        link_tag = name_tag.find("a", href=True)
                        if link_tag:
                            profile_link = link_tag['href']
                            profile_links.append(f"https://ownr.dk{profile_link}")

                return profile_links
        except aiohttp.ClientError as e:
            print(f"Error fetching profile links for CVR {cvr}: {e}")
            if attempt < MAX_RETRIES - 1:
                print(f"Retrying... (attempt {attempt + 1})")
                await asyncio.sleep(1)  # Sleep between retries
            else:
                print(f"Failed to retrieve profile links for CVR {cvr} after {MAX_RETRIES} attempts.")
                return []


# Asynchronous function to fetch the full address from a person's public profile
async def fetch_full_address(session, profile_url):
    headers = {
        "accept": "text/html,application/xhtml+xml,application/xml;q=0.9",
        "accept-language": "en-US,en;q=0.9",
        "cache-control": "max-age=0",
        "referer": profile_url,
        "sec-ch-ua": '"Google Chrome";v="129", "Not=A?Brand";v="8", "Chromium";v="129"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"Windows"',
        "sec-fetch-dest": "document",
        "sec-fetch-mode": "navigate",
        "sec-fetch-site": "same-origin",
        "sec-fetch-user": "?1",
        "upgrade-insecure-requests": "1",
        "user-agent": "Mozilla/5.0",
    }

    for attempt in range(MAX_RETRIES):
        try:
            async with session.get(profile_url, headers=headers) as response:
                soup = BeautifulSoup(await response.text(), "html.parser")

                header = soup.find("header", {"class": "page_header"})
                if header:
                    name_tag = header.find("h1", {"itemprop": "name"})
                    address_tag = header.find("span", {"class": "address"})
                    if name_tag and address_tag:
                        name = name_tag.text.strip()
                        address = address_tag.text.strip()
                        return name, address.replace(', DK', '')  # Clean address format
                return "Not Found", "Address not found"
        except aiohttp.ClientError as e:
            print(f"Error fetching address from {profile_url}: {e}")
            if attempt < MAX_RETRIES - 1:
                print(f"Retrying... (attempt {attempt + 1})")
                await asyncio.sleep(1)
            else:
                print(f"Failed to retrieve address for {profile_url} after {MAX_RETRIES} attempts.")
                return "Not Found", "Address not found"


# Asynchronous function to process each CVR, fetch links and addresses
async def process_cvr(session, cvr, processed_addresses):
    profile_urls = await fetch_all_profile_links(session, cvr)
    results = []
    if profile_urls:
        for profile_url in profile_urls:
            name, address = await fetch_full_address(session, profile_url)
            # Ensure no duplicate addresses are added
            if address not in processed_addresses:
                processed_addresses.add(address)
                results.append((cvr, name, address))
            else:
                print(f"Duplicate address found and skipped: {address}")
    else:
        results.append((cvr, "Not Found", "Not Found"))
    return results


# Function to process batches of CVRs asynchronously
async def fetch_data_for_cvr_from_excel(file_path):
    # Read the Excel file
    df = pd.read_excel(file_path)

    # Ensure there is a 'CVR' column in the Excel file
    if 'CVR' not in df.columns:
        print("No 'CVR' column found in the Excel file")
        return

    cvr_numbers = df['CVR'].tolist()

    # Split into batches of 100 CVRs at a time
    batch_size = 100
    results = []
    processed_addresses = set()  # Set to track addresses and avoid duplicates

    async with aiohttp.ClientSession() as session:
        for i in range(0, len(cvr_numbers), batch_size):
            batch = cvr_numbers[i:i + batch_size]
            tasks = [asyncio.create_task(process_cvr(session, cvr, processed_addresses)) for cvr in batch]
            batch_results = await asyncio.gather(*tasks)

            # Flatten the list of results
            for res in batch_results:
                results.extend(res)

            # Wait for 1 second between batches
            if i + batch_size < len(cvr_numbers):
                await asyncio.sleep(1)

    # Convert results to DataFrame
    result_df = pd.DataFrame(results, columns=['CVR', 'Name', 'Address'])

    # Save the updated DataFrame to a new Excel file
    output_file = "output_data.xlsx"
    result_df.to_excel(output_file, index=False)
    print(f"Results saved to {output_file}")


# Main entry point to start the event loop
def main(file_path):
    asyncio.run(fetch_data_for_cvr_from_excel(file_path))


# Example usage
file_path = "cvr_data.xlsx"  # Replace with your actual Excel file path
main(file_path)
