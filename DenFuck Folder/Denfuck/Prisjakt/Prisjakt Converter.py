import requests

# URL for Prisjakts BFF endpoint
url = "https://www.prisjakt.nu/_internal/bff"

# Headers with necessary cookies and user-agent

headers = {
    "accept": "*/*",
    "accept-language": "en-US,en;q=0.9",
    "content-type": "application/json",
    "cookie": (
        "pj:cfexpuid=aa8a7741-e27f-4143-87fa-1337895c6b40; "
        "pj:session=eyJpZCI6IjA5N2ZiZjAwLWM0ZGItNDg3Mi1iNjZhLWM0NTA5N2Q1NzcxYyIsInZpZXdlZEV4cGVyaW1lbnRzIjp7InNwb25zb3JlZC1pbi1wcm9kdWN0LXBhZ2UiOnsidmFyaWFudCI6InNob3cifSwibGFuZGluZy1wYWdlLXNwcmluZy1iYW5uZXIiOnsidmFyaWFudCI6InNob3cifSwiYXJ0aWNsZXMtZnJvbS1zYW5pdHkiOnsidmFyaWFudCI6InNob3cifSwidXNlLW5leHRqcy1wcm94eSI6eyJ2YXJpYW50IjoiZW5hYmxlZCJ9fSwiX2V4cGlyZSI6MjA0NTc1MzYxOTcwMSwiX21heEFnZSI6MzE1MzYwMDAwMDAwfQ==; "
        "pj:session.sig=Aw1KgSB-XT7VfheyijDaNp1-olI; _cmp_marketing=1; "
        "_ga=GA1.1.1198315508.1730393624; _cmp_analytics=1; _cmp_advertising=1; "
        "_cmp_personalisation=1; consentUUID=261a2f56-a453-47e5-b83e-0390a28aaf50_37; "
        "consentDate=2024-10-31T16:53:43.398Z; _gcl_au=1.1.721703019.1730393626; "
        "cis-jwe=eyJpc3N1ZWRBdCI6IjIwMjQtMTAtMzFUMTY6NTM6NDFaIiwiZW5jIjoiQTEyOENCQy1IUzI1NiIsInJlSXNzdWVkQXQiOiIyMDI0LTEwLTMxVDE2OjUzOjQzWiIsImFsZyI6ImRpciIsImtpZCI6IjIifQ..0amSMjlCiVp8b2ihAHZPLA.sp5X6ZRu49lxGdT3B_qT0oXQyyn20KzkbXbQi_SNC9-i4Q72yrs2APEWwVNLmhf43PK-qgXRa2v8FUHoy3iMCw.6oApK2tX9vHtK9Kijhov1A; "
        "_pulse2data=0f10f37b-7933-4f15-b7af-492af7453d95%2Cv%2C%2C1730998423000%2CeyJpc3N1ZWRBdCI6IjIwMjQtMTAtMzFUMTY6NTM6NDFaIiwiZW5jIjoiQTEyOENCQy1IUzI1NiIsInJlSXNzdWVkQXQiOiIyMDI0LTEwLTMxVDE2OjUzOjQzWiIsImFsZyI6ImRpciIsImtpZCI6IjIifQ..FFy3re_C-i6vVEZc3ZmVAA.j7PcZNvKW8TGq4fn22pQ7dYP8Z0-27cTSRx_7B03TIJnXypWYbEEkJK3pxfX1TXM7x6XF3iOPrgtNdEzadK4IjzMDxekad1TKKuMlSp-TxpXuaFrQdjCgdr_tUvGWUA5AG-0tH52GTGVYLERtI_X9kQR9THHOtfschXk2tzEfsRSC4nWM0-f_skmywc3SF46ZPjgSSFjeswTb6Bezs0U_jx-kHRZaIda83GAdYeSQQiFCOeWc9sfIJvsJMo-MpAHuzNZuIj_Pt9tXTnBHyHhdLaj2L7NO3nuPw9Q6L637X2lNWZJlLv8h5WAADrjnjZSc_8X-ORBpTx67X1zyTqU2w.r6BmWJdXHQDba9EX-E61kw%2C%2C0%2Ctrue%2C%2CeyJraWQiOiIyIiwiYWxnIjoiSFMyNTYifQ..B3-rjR55tPCFQdsN4exffcW_3O5wG7NLZsHga8XbhT4; "
        "__codnp=; pj_partner={\"partner_id\":\"259\",\"updated_at\":1730496398943}; "
        "_hjSessionUser_3101556=eyJpZCI6IjJiNjk1ODUxLTA3MDItNTdhOC04ZjdkLTU5MmE1MTEyNGE1NCIsImNyZWF0ZWQiOjE3MzA0OTYyOTI1NDUsImV4aXN0aW5nIjp0cnVlfQ==; "
        "_hjSession_3101556=eyJpZCI6IjczNmRiNmY3LWRhMDEtNDI1Mi1iN2RjLTIyZDlkODc1MWUwOSIsImMiOjE3MzA1MDc3NTkwNzcsInMiOjAsInIiOjAsInNiIjowLCJzciI6MCwic2UiOjAsImZzIjowLCJzcCI6MH0=; "
        "_clck=v0me8a%7C2%7Cfqj%7C0%7C1765; __cf_bm=sAzZhggG76zFQJZh.JVDOpnH1fwvOpNidh04CDnppHc-1730511918-1.0.1.1-ERe29g5Cb1wxjA9fooPyIPbS9BP1PPpB949RBj.hPBerWLN.ybNMwl_1SNw0zsRwFbxzgPhSGpvIOLjGrP8_Pg; "
        "cf_clearance=nwDKWW3rJBiui3lDRKYjOF9qNu7MM4n_M_vIKV0pegA-1730511921-1.2.1.1-5m7V5cxL5eOO9MFFzUt4yvMciq71oo1CcS5GRgUdwji5L4s2MrtruL16EHvarW.OwQStgDDYv5cjT7PA4ADJTgOHjSpNptIl.Q3SMyohFlhdwCf3COoVRa6Js9RSowr4fNWeYZaKX90aLVXzuVXgjtAAuXGbziAFMZNvoRFcje9pk2lnnbFSlJXw7mti742HXGer.zLT5FmXno_rfBftJKx6zofLExvYKsOojE2El5JThp9JX0tR2s8CySyHEOFuukYbsygFVTSEhuKtBHkriW9SBG_3Cqlj6.AklRHGZdQpMFLK2OsCHo0jioatU0TQ2VUjEh2XyvZ8S9kr40Q0aR4QTQ0K6JuV8e7Rr0cFOqnTvDuAIAm6ScEIbsigFxYhf1OT3gQwxMLMjcJ6hu0iPkbyALRepLQ17igL0VuMhUE; "
        "_uetsid=c1c31260989711efade889f5621f71ed; _uetvid=b717eee097a811efaf95e32847a903ff; "
        "pj_sid=9d951109-7263-4168-8b64-86284dbe4c46; "
        "_pulsesession=%5B%22sdrn%3Aschibsted%3Asession%3A683a23a3-20ef-4b97-9523-92a9289553ef%22%2C1730507757949%2C1730511924667%5D; "
        "_ga_LB08D4LREX=GS1.1.1730507757.4.1.1730511927.0.0.0"
    ),
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36"
}


