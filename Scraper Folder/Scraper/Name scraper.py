# Read the contents of your existing text file (assuming the file is named "emails.txt")
with open("Excels/Bajshörna.txt", "r") as infile:
    lines = infile.readlines()

# Extract email addresses from each line
email_addresses = []
for line in lines:
    parts = line.strip().split(":")  # Split by colon
    if len(parts) >= 2:  # Ensure there's at least one colon
        email_addresses.append(parts[0])  # Extract the email address

# Write the extracted email addresses to a new text file (named "extracted_emails.txt")
with open("Excels/extracted_emails.txt", "w") as outfile:
    for email in email_addresses:
        outfile.write(email + "\n")  # Write each email address followed by a newline

print(f"Extracted {len(email_addresses)} email addresses. Saved to 'extracted_emails.txt'.")
