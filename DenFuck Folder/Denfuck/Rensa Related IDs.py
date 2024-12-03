import csv

# 1. Samla alla produkt-IDs i en lista
all_product_ids = set()  # Set för snabbare sökning

# Läs in från din CSV-fil där alla IDs finns (t.ex. 'products_output.csv')
with open('products_output.csv', 'r', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    for row in reader:
        product_id = row.get('ID', '').strip()  # Hämta ID och ta bort eventuella mellanslag
        if product_id:  # Kontrollera att ID inte är tomt
            all_product_ids.add(product_id)  # Lägg till varje produkt-ID i setet

# 2. Uppdatera relaterade produkter
updated_data = []

# Läs in filen igen och filtrera "Related IDs"
with open('products_output.csv', 'r', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    for row in reader:
        related_ids = row.get('Related IDs', '').split(',')  # Dela upp relaterade IDs
        # Behåll endast de IDs som finns i all_product_ids
        filtered_related_ids = [rid.strip() for rid in related_ids if rid.strip() in all_product_ids]
        row['Related IDs'] = ','.join(filtered_related_ids)  # Uppdatera med filtrerade IDs
        updated_data.append(row)

# 3. Skriv tillbaka till en ny CSV-fil
output_file = 'updated_products.csv'
with open(output_file, 'w', newline='', encoding='utf-8') as f:
    writer = csv.DictWriter(f, fieldnames=reader.fieldnames)
    writer.writeheader()
    writer.writerows(updated_data)

print(f"Filtreringen är klar. Resultatet sparades i {output_file}")
