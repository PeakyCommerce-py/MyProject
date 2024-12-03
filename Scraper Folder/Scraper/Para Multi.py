import json

# Function to prompt for default values
def prompt_for_defaults():
    defaults = {}
    defaults['m'] = "0"
    defaults['k'] = "0"
    defaults['r'] = "0"
    defaults['er'] = "0"
    defaults['b'] = "1"
    defaults['eb'] = "0"
    defaults['amin'] = int(input("Min Ålder: "))
    defaults['amax'] = int(input("Max Ålder: "))
    return defaults

# Prompt for default values
defaults = prompt_for_defaults()

# Prompt for multiple "Kommun" names
kommun_names = input("Enter Kommun names separated by commas: ").split(",")

# Clean up and strip spaces from each Kommun name
kommun_names = [kommun.strip() for kommun in kommun_names]

# Kombinationer av kön och civilstånd
gender_options = [('m', '1', 'k', '0'), ('m', '0', 'k', '1')] if defaults['m'] == "1" else [('m', defaults['m'], 'k', defaults['k'])]
marital_status_options = [('r', '1', 'er', '0'), ('r', '0', 'er', '1')] if defaults['r'] == "1" else [('r', defaults['r'], 'er', defaults['er'])]

# Create search parameters
searchParameters = []
for person_name in kommun_names:
    for gender in gender_options:
        for marital_status in marital_status_options:
            current_amin_amax = defaults['amin']
            for _ in range((defaults['amax'] - defaults['amin'] + 1)):
                person_params = {
                    "person": person_name,
                    gender[0]: gender[1],
                    gender[2]: gender[3],
                    marital_status[0]: marital_status[1],
                    marital_status[2]: marital_status[3],
                    "b": defaults['b'],
                    "eb": defaults['eb'],
                    "amin": current_amin_amax,
                    "amax": current_amin_amax
                }
                searchParameters.append(person_params)
                current_amin_amax += 1

# Additional parameters
pages = "16"
fileName = input("Enter the file name for the output: ")

# Create JSON structure
json_data = {
    "searchParameters": searchParameters,
    "pages": pages,
    "fileName": fileName
}

# Save to a JSON file
with open('parameters.json', 'w', encoding="utf-8") as file:
    json.dump(json_data, file, indent=4)

print("JSON file created successfully.")
