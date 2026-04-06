import requests
import time
from bs4 import BeautifulSoup

WEBHOOK_URL = "https://discord.com/api/webhooks/1490646676262883350/erTfPJAGQ6Gbo1h6xkQ3bzAWFs9Viet-ZfjMhtTf-Illyjh5Q9r0aQEAzRC_mijXH-aH"

URL = "https://www.vinted.pl/catalog?search_text=ps5&order=newest_first"

seen = set()

def send(title, link, price):
    data = {
        "content": f"🔥 {title}\n💰 {price}\n{link}"
    }
    requests.post(WEBHOOK_URL, json=data)

def check():
    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    r = requests.get(URL, headers=headers)

    if r.status_code != 200:
        print("Błąd:", r.status_code)
        return

    soup = BeautifulSoup(r.text, "html.parser")

    items = soup.find_all("a", {"data-testid": "item-link"})
    print("Znaleziono:", len(items))

    for item in items:
        link = "https://www.vinted.pl" + item.get("href")

        title = item.get_text(strip=True)

        if link in seen:
            continue

        seen.add(link)

        t = title.lower()

        if "ps4" in t or "ps5" in t:
            if any(x in t for x in ["pad", "kontroler", "kabel"]):
                continue

            print("Wysłano:", title)
            send(title, link, "sprawdź ofertę")

def main():
    print("Bot działa (SCRAPER)...")

    while True:
        try:
            check()
            time.sleep(30)
        except Exception as e:
            print("Błąd:", e)
            time.sleep(30)

if __name__ == "__main__":
    main()
