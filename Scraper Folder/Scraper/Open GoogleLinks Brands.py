import webbrowser
import time

# Load brand names from the text file
def load_brands(filename):
    with open(filename, 'r', encoding='utf-8') as file:
        return [line.strip() for line in file]

# Open multiple search links for a brand
def open_links(brand_name):
    search_terms = [f"", "Distributor", "Agent", "Leverantör", "Distributör", "Retail", "Bli Återförsäljare"]
    base_url = "https://www.google.com/search?q="
    for term in search_terms:
        url = f"{base_url}{brand_name} {term}"

        webbrowser.open_new_tab(url)
        time.sleep(0.1)  # Small delay to prevent opening tabs too quickly

def main():
    brands = load_brands('distrubitor.txt')
    for brand in brands:
        print(f"Opening links for {brand}...")
        open_links(brand)
        input("Press Enter to continue to the next brand...")

if __name__ == "__main__":
    main()
