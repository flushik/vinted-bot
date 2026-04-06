import requests
import time

WEBHOOK_URL = "https://discord.com/api/webhooks/1490646676262883350/erTfPJAGQ6Gbo1h6xkQ3bzAWFs9Viet-ZfjMhtTf-Illyjh5Q9r0aQEAzRC_mijXH-aH"
SEARCH_URL = "https://www.vinted.pl/api/v2/catalog/items?search_text=playstation"

seen_ids = set()

def is_valid(item):
    title = item["title"].lower()

    # musi być PS4 albo PS5
    if not any(x in title for x in ["ps4", "ps5", "playstation 4", "playstation 5"]):
        return False

    # odrzucamy pojedyncze rzeczy
    if title.startswith(("pad", "kontroler", "gra", "kabel", "ładowarka")):
        return False

    # dodatkowe zabezpieczenie
    if "pad do" in title or "gra na" in title:
        return False

    return True

def get_items():
    r = requests.get(SEARCH_URL)
    return r.json().get("items", [])

def send(item):
    embed = {
        "title": item["title"],
        "url": item["url"],
        "description": f"💸 {item['price']} zł",
        "image": {
            "url": item["photo"]["url"]
        },
        "color": 5814783
    }

    data = {
        "embeds": [embed]
    }

    requests.post(WEBHOOK_URL, json=data)

while True:
    try:
        items = get_items()
        for item in items:
            if item["id"] not in seen_ids and is_valid(item):
                seen_ids.add(item["id"])
                send(item)
        time.sleep(60)
    except Exception as e:
        print(e)
        time.sleep(60)
