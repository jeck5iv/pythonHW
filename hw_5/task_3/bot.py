import asyncio
import json
from aiogram import Bot, Dispatcher
from aiogram.types import Message
from aiogram.filters import CommandStart
from aiogram.utils.markdown import hlink
from aiogram.enums import ParseMode
from dotenv import load_dotenv
from config import TELEGRAM_TOKEN
from aiogram.client.default import DefaultBotProperties

# загружаем токен
load_dotenv()

bot = Bot(token=TELEGRAM_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dp = Dispatcher()

subscriptions = {}

def add_subscription(chat_id, filter_text):
    if chat_id not in subscriptions:
        subscriptions[chat_id] = []
    if filter_text not in subscriptions[chat_id]:
        subscriptions[chat_id].append(filter_text)

@dp.message(CommandStart())
async def cmd_start(message: Message):
    await message.answer("Привет! Напиши мне фильтр: \"/subscribe Петроградская\" или \"/subscribe студия\"")

@dp.message()
async def handle_message(message: Message):
    if message.text.startswith("/subscribe"):
        filter_text = message.text.replace("/subscribe", "").strip()
        add_subscription(message.chat.id, filter_text)
        await message.answer(f"Подписал на объявления с фильтром: {filter_text}")
    else:
        await message.answer("Неизвестная команда")

# проверка обновлений в базе и отправка сообщений
async def check_updates():
    last_known_ids = set()
    while True:
        try:
            with open("data.json", "r", encoding="utf-8") as f:
                data = json.load(f)
            ads = data.get("results", [])

            new_ads = [ad for ad in ads if ad["link"] not in last_known_ids]

            for ad in new_ads:
                for chat_id, filters in subscriptions.items():
                    if any(
                        filter_text.lower() in ad["title"].lower() or
                        filter_text.lower() in ad["price"].lower() or
                        filter_text.lower() in ad["address"].lower() or
                        filter_text.lower() in ad["link"].lower()
                        for filter_text in filters
                    ):
                        text = (
                            f"<b>{ad['title']}</b>\n"
                            f"{ad['price']}₽\n"
                            f"{ad['address']}\n"
                            f"<a href=\"{ad['link']}\">Ссылка</a>"
                        )
                        try:
                            await bot.send_message(chat_id, text)
                            last_known_ids.add(ad["link"])
                        except Exception as e:
                            print(f"Не удалось отправить сообщение пользователю {chat_id}: {e}")
        except Exception as e:
            print(f"Ошибка в check_updates: {e}")

        await asyncio.sleep(10)

async def main():
    asyncio.create_task(check_updates())
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
