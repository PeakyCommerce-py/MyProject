import requests
import json
import pandas as pd

# Load search parameters from parameters.json
with open('parameters.json', 'r', encoding="utf-8") as file:
    data = json.load(file)

search_parameters = data['searchParameters']
pages = int(data['pages'])
file_name = data['fileName']

# URL for the search API
url = "https://www.ratsit.se/api/search/combined"

# Headers to simulate a browser request
headers = {
    "accept": "application/json, text/plain, */*",
    "accept-language": "en-US,en;q=0.9,cs;q=0.8,ru;q=0.7",
    "content-type": "application/json",
    "priority": "u=1, i",
    "sec-ch-ua": "\"Chromium\";v=\"130\", \"Google Chrome\";v=\"130\", \"Not?A_Brand\";v=\"99\"",
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": "\"Windows\"",
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "same-origin",
    "cookie": "CookieConsent={stamp:%27qhhXnqJupkuruGdxs96AUq5T37nOCrC1zcq7VuNqHOMWclVeoLE/kw==%27%2Cnecessary:true%2Cpreferences:true%2Cstatistics:true%2Cmarketing:true%2Cmethod:%27explicit%27%2Cver:3%2Cutc:1730899072029%2Cregion:%27uz%27}; _gcl_au=1.1.1804227595.1730899072; _ga=GA1.1.1112548300.1730899073; _clck=hr4cw3%7C2%7Cfqn%7C0%7C1771; gtm_upi=djVRU2dndGVINklLTnRLS0tJdWNYU29OVk5HUjQ2bVFJdVcreUdXd0ZQaz; _fbp=fb.1.1730899244518.89996532377576615; __gads=ID=c64172f124e721d1:T=1730899074:RT=1730899400:S=ALNI_MYDUND0fgmcltbFeJiAwDEf4hg4FA; __gpi=UID=00000f2549ac8e47:T=1730899074:RT=1730899400:S=ALNI_MbUbv8_gV861wPBNbYD2kDjkrzsaQ; __eoi=ID=8980ac87a22e9f98:T=1730899074:RT=1730899400:S=AA-AfjZZBEDe0kxzod-m2IljJ3RI; .AspNetCore.Antiforgery.73XflXSd7TU=CfDJ8JyZhnBfggVClOTwXXWQB1mZP-q26iU5ci_HHoZkLQvYXDSLkiaf5lxRtmBSHsQwMYVBnxXpVZiOMMA1swE9oEVVnwXkXFfJq55lcqVxhhe-VgVp4XuASJnGGB0_b7fj9b21BLmmf9KiCQkIZbqp5Hw; _return_url=%7B%22Url%22%3A%22%2Fsok%2Fperson%3Fvem%3DHalmstad%5Cu0026m%3D0%5Cu0026k%3D0%5Cu0026r%3D0%5Cu0026er%3D0%5Cu0026b%3D0%5Cu0026eb%3D0%5Cu0026amin%3D16%5Cu0026amax%3D120%5Cu0026fon%3D1%5Cu0026page%3D1%22%2C%22Text%22%3A%22s%5Cu00F6ket%22%7D; wisepops=%7B%22popups%22%3A%7B%7D%2C%22sub%22%3A0%2C%22ucrn%22%3A70%2C%22cid%22%3A%2250552%22%2C%22v%22%3A4%2C%22bandit%22%3A%7B%22recos%22%3A%7B%7D%7D%7D; wisepops_props=%7B%22uid%22%3A%22undefined%22%2C%22ue%22%3A%22undefined%22%2C%22uds%22%3A%22undefined%22%2C%22srpat%22%3A%22undefined%22%2C%22srpap%22%3A%22undefined%22%2C%22srpapr%22%3A%22undefined%22%2C%22srpna%22%3A%22undefined%22%2C%22pvn%22%3A%22null%22%2C%22cvn%22%3A%22null%22%2C%22pt%22%3A%22search%22%2C%22companypage%22%3A%22null%22%2C%22personpage%22%3A%22null%22%7D; .AspNetCore.Cookies=CfDJ8JyZhnBfggVClOTwXXWQB1k7i8qmJ7S-xA6cCKUl8K6QKtdJSCyQNf6AqScwkt6btEwcDKeV8jGKBHaZWR9PMYIJzck0De3G77w93u0awYeTHShDv6kY0Z9M2ZzQfGLE22ScV7crC7SbmkW0o-jHFg7zJDD8DQ1aCCzWeCJDqxgXJrJA5h26x6RjYFzhQjLQIWnDUqfet7ZQ1TQFVAHKo-WIOt8mpNhFT83tVIYp-Ouf2XH8UEIbYj-cjPR9ifgZHYsahegCh5TDOYji25dbpuTrMxVuFJoTy9VaNuOOyu8J9J2HxFb1t3AjvLaiZx_4fvn672EinzQjrI4pamfe_LARA9rJ4vI1pru5lsshuGo4BMjzpcD4rN3qk61SJ0l_k-30iHh4tvJ4IPUJPKV3U7AxZC1bNMQFfJnpv-Y0RbhncHK8_1_ejp1bNAfUAyTRC0_66AbjySQ0cd6Lw-d6ArCuDryw3bzriz_zUyUl57iwh10IurB_3IyFcY68wC8ALX9CPvk7kL9tmcdCbOmdfpWdKf-4-xsctPF88_VH4H_4MY34T34eOOydnVwxTMsEOqjJvGPzGe2SerLTWRvoRStNLYVWLhwqx1c97NY2w11J3zT8AFmnKw3PEEc59yli3CR2QPML7NdXvKMU-8KspZnIHSV7JRDdbz9jEiC_vCQFVws9mO4Uf3nOuMhxwX8ssX6e4esdQpRWBNfnIBlIzYXetOGVI3POVmfmtecpu9WAxMurm8Q197FEzj5FMpCYgwt0Nz372DueZ1kQ8yMlgQUY-2dC8HPB5EMtFIAILPS5qafyJpmqHwkzn34ZKf0YyyPVBBJ0sjruSjkTpLDtexT4v5b2hiEIaS2PUauZYFVe6B7xF5G2iW89Mwl_Ts__7VCgYHh4M8u_69mMnfIR2iD9bUtNRK-bqxDNjtPZO9QpsjNROvzR4lFgTGrQdV5D7HH6T3EoTbAWLP6LNBFuwRP-jQbJn-oEHpn2O1vv8AzuFdKWAJ4QUGR0uW0zSyb18gWcvEn42RidA3xipmPuDZE; _uetsid=87d373509c4111ef95cf79e819c47181; _uetvid=adbd92a0caa411ee9b0d0f6815d49683; wisepops_visitor=%7B%22AX7MUsC3EZ%22%3A%2237122ea8-3ce7-4397-98b4-2d841d5a1aac%22%7D; wisepops_visits=%5B%222024-11-06T13%3A40%3A27.613Z%22%2C%222024-11-06T13%3A27%3A58.651Z%22%2C%222024-11-06T13%3A27%3A55.448Z%22%2C%222024-11-06T13%3A27%3A48.834Z%22%2C%222024-11-06T13%3A27%3A43.099Z%22%2C%222024-11-06T13%3A27%3A19.816Z%22%2C%222024-11-06T13%3A23%3A59.692Z%22%2C%222024-11-06T13%3A23%3A26.562Z%22%2C%222024-11-06T13%3A23%3A15.843Z%22%2C%222024-11-06T13%3A20%3A43.402Z%22%5D; wisepops_session=%7B%22arrivalOnSite%22%3A%222024-11-06T13%3A40%3A27.613Z%22%2C%22mtime%22%3A1730900429013%2C%22pageviews%22%3A1%2C%22popups%22%3A%7B%7D%2C%22bars%22%3A%7B%7D%2C%22sticky%22%3A%7B%7D%2C%22countdowns%22%3A%7B%7D%2C%22src%22%3Anull%2C%22utm%22%3A%7B%7D%2C%22testIp%22%3Anull%7D; _clsk=t68s0x%7C1730900429902%7C16%7C1%7Ct.clarity.ms%2Fcollect; _ga_C2F6LZXLZK=GS1.1.1730899072.1.1.1730900434.54.0.1740764176"
}

