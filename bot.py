import requests
from bs4 import BeautifulSoup
import time

URL = "https://www.vinted.pl/catalog?search_text=playstation&order=newest_first"
WEBHOOK = "https://discord.com/api/webhooks/1490457408269455510/4toMRV9vw4AFXguvMJIPXzcrTLOMCPTlChg57npjBCqSHB_QMvBzDnIZUIAxyOzUXfMi"

seen = set()

def send(title, price, link, img):
    data = {
        "embeds": [
            {
                "title": title,
                "url": link,
                "description": f"💰 {price}",
                "image": {"url": img} if img else {}
            }
        ]
    }
    requests.post(WEBHOOK, json=data)

def get_details(link):
    headers = {"User-Agent": "Mozilla/5.0"}
    r = requests.get(link, headers=headers)
    soup = BeautifulSoup(r.text, "html.parser")

    title = soup.find("h1")
    title = title.get_text(strip=True) if title else "Brak tytułu"

    price = soup.find(string=lambda x: "zł" in x if x else False)
    price = price.strip() if price else "Brak ceny"

    img = soup.find("img")
    img = img["src"] if img and img.has_attr("src") else None

    return title, price, img

def check():
    headers = {"User-Agent": "Mozilla/5.0"}
    r = requests.get(URL, headers=headers)
    soup = BeautifulSoup(r.text, "html.parser")

    for a in soup.find_all("a", href=True):
        link = a["href"]

        if "/items/" in link:
            if not link.startswith("http"):
                full_link = "https://www.vinted.pl" + link
            else:
                full_link = link

            if full_link in seen:
                continue

            seen.add(full_link)

            title, price, img = get_details(full_link)
            title_lower = title.lower()

            # musi być PS4 lub PS5
            #if not any(x in title_lower for x in ["ps4", "playstation 4", "ps5", "playstation 5"]):
                continue

            # musi wyglądać na konsolę
            good_words = ["konsola", "console", "zestaw", "bundle"]
            if not any(word in title_lower for word in good_words):
                continue

            # blokujemy śmieci
            bad_words = [
                "fifa", "gra", "gry", "płyta", "cd", "dysk",
                "konto", "psn", "klucz", "kod", "digital",
                "dlc", "season pass"
            ]
            if any(word in title_lower for word in bad_words):
                continue

            # blokujemy słabe oferty
            weak_words = [
                "uszkodzony", "nie działa", "na części",
                "brak", "bez kabla", "sam pad"
            ]
            if any(word in title_lower for word in weak_words):
                continue

            send(title, price, full_link, img)

while True:
    check()
    time.sleep(180)
