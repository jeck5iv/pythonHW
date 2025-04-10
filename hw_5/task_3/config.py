import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "data.json")  # путь к файлу с данными от скрапера
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")   # токен бота, для работы поставьте переменную окружения
