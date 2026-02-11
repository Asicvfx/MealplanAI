"""
Конфигурация приложения.
"""
import os
from dotenv import load_dotenv

# Загружаем переменные окружения
load_dotenv()

# API ключи
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

# Настройки модели
MODEL_NAME = "gemini-flash-latest"
TEMPERATURE = 0.7

# Проверка наличия API ключа
if not GOOGLE_API_KEY:
    raise ValueError(
        "GOOGLE_API_KEY не найден в переменных окружения. "
        "Пожалуйста, создайте файл .env и добавьте GOOGLE_API_KEY=ваш_ключ"
    )