# Define the payload to fetch detailed information for each product using its ID
def get_detailed_product_info(product_id):
    payload = {
        "operationName": "productPage",
        "query": """
        query productPage($id: Int!) {
            product(id: $id) {
                id
                name
                description
                priceSummary {
                    regular
                }
                category {
                    path {
                        name
                    }
                }
                media {
                    first(width: _280)  # Use enum value _280 for the image width
                }
                prices {
                    meta {
                        itemsTotal
                    }
                    nodes {
                        shopOfferId
                        name
                        externalUri
                        price {
                            inclShipping
                            exclShipping
                        }
                        store {
                            name
                            currency
                        }
                    }
                }
            }
        }
        """,
        "variables": {
            "id": product_id
        }
    }

    # Make the request to fetch product details
    response = requests.post(url, headers=headers, json=payload)

    # Check if the response is successful
    if response.status_code == 200:
        data = response.json()

        # Check if there's an error in the data
        if "errors" in data:
            print(f"Error fetching details for product ID {product_id}: {data['errors']}")
            return None

        # Return the product details
        return data["data"]["product"]
    else:
        print(f"Error: Status Code {response.status_code}")
        print("Response:", response.text)
        return None


# Main function to display fetched detailed data
def display_product_details(product_id):
    print(f"Fetching detailed info for Product ID: {product_id}")
    product_info = get_detailed_product_info(product_id)

    if product_info:
        print("Product Name:", product_info["name"])
        print("Description:", product_info.get("description", "No description available"))
        print("Regular Price:", product_info["priceSummary"]["regular"], "SEK")
        print("Category Path:", " > ".join([cat["name"] for cat in product_info["category"]["path"]]))
        print("Image URL:", product_info["media"]["first"])

        print("\nCompetitor Offers:")
        if product_info["prices"] and product_info["prices"]["nodes"]:
            for offer in product_info["prices"]["nodes"]:
                print("Store:", offer["store"]["name"])
                print("Price (Excl. Shipping):", offer["price"]["exclShipping"], offer["store"]["currency"])
                print("Price (Incl. Shipping):", offer["price"]["inclShipping"], offer["store"]["currency"])
                print("Link to Store:", offer["externalUri"])
                print("-" * 40)
        else:
            print("No competitor offers found.")

        print("=" * 50)
    else:
        print("Failed to retrieve detailed product information.")


# List of product IDs to check (replace these with actual IDs you want to query)
product_ids = [13241992]  # Replace with actual product IDs you want to retrieve data for

# Loop through each product ID and display data
for product_id in product_ids:
    display_product_details(product_id)