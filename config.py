import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv('BOT_TOKEN')
BASE_URL = os.getenv('BASE_URL')

if not BOT_TOKEN:
    raise ValueError("Переменная BOT_TOKEN не найдена в файле .env!")
if not BASE_URL:
    raise ValueError("Переменная BASE_URL не найдена в файле .env!")

class APIEndpoints:
    PROFILE_BY_NICK = "/api/profiles/by-nick/{nick}"