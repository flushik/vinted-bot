import requests
import time
import xml.etree.ElementTree as ET

WEBHOOK_URL = "https://discord.com/api/webhooks/1490646676262883350/erTfPJAGQ6Gbo1h6xkQ3bzAWFs9Viet-ZfjMhtTf-Illyjh5Q9r0aQEAzRC_mijXH-aH"

RSS_URL = "https://www.vinted.pl/catalog?search_text=ps5&order=newest_first&per_page=20&rss=true"

seen = set()

def send(title, link):
    data = {
        "content": f"{title}\n{link}"
    }
    requests.post(WEBHOOK_URL, json=data)
    print("Wysłano:", title)


def check():
    r = requests.get(RSS_URL)
    root = ET.fromstring(r.content)

    for item in root.findall(".//item"):
        title = item.find("title").text
        link = item.find("link").text

        if link not in seen:
            seen.add(link)

            # filtr
            t = title.lower()
            if "ps4" in t or "ps5" in t:
                if not any(x in t for x in ["pad", "kontroler", "kabel"]):
                    send(title, link)


print("Bot działa (RSS)...")

while True:
    try:
        check()
        time.sleep(60)
    except Exception as e:
        print("Błąd:", e)
        time.sleep(60)
