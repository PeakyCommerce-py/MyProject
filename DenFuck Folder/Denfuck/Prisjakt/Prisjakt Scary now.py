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


# Function to search for product ID by EAN
def search_product_id(ean):
    # Define the payload for the request
    payload = {
        "query": """
        query searchPage($query: String!) {
            newSearch(query: $query) {
                results {
                    products {
                        nodes {
                            ... on Product {
                                productId: id  # Alias for Product ID
                            }
                            ... on Offer {
                                offerId: id    # Alias for Offer ID
                            }
                        }
                    }
                }
            }
        }
        """,
        "variables": {
            "query": ean,
        }
    }

    # Make the request
    response = requests.post(url, headers=headers, json=payload)
    if response.status_code == 200:
        data = response.json()
        if 'data' in data and 'newSearch' in data['data']:
            products = data['data']['newSearch']['results']['products']['nodes']
            product_ids = [product.get('productId') or product.get('offerId') for product in products if 'productId' in product or 'offerId' in product]
            return product_ids
        else:
            print(f"No valid data found for EAN {ean}: {data}")
            return []
    else:
        print(f"Error fetching product ID for EAN {ean}: {response.text}")
        return []


# Function to get detailed product information
def get_product_details(product_id):
    # Define the payload for the request
    payload = {
        "query": """
        query productPage($id: Int!) {
            product(id: $id) {
                id
                name
                description
                priceSummary {
                    regular
                }
                media {
                    first(width: _280)
                }
            }
        }
        """,
        "variables": {
            "id": product_id,
        }
    }

    # Make the request
    response = requests.post(url, headers=headers, json=payload)

    # Check if the response is successful
    if response.status_code == 200:
        data = response.json()
        if 'data' in data and 'product' in data['data']:
            product = data['data']['product']
            return {
                "id": product['id'],
                "name": product['name'],
                "description": product['description'],
                "regular_price": product['priceSummary']['regular'],
                "image_url": product['media']['first'],
            }
        else:
            print(f"No product data found for ID {product_id}: {data}")
            return None
    else:
        print(f"Error fetching product details for ID {product_id}: {response.text}")
        return None


# List of EANs to process
ean_list = [
    "7331059102883",  # Example EAN
]

# Main script logic
for ean in ean_list:
    print(f"Fetching product ID for EAN: {ean}")
    product_ids = search_product_id(ean)

    for product_id in product_ids:
        print(f"Fetching details for Product ID: {product_id}")
        product_details = get_product_details(product_id)
        if product_details:
            print("Product Details:", product_details)
