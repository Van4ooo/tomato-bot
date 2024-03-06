import os
import sys

from aiogram import Bot
from dotenv import load_dotenv


current_dir = os.path.dirname(os.path.abspath(__file__))
project_dir = os.path.abspath(os.path.join(current_dir, os.pardir))
env_path = os.path.join(project_dir, ".env")

load_dotenv(env_path)

if not os.getenv("BOT_TOKEN"):
    print("[ERROR] Введіть токен бота в файл .env", file=sys.stderr)
    sys.exit(1)

bot = Bot(token=os.getenv("BOT_TOKEN"))

__all__ = ('bot', )
