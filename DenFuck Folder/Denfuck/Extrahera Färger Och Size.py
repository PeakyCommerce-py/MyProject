import csv
import re

# Grundläggande färger på svenska och engelska
basic_colors = {
    "Red": "Röd", "Green": "Grön", "Blue": "Blå", "Yellow": "Gul",
    "Black": "Svart", "White": "Vit", "Grey": "Grå", "Pink": "Rosa",
    "Purple": "Lila", "Orange": "Orange", "Brown": "Brun", "Turquoise": "Turkos"
}

# Regex-mönster för att matcha storlekar (t.ex. "30 cm", "Ø25 cm", "35cm")
size_pattern = re.compile(r"(?:Ø)?(\d{2,3})\s?cm", re.IGNORECASE)

# Funktion för att hitta färg från produktnamnet
def detect_color_from_name(product_name):
    for english_color, swedish_color in basic_colors.items():
        # Matcha färg i produktnamnet (både engelska och svenska)
        if re.search(rf"\b{english_color.lower()}\b", product_name.lower()):
            return swedish_color  # Returnera färg på svenska
        if re.search(rf"\b{swedish_color.lower()}\b", product_name.lower()):
            return swedish_color  # Om den redan är på svenska, returnera direkt
    return "Unknown Color"

# Funktion för att hitta storlek från produktnamnet
def detect_size_from_name(product_name):
    size_match = size_pattern.search(product_name)
    if size_match:
        return f"Ø{size_match.group(1)} cm"  # Format som Ø30 cm
    return "Unknown Size"

# Huvudlogik för att processa filen och extrahera färg och storlek
def main():
    input_filename = "input_products.csv"  # Input-fil med artiklar
    output_filename = "output_products_with_color_size.csv"  # Output-fil

    with open(input_filename, mode="r", encoding="utf-8") as infile, open(output_filename, mode="w", newline="", encoding="utf-8") as outfile:
        reader = csv.DictReader(infile)
        fieldnames = reader.fieldnames + ["Extracted Color", "Extracted Size", "Matched"]
        writer = csv.DictWriter(outfile, fieldnames=fieldnames)
        writer.writeheader()

        for row in reader:
            product_name = row["Article Name"]  # Kolumnen med produktnamnet

            # Extrahera färg och storlek
            extracted_color = detect_color_from_name(product_name)
            extracted_size = detect_size_from_name(product_name)

            # Kontrollera om båda attributen hittades
            matched = "Yes" if extracted_color != "Unknown Color" and extracted_size != "Unknown Size" else "No"

            print(f"Produkt: {product_name}, Färg: {extracted_color}, Storlek: {extracted_size}, Matchad: {matched}")

            # Uppdatera raden med extraherade attribut
            row.update({
                "Extracted Color": extracted_color,
                "Extracted Size": extracted_size,
                "Matched": matched
            })

            # Skriv raden till output-fil
            writer.writerow(row)

    print(f"Resultat sparade i {output_filename}")

if __name__ == "__main__":
    main()
