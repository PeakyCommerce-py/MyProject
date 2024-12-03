import gspread
import openai
import os

# Print OpenAI version
print(openai.__version__)

# Authenticate Google Sheets
gc = gspread.service_account(filename='scraping-443109-01dfb15e7aa9.json')
sheet = gc.open_by_key('1iJIORj5HkWt2ULh_Plm2la8Jfgdl71v50ghWNecfhy8').worksheet("Catalog")

# Authenticate OpenAI (use environment variable for API key)
openai.api_key = os.getenv('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')  # It's better to store API key in an environment variable

# Fetch all data from the sheet
data = sheet.get_all_records()  # List of dictionaries
headers = sheet.row_values(2)  # Assuming row 2 contains headers

# Function to construct the prompt
def construct_prompt(row, headers):
    product_description = row.get("Sales Text", "")
    extra_data = [
        f"{headers[i]}: {row.get(headers[i], '')}" for i in range(len(headers)) if row.get(headers[i], '').strip()
    ]
    return f"""
    Du är produktskribent för en ledande skandinavisk möbel- och inredningsbutik online. Skapa en kort och inspirerande produktbeskrivning baserat på: {product_description}.
    Använd följande data för extra information: {', '.join(extra_data)}.

    Skriv en kort produktbeskrivning med följande riktlinjer:
    - Längd: 10–50 ord.
    - Börja med produktkategori och varumärke.
    - Nämn material eller design.
    - Lyft fram en specifik funktion eller fördel.
    - Inkludera ett användningsområde eller en inspiration.

    Språkregler:
    - Kortfattad och lättläst.
    - Använd naturliga och inspirerande formuleringar.
    - Undvik tekniska detaljer om de inte är nödvändiga.
    """

# Iterate through rows and process each prompt
results = []
start_row = 3  # Starting row for "Description" updates (GF3 corresponds to row 3 in Google Sheets)
description_column_index = 187  # Column index for "GF" (adjust based on the actual column index in your sheet)

for i, row in enumerate(data):
    prompt = construct_prompt(row, headers)

    # Send request to OpenAI for each row
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4-o-mini",  # Change this to the model you want to use
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt}  # Using the dynamically created prompt
            ]
        )

        # Extract the result from the response
        result = response['choices'][0]['message']['content']

        # Save result and update the corresponding Google Sheet cell in "GF"
        results.append(result)
        sheet.update_cell(start_row + i, description_column_index, result)  # Update the "GF" column (adjust index as needed)
    except Exception as e:
        print(f"Error processing row {start_row + i}: {e}")

# Save results to a file (optional)
with open("output.csv", "w", encoding="utf-8") as f:
    for result in results:
        f.write(result + "\n")

print("Processing completed.")
