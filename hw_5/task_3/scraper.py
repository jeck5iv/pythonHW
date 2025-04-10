import asyncio
import aiohttp
import json
from datetime import datetime
from bs4 import BeautifulSoup

AVITO_URL = "https://www.avito.ru/sankt-peterburg/kvartiry/prodam-ASgBAgICAUSSA8YQ?context=H4sIAAAAAAAA_wEjANz_YToxOntzOjg6ImZyb21QYWdlIjtzOjc6ImNhdGFsb2ciO312FITcIwAAAA&p=1"

HEADERS = {
    "User-Agent": "Mozilla/5.0"
}

async def fetch_html(session, url):
    async with session.get(url) as response:
        return await response.text()

async def parse_avito_page(session):
    html = await fetch_html(session, AVITO_URL)
    soup = BeautifulSoup(html, "html.parser")

    ads = []
    items = soup.select('[data-marker="item"]')

    for item in items:
        try:
            title_elem = item.select_one('[itemprop="name"]')
            title = title_elem.text.strip() if title_elem else "N/A"

            price_elem = item.select_one('[itemprop="price"]')
            price = price_elem.get("content") if price_elem else "N/A"

            address_elem = item.select_one('[data-marker="item-address"]')
            address = address_elem.text.strip() if address_elem else "N/A"

            link_elem = item.select_one('a[data-marker="item-title"]')
            link = f"https://www.avito.ru{link_elem.get('href')}" if link_elem else "N/A"

            ads.append({
                "title": title,
                "price": price,
                "address": address,
                "link": link
            })
        except Exception:
            continue

    return ads

async def save_ads(ads):
    filename = "data.json"
    with open(filename, "w", encoding="utf-8") as f:
        json.dump({
            "timestamp": datetime.now().isoformat(),
            "results": ads
        }, f, indent=2, ensure_ascii=False)

async def periodic_scrape(interval=300):
    async with aiohttp.ClientSession(headers=HEADERS) as session:
        while True:
            print("Fetching new ads...")
            ads = await parse_avito_page(session)
            print(f"Found {len(ads)} ads.")
            await save_ads(ads)
            print(f"Saved to data.json")
            await asyncio.sleep(interval)

if __name__ == "__main__":
    asyncio.run(periodic_scrape())
