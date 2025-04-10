import asyncio
import aiohttp
import aiofiles
import os
from uuid import uuid4

ARTIFACTS_DIR = "artifacts/artifacts_1"
URL = "https://thispersondoesnotexist.com/"

async def fetch_image(session, idx):
    try:
        async with session.get(URL) as response:
            if response.status == 200:
                img_bytes = await response.read()
                filename = os.path.join(ARTIFACTS_DIR, f"{uuid4().hex}_{idx}.jpg")
                async with aiofiles.open(filename, "wb") as f:
                    await f.write(img_bytes)
                print(f"Downloaded: {filename}")
            else:
                print(f"Failed to fetch image {idx}, status: {response.status}")
    except Exception as e:
        print(f"Error fetching image {idx}: {e}")

async def main(n_images: int):
    os.makedirs(ARTIFACTS_DIR, exist_ok=True)
    timeout = aiohttp.ClientTimeout(total=20)
    headers = {"User-Agent": "Mozilla/5.0"}

    async with aiohttp.ClientSession(timeout=timeout, headers=headers) as session:
        tasks = [fetch_image(session, i) for i in range(n_images)]
        await asyncio.gather(*tasks)

if __name__ == "__main__":
    import sys
    n = int(sys.argv[1]) if len(sys.argv) > 1 else 10
    asyncio.run(main(n))
