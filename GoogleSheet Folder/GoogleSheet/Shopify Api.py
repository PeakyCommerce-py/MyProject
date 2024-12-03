import requests

# Use the Admin API Access Token after installing the app
ACCESS_TOKEN = "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"  # Replace with the actual access token
STORE_URL = "5690df.myshopify.co"
API_VERSION = "2023-04"

# Product ID to delete (you can fetch it via a GET request)
product_id = "10347031069003"  # Replace with the actual product ID you want to delete

url = f"https://{STORE_URL}/admin/api/{API_VERSION}/products/{product_id}.json"# Headers for authentication
headers = {
    "Content-Type": "application/json",
    "X-Shopify-Access-Token": ACCESS_TOKEN,
}

# Perform the DELETE request
delete_Request = requests.delete(url, headers=headers)

# Check the response
if delete_Request.status_code == 200:
    print(f"Product {product_id} deleted successfully.")
else:
    print(f"Failed to delete product: {delete_Request.status_code}")
    try:
        print(delete_Request.json())  # Try to decode JSON response for error details
    except ValueError:
        print(delete_Request.text)  # Fallback to plain text if JSON decoding fails