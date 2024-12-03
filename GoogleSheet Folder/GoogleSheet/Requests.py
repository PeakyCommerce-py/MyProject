import os

def find_file(file_name, search_path):
    for root, dirs, files in os.walk(search_path):
        if file_name in files:
            return os.path.join(root, file_name)
    return None  # Return None if the file is not found

# Example Usage
file_name = 'scraping-443109-001aee491348.json'
search_path = 'C:\\Users\\Dejan\\PycharmProjects\\GoogleSheet'
SERVICE_ACCOUNT_FILE = find_file(file_name, search_path)

if SERVICE_ACCOUNT_FILE:
    print(f"File found: {SERVICE_ACCOUNT_FILE}")
else:
    print("File not found!")
