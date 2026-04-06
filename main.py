import requests
import time

WEBHOOK_URL = "https://discord.com/api/webhooks/1490646676262883350/erTfPJAGQ6Gbo1h6xkQ3bzAWFs9Viet-ZfjMhtTf-Illyjh5Q9r0aQEAzRC_mijXH-aH"
SEARCH_URL = "https://www.vinted.pl/api/v2/catalog/items?search_text=playstation"

seen_ids = set()

def is_valid(item):
    title = item["title"].lower()

    # musi zawierać PS4/PS5
    if not any(x in title for x in ["ps4", "ps5", "playstation 4", "playstation 5"]):
        return False

    # odrzucamy pojedyncze rzeczy
    blocked = ["pad", "kontroler", "controller", "kabel", "ładowarka", "zasilacz", "sluchawki", "słuchawki"]

    if any(x in title for x in blocked):
        return False

    # ALE jeśli jest konsola + coś (np pad) to OK
    if any(x in title for x in ["ps4", "ps5"]):
        return True

    return True


def get_items():
    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    try:
        r = requests.get(SEARCH_URL, headers=headers)
        return r.json().get("items", [])
    except Exception as e:
        print("Błąd pobierania:", e)
        return []


def send(item):
    image_url = None
    if "photo" in item and item["photo"]:
        image_url = item["photo"]["url"]

    embed = {
        "title": item["title"],
        "url": item["url"],
        "description": f"💰 {item['price']} zł",
        "color": 5814783
    }

    if image_url:
        embed["image"] = {"url": image_url}

    data = {
        "embeds": [embed]
    }

    try:
        requests.post(WEBHOOK_URL, json=data)
        print("Wysłano:", item["title"])
    except Exception as e:
        print("Błąd wysyłania:", e)


print("Bot działa...")

while True:
    try:
        items = get_items()

        for item in items:
            if item["id"] not in seen_ids and is_valid(item):
                seen_ids.add(item["id"])
                send(item)

        time.sleep(60)

    except Exception as e:
        print("Błąd główny:", e)
        time.sleep(60)