links = []

# Loop through the search parameters
for params in search_parameters:
    person = params['person']
    amin = params['amin']
    amax = params['amax']

    m = params['m']
    k = params['k']
    b = params['b']
    r = params['r']
    er = params['er']
    eb = params['eb']

    # Loop through the pages for the current search parameters
    for page in range(1, pages + 1):
        # Construct the payload for the current request
        payload = {
            "who": "Halmstad",
            "age": ["16", "120"],
            "phoneticSearch": True,
            "companyName": "",
            "orgNr": "",
            "firstName": "",
            "lastName": "",
            "personNumber": "",
            "phone": "",
            "address": "",
            "postnr": "",
            "postort": "",
            "kommun": "",
            "page": 1,
            "url": "/sok/person?vem=Halmstad&m=0&k=0&r=0&er=0&b=0&eb=0&amin=16&amax=120&fon=1&page=1"
        }

        # Send the POST request to the API
        response = requests.post(url, headers=headers, json=payload)
        print(response.text)
        # Check if the response is successful
        if response.status_code == 200:
            response_data = response.json()
            hits = response_data.get('person', {}).get('hits', [])

            if not hits:
                print(f"No more results found for parameters: {params}")
                break

            # Extract URLs from the search results
            for result in hits:
                person_url = result.get("personUrl")
                if person_url:
                    links.append(person_url)


        else:
            print(
                f"Failed to retrieve data for page {page} with parameters: {params}. Status code: {response.status_code}")
            break

# Save the links to an Excel file
df = pd.DataFrame({'Links': links})
excel_filename = f"{file_name}.xlsx"
df.to_excel(excel_filename, index=False)

print(f"Data saved to {excel_filename}")
