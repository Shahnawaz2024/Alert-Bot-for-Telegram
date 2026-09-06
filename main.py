import requests  # type: ignore[import-not-found]
from bs4 import BeautifulSoup  # type: ignore[import-not-found]
import json
import os

STATE_FILE = "seen.json"

def load_seen():
    if os.path.exists(STATE_FILE):
        with open(STATE_FILE) as f:
            return set(json.load(f))
    return set()

def save_seen(seen):
    with open(STATE_FILE, "w") as f:
        json.dump(list(seen), f)

def scrape():
    headers = {"User-Agent": "Mozilla/5.0 (compatible; MyAlertBot/1.0)"}
    r = requests.get("https://example.com/listings", headers=headers, timeout=10)
    soup = BeautifulSoup(r.text, "html.parser")
    items = []
    for card in soup.select(".listing-item"):  # <- adjust selector
        title = card.select_one(".title").text.strip()
        link = card.select_one("a")["href"]
        items.append((title, link))
    return items

def send_telegram(msg):
    token = os.environ["TG_TOKEN"]
    chat_id = os.environ["TG_CHAT_ID"]
    requests.post(
        f"https://api.telegram.org/bot{token}/sendMessage",
        data={"chat_id": chat_id, "text": msg}
    )

def main():
    seen = load_seen()
    items = scrape()
    new_items = [i for i in items if i[1] not in seen]
    for title, link in new_items:
        send_telegram(f"New: {title}\n{link}")
    seen.update(i[1] for i in items)
    save_seen(seen)

if __name__ == "__main__":
    main()