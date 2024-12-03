import requests
from bs4 import BeautifulSoup
import csv
from collections import defaultdict

# Dina cookies för inloggning
cookies = {
    "amcookie_policy_restriction": "denied",
    "aw_popup_viewed_page": "[%22bbc9ba7666d7d88096971df7c13e31ac04c3066b8905a88c777a0e81916da2eb%22%2C%2249dbfcfcb53b336e2719463f32c08bfe8b9c930fafc270f194d6c9ba91578288%22]",
    "form_key": "l9cMINqASD3VdaSU",
    "PHPSESSID": "djmfnpb9cb4p5qikf93ljk097e",
    "_ALGOLIA_MAGENTO_AUTH": "aa-Y3VzdG9tZXItMDc0YWIwMzA0MjlkMWI1NTE0NmIyNDFjZjgxYjA3NDFhYTc2Y",
    "lvc-path-key": "1-2-75",
    "mage-cache-sessid": "true",
    "mage-cache-storage": "{}",
    "mage-cache-storage-section-invalidation": "{}",
    "mage-messages": "",
    "private_content_version": "3b190a8af4c984777ba9a9c1ff59235b",
    "product_data_storage": "{}",
    "recently_compared_product": "{}",
    "recently_compared_product_previous": "{}",
    "recently_viewed_product": "{}",
    "recently_viewed_product_previous": "{}",
    "section_data_ids": "{%22customer%22:1732541551%2C%22compare-products%22:1732541551%2C%22last-ordered-items%22:1732541551%2C%22cart%22:1732635754%2C%22directory-data%22:1732541551%2C%22captcha%22:1732541551%2C%22instant-purchase%22:1732541551%2C%22loggedAsCustomer%22:1732541551%2C%22persistent%22:1732635754%2C%22review%22:1732541551%2C%22wishlist%22:1732541551%2C%22ammessages%22:1732541551%2C%22recently_viewed_product%22:1732541551%2C%22recently_compared_product%22:1732541551%2C%22product_data_storage%22:1732541551%2C%22paypal-billing-agreement%22:1732541551}",
    "X-Magento-Vary": "63d48e8f09734a959877da340b848b952253d9a1ac543c36645be1d1f7747b38",
}

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
}


def get_categories_and_subcategories(base_url):
    """
    Hämta överkategorier och deras underkategorier med länkar och artikelräkningar.
    """
    response = requests.get(base_url, headers=headers, cookies=cookies)
    if response.status_code != 200:
        print(f"Failed to retrieve {base_url} (Status code: {response.status_code})")
        return {}

    soup = BeautifulSoup(response.text, "html.parser")
    categories = defaultdict(dict)

    # Hämta överkategorier
    over_categories = soup.select("li.item.-filter-parent")
    for over_category in over_categories:
        over_category_name = over_category.get("data-label")

        # Lägg till artikelräkningen i överkategorinamnet
        article_count_tag = over_category.select_one(".count")
        if article_count_tag:
            article_count = article_count_tag.get_text(strip=True)
            over_category_name = f"{over_category_name} ({article_count})"

        # Hämta underkategorier
        subcategories = over_category.select("ul.items-children.level-1 li.item.-filter-parent")
        for subcategory in subcategories:
            subcategory_name = subcategory.get("data-label")
            subcategory_link = subcategory.select_one("a").get("href")
            subcategory_article_count_tag = subcategory.select_one(".count")
            if subcategory_article_count_tag:
                subcategory_article_count = subcategory_article_count_tag.get_text(strip=True)
                subcategory_name = f"{subcategory_name} ({subcategory_article_count})"
            categories[over_category_name][subcategory_name] = subcategory_link

    return categories


def save_categories_to_csv(categories, output_file="categories.csv"):
    """
    Spara kategorier och underkategorier i en CSV-fil.
    """
    with open(output_file, "w", newline="", encoding="utf-8") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["Over Category", "Subcategory", "Subcategory Link"])
        for over_category, subcategories in categories.items():
            for subcategory_name, subcategory_link in subcategories.items():
                writer.writerow([over_category, subcategory_name, subcategory_link])


def main():
    base_url = "https://extranet.martinex.se/hemma"  # Sidan med alla kategorier
    print("Hämtar överkategorier och underkategorier...")
    categories = get_categories_and_subcategories(base_url)
    print(f"Hittade {len(categories)} överkategorier.")

    # Spara resultat i en CSV-fil
    save_categories_to_csv(categories)
    print("Kategorier sparade i 'categories.csv'.")


if __name__ == "__main__":
    main()