import requests

# Define the API endpoint URL for checking product existence
base_url = "https://www.prisjakt.nu/_internal/bff"  # Replace with the correct endpoint URL

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

# List of Product IDs to verify
product_ids = [5167104, 4921345, 5167111, 5001224, 2785291, 4921368, 442398, 501807, 501808, 325691, 325692, 5048385, 729159, 12458443, 5322868, 12611703, 3293317, 878733, 737445, 5345456, 5345458, 5345460, 737467, 3541180, 5345468, 737473, 3541189, 737483, 1251536, 1779924, 5345511, 344296, 344301, 1255661, 5757175, 13943034, 5757182, 5757185, 6238469, 6238476, 5703951, 5703952, 1222929, 1030417, 5703954, 5316883, 5703953, 5757211, 2695456, 3430692, 6027572, 12400954, 6027579, 12400957, 6027582, 6027581, 2801988, 3705158, 313671, 1370443, 5312853, 1222999, 5757271, 12558682, 5757274, 764260, 12558693, 5757287, 5757290, 5312879, 5312880, 5312881, 5312882, 5757297, 5085558, 4370808, 4370809, 2181499, 4370812, 4370813, 3744140, 3393940, 12458418, 12458419, 3303860, 12458420, 12458421, 2636215, 5757368, 2636216, 2636218, 657850, 315835, 12458428, 12458422, 12458423, 12458424, 12458425, 12458426, 12458427, 12458429, 12458430, 12458431, 12458432, 5757384, 12458433, 12458434, 12458435, 12458437, 12458438, 12458439, 12458440, 5757392, 12458441, 12458442, 752083, 301523, 12458444, 12458445, 12458446, 12458447, 3215833, 12458449, 12458450, 12458451, 12458452, 12458453, 12458448, 12458455, 12458456, 12458466, 752099, 12458459, 3746277, 12458461, 12458462, 5292520, 12458464, 12458465, 12458468, 12458469, 621037, 12407292, 12458454, 13742590, 12407299, 12407308, 12458457, 12458458, 13742618, 13742619, 315931, 12458460, 13742623, 13742624, 4923856, 13742627, 12458463, 623160, 5343805, 4379206, 1057352, 3111506, 4379227, 12446302, 12446303, 12446305, 12446309, 3490406, 5147241, 5102186, 2708073, 4379245, 5147247, 619124, 5757556, 739968, 500360, 5343881, 500361, 5343884, 3746447, 739992, 3746466, 3746467, 2636452, 316067, 2636457, 1743529, 5817012, 5817014, 373436, 316099, 1782479, 3005151, 445152, 3005154, 1497830, 5102311, 5102312, 1497835, 3279608, 3187457, 3187459, 2095878, 3015451, 5344028, 5307167, 5344033, 5344034, 3232547, 5344036, 5704488, 3232552, 3232555, 328492, 496435, 5344053, 1223484, 5344061, 5344063, 1317700, 3005260, 6116192, 6116193, 6116194, 3746657, 3746656, 3185505, 3494757, 5821296, 6116246, 5458839, 5458840, 6116247, 2663328, 6116257, 3705762, 3705761, 6116260, 2663332, 5458854, 5458855, 5458856, 4791206, 6116266, 5458851, 1321896, 5458861, 5458867, 13908941, 5307342, 2671573, 1000406, 5307363, 3705836, 5159949, 1481752, 5159960, 1481755, 1481756, 4625435, 1246241, 1246242, 734247, 734248, 1665479, 3101748, 5377080, 3101753, 3101752, 11883578, 3646522, 1498171, 3646527, 1498175, 5377092, 6014038, 6014041, 2786394, 13558875, 1322076, 13558876, 1322080, 13558881, 2264167, 2264170, 2264180, 1635450, 1322122, 4170894, 4170895, 4170898, 4170899, 4170900, 4170901, 1733784, 5448857, 5448856, 2671777, 2639010, 2639013, 2639014, 2639015, 12397740, 1907886, 740528, 2208949, 283837, 2634951, 2710728, 1840331, 1840332, 12790988, 1389789, 2710749, 13153505, 13153506, 13153507, 13153508, 13153509, 5213415, 1555691, 13153518, 1780977, 2821392, 5160229, 5160231, 5520682, 1744172, 1744173, 326964, 3487037, 329023, 1983811, 5344580, 5160259, 1713476, 3409224, 994637, 732502, 12612956, 3956061, 10675550, 10675549, 3290464, 12483932, 12483933, 12483935, 12483937, 732517, 12483943, 2635112, 5637480, 732521, 12399979, 4205937, 732534, 3188093, 5103040, 5103041, 916931, 749006, 320977, 320979, 320981, 316886, 320983, 320982, 3290603, 6477296, 263705, 263706, 263709, 2809384, 869931, 314925, 314926, 3294766, 11378224, 314933, 2719290, 11378238, 1265219, 5344836, 1265221, 728650, 11378255, 11378256, 13000271, 13000274, 13000273, 13000276, 13000275, 13000279, 11378263, 11378265, 13000283, 5095004, 5095006, 11378271, 5344866, 5344869, 12351079, 263788, 12351086, 263791, 11378289, 5344881, 263800, 12351096, 730754, 263820, 263822, 1812116, 263829, 263831, 4695704, 263832, 3942046, 10534558, 1908385, 10534562, 1812131, 3987111, 5344938, 11378347, 2045615, 263862, 917174, 2574031, 2717398, 2717400, 263904, 2946790, 263916, 263917, 263918, 263919, 4382451, 5650163, 5650164, 4597494, 5650166, 5650168, 5650167, 4341503, 360194, 263939, 734990, 739088, 4732693, 4722458, 4831004, 974627, 5619492, 1982256, 5580593, 5580594, 2998080, 4403009, 735041, 5130065, 739170, 7206755, 749410, 509796, 5791608, 5791610, 13969278, 13969279, 2180992, 894848, 264066, 2180995, 5920652, 5920653, 4806545, 264082, 2154395, 5920669, 5920670, 509854, 509855, 509853, 896939, 264107, 264119, 804794, 749505, 4026308, 774084, 4026310, 1054662, 4169672, 4169676, 6027221, 509918, 6027236, 6027237, 6027238, 4921320, 1251307, 4921329, 4169727]

# Function to check if a product exists
def check_product_exists(product_id):
    payload = {
        "query": """
        query productPage($id: Int!) {
            product(id: $id) {
                id
                name
                # Add other fields if needed
            }
        }
        """,
        "variables": {
            "id": product_id
        }
    }
    response = requests.post(base_url, headers=headers, json=payload)
    if response.status_code == 200:
        data = response.json()
        # Check if the product data is present
        if "data" in data and "product" in data["data"] and data["data"]["product"] is not None:
            return True, data["data"]["product"]
    return False, None

# Loop through each Product ID and verify
for product_id in product_ids:
    exists, product_data = check_product_exists(product_id)
    if exists:
        print(f"Product ID {product_id} exists: {product_data}")
    else:
        print(f"Product ID {product_id} does not exist.")