import aiohttp
import asyncio
import brotli

async def fetch(session, url, headers, data):
    async with session.post(url, headers=headers, json=data) as response:
        print(f"Request Headers: {headers}")
        print(f"Request Data: {data}")
        print(f"Response Status: {response.status}")
        if response.status == 200:
            return await response.json()
        else:
            print(f"Failed with status {response.status}")
            return None

async def main():
    url = "https://www.ratsit.se/api/search/person"
    headers = {
        "Accept": "application/json, text/plain, */*",
        "Accept-Encoding": "gzip, deflate, br",  # Brotli encoding (br) included here
        "Accept-Language": "en-US,en;q=0.9",
        "Content-Type": "application/json",
        "Cookie": "CookieConsent={stamp:%27FZbmi5v0GylKxV/u0IM44711ExFFLYMPg881T6fR+QTSeT0AqUxtxw==%27%2Cnecessary:true%2Cpreferences:true%2Cstatistics:true%2Cmarketing:true%2Cmethod:%27explicit%27%2Cver:3%2Cutc:1726949137638%2Ciab2:%27CQFTH0AQFTH0ACGABBENBHFsAP_gAEPgAAAAKbtV_G__bWlr8X73aftkeY1P9_h77sQxBhfJE-4FzLvW_JwXx2ExNA36tqIKmRIAu3bBIQNlGJDUTVCgaogVryDMaE2coTNKJ6BkiFMRM2dYCF5vm4tj-QKY5vr991dx2B-t7dr83dzyz4VHn3a5_2a0WJCdA5-tDfv9bROb-9IOd_x8v4v8_F_rE2_eT1l_tWvp7D9-cts7_XW89_fff_9Ln_-uB_-_2CmQBJhoVEAZYEhIQaBhBAgBUFYQEUCAAAAEgaICAEwYFOwMAl1hIgBACgAGCAEAAKMgAQAAAQAIRABAAUCAACAQKAAMACAYCAAgYAAQAWAgEAAIDoGKYEECgWACRmREKYEIQCQQEtlQgkAQIK4QhFngEQCImCgAAAAAKwABAWCwOJJASoSCBLiDaAAAgAQCCAAoQScmAAIAzZag8GTaMrTANHzBIhpgGQAA.YAAAAAAAAAA%27%2Cgacm:%272~AAAAAAAAAAACAABAAAgAIAAABAAAAAAACAAAAAAAAAAQAAAAAAABABAAAAAAAAAAAAAAAQAAAAAAAAAAAgMAAAAAAAgAAAACAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAgAAAAAAAAAAAAAAAAAAEAAAAAAAAAAAQAAAAAAFAAAAAAAAAAAAAAAAABAAAAAAAAAAACAAABAAAAAAAAAAAAAAAAAABAQAAAEAAAAAAAAAAAAAAAAAAACBAAAAAAAAAAAAQAAAAAAAAAAgAAAAAAAQAAAAAAAAAAAAAAAACAgBAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAIAAAAAAAAAAAAAAAAAAAAAAAAAAAAAEAAAAAAAAAAgAAAAABAAAAAAAAAAAAAAAAAAAAAAAAAAAAgAAAAAAkQAAAAAAAAAAAAAAAAQ=fmR2Lg==AA==%27%2Cregion:%27se%27}; _gcl_au=1.1.322227372.1726949135; _ga=GA1.1.362860978.1726949135; gtm_upi=ZmgySnplTVlXNUJNcUJvbWIxeTYxK1MxVUsrV2pTaHdYTlphb2lmOHBjaz; _tt_enable_cookie=1; _ttp=e6OtzdU99uan-S-vFkahUpo1qQt; lwuid=gnlwc5340f1c-c925-4bb2-b97d-92e774e6615b; _clck=y3i82g%7C2%7Cfqm%7C0%7C1770; .AspNetCore.Antiforgery.73XflXSd7TU=CfDJ8JyZhnBfggVClOTwXXWQB1naaqgCW2mzcG-MF9TqEqyv3JORbo02y2iq2fpxHF_TfoKJkRhciqg2AT-BO6-vFphEe0jcuJj-SovOVfM9svxrWKSThO10oCFMi8c_3Gi5IE6QkzvT5UzMBct6gPmLqc4; .AspNetCore.Cookies=CfDJ8JyZhnBfggVClOTwXXWQB1njcz-3H5JLFzW3QGptevb804K1G8fxcgKUwBj120kywiPDh-Y90-4ZduxrxfbhMeeQHNoa4K1D2dQF1zAi82yzLUc_-uG6alvMmbe4eqN53dodIO5-QEQSSfqx5pN6hX_ye-c8ieAq-mhZHfcgI4nm40A2Uf2i86yJZd3c70u3eS49fdLtcZ9E-Bjd0n3l_RoFPVhQr1zbxasAQOPHXgQBuD-JsMmEkKMZhfrgpNz8q5kqlMkt5maeKPkqFJrFRObLMRgtmO4bpf6HYuxDZZjUdvQW7gDrKXnI_ADQ-AR4hqlJwDMNvrUrL3Hp1rcnTeoRow5E49OZlh7xyM2pGrpt3xi5CzsfZoicnizd4UGWUe2Xnx7U1l0EvWlGx_Lw22LAlawYsp985rIaje3wAFPAgel_Nz3A9TZn5tLAgWE_SvOMcczkjcsUC6XD7UIgFGUrtJz4Hc-O0JA2uD0imvGCHg2C-ok9lsX48T1R3M1pOKgpl4S0Y5fWlq5PQ1YYmpsvoluHAoEtWqFgDt8hzda9rsau_-1LRMMaJGrPqK6TeD51sbyO0HZ2enT7QJ1bNlIXD-BmuXl7eXU460vkRFROAUVvbZMWBs9HcpQiAR6l628xZiUq9I53TdzZ7MBCfqIsGVFQVKrJIayOkYfZuCk6Aqt9VImPWMowbjGJAhrHlZCOBeljLP1wTc2vPpFateXXwNpCUwbF9lZbdultaOk49EPvhrXCXdfYUBVjW6tL-T3cRzibHTIJYjA3_O8oo78HTQxHBp_-lvM1t_no5yiT6WvaSAtxAOJ_MVzZNg_8uAfkRSxcKHtBrdLbCAE55nvloVrZsvV_JjLFhn4Yn4U5LUWfj4Qr-hDFf8i8l75NtJiQSZXoOB3sdt4HEjMsHsIlL_4jfBpMh1Te0zClQyw-cSfXSIFSbipZraanUpNbpN7udqYtxJqtKGowyiXpl7ICc1M52R_Px4RdHtRbiqkP_TrGTDIfxlOMCZl-nLQsr9X_ZYaH1wtbLm97S3AZzuE; _return_url=%7B%22Url%22%3A%22%2F19240419-Rut_Louise_Holmgren_Arjeplog%2FWnU9grZBIgA8KrMuGqdLEAkYBMJhaeJpbkFn-5DGv9I%22%2C%22Text%22%3A%22personrapporten%22%7D; wisepops=%7B%22popups%22%3A%7B%7D%2C%22sub%22%3A0%2C%22ucrn%22%3A33%2C%22cid%22%3A%2250552%22%2C%22v%22%3A4%2C%22bandit%22%3A%7B%22recos%22%3A%7B%7D%7D%7D; wisepops_props=%7B%22uid%22%3A%221849064%22%2C%22ue%22%3A%22dean.daniels3%40outlook.com%22%2C%22uds%22%3A%222023-01-03%22%2C%22srpat%22%3A%22false%22%2C%22srpap%22%3A%22false%22%2C%22srpapr%22%3A%22false%22%2C%22srpna%22%3A%22false%22%2C%22pvn%22%3A%22null%22%2C%22cvn%22%3A%22null%22%2C%22pt%22%3A%22other%22%2C%22companypage%22%3A%22null%22%2C%22personpage%22%3A%22null%22%7D; wisepops_visitor=%7B%22AX7MUsC3EZ%22%3A%22842960d8-57b4-40a6-8288-12ed62d7d45d%22%7D; wisepops_visits=%5B%222024-11-05T17%3A24%3A27.915Z%22%2C%222024-11-05T17%3A24%3A21.345Z%22%2C%222024-11-05T17%3A23%3A41.178Z%22%2C%222024-11-05T17%3A23%3A34.047Z%22%2C%222024-11-05T17%3A23%3A20.712Z%22%2C%222024-11-05T17%3A23%3A06.147Z%22%2C%222024-11-05T17%3A22%3A33.227Z%22%2C%222024-11-05T17%3A22%3A30.071Z%22%2C%222024-11-05T17%3A22%3A14.435Z%22%2C%222024-11-05T17%3A22%3A07.806Z%22%5D; wisepops_session=%7B%22arrivalOnSite%22%3A%222024-11-05T17%3A24%3A27.915Z%22%2C%22mtime%22%3A1730827468387%2C%22pageviews%22%3A1%2C%22popups%22%3A%7B%7D%2C%22bars%22%3A%7B%7D%2C%22sticky%22%3A%7B%7D%2C%22countdowns%22%3A%7B%7D%2C%22src%22%3Anull%2C%22utm%22%3A%7B%7D%2C%22testIp%22%3Anull%7D; _uetsid=4e91ce809b9111efa50e4bbeab194826; _uetvid=4e91cbe09b9111efab1ad9d36d129745; _clsk=1a1u01y%7C1730827469007%7C18%7C0%7Cw.clarity.ms%2Fcollect; _ga_C2F6LZXLZK=GS1.1.1730826655.2.1.1730827480.39.1.858039711",  # Replace with your actual cookies
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36"
    }
    data = {
        "who": "Arjeplog",
        "age": ["16", "120"],
        "phoneticSearch": True,
        "firstName": "",
        "lastName": "",
        "page": 2
    }

    async with aiohttp.ClientSession() as session:
        response = await fetch(session, url, headers, data)
        if response:
            print(response)

# Run the async main function
asyncio.run(main())
