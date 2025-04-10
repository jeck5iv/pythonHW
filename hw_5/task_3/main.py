import asyncio
from bot import check_updates, main as bot_main
from scraper import periodic_scrape

async def main():
    asyncio.create_task(check_updates())
    asyncio.create_task(periodic_scrape())

    await bot_main()

if __name__ == "__main__":
    asyncio.run(main())
