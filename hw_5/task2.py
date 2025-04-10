import asyncio
import aiohttp
import aiofiles
import os
import json
from bs4 import BeautifulSoup
from datetime import datetime

ARTIFACTS_DIR = "artifacts/artifacts_2"
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
    os.makedirs(ARTIFACTS_DIR, exist_ok=True)
    filename = os.path.join(ARTIFACTS_DIR, "ads.json")
    async with aiofiles.open(filename, "w") as f:
        await f.write(json.dumps({
            "timestamp": datetime.now().isoformat(),
            "results": ads
        }, indent=2, ensure_ascii=False))

async def periodic_scrape(interval=300):
    async with aiohttp.ClientSession(headers=HEADERS) as session:
        while True:
            print("Fetching new ads...")
            ads = await parse_avito_page(session)
            print(f"Found {len(ads)} ads.")
            await save_ads(ads)
            print(f"Saved to {ARTIFACTS_DIR}/ads.json")
            await asyncio.sleep(interval)

if __name__ == "__main__":
    import sys
    interval = int(sys.argv[1]) if len(sys.argv) > 1 else 300  # интервал 5 минут по дефолту
    asyncio.run(periodic_scrape(interval))
