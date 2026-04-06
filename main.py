import requests
import time

WEBHOOK_URL = "https://discord.com/api/webhooks/1490646676262883350/erTfPJAGQ6Gbo1h6xkQ3bzAWFs9Viet-ZfjMhtTf-Illyjh5Q9r0aQEAzRC_mijXH-aH"

def get_items():
    headers = {
        "User-Agent": "Mozilla/5.0"
    }
    url = "https://www.vinted.pl/api/v2/catalog/items?search_text=ps5"
    r = requests.get(url, headers=headers)
    return r.json()["items"]

while True:
    try:
        items = get_items()

        print("Znaleziono ofert:", len(items))  # żebyś widział że działa

        for item in items[:5]:  # bierze 5 pierwszych
            requests.post(WEBHOOK_URL, json={
                "content": f"{item['title']}\n{item['price']} zł\n{item['url']}"
            })

        time.sleep(60)

    except Exception as e:
        print("Błąd:", e)
        time.sleep(60)
