"""
Конфигурация приложения.
"""
import os
from dotenv import load_dotenv

# Загружаем переменные окружения
load_dotenv()

# API ключи
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Настройки модели
MODEL_NAME = "gpt-4-turbo-preview"
TEMPERATURE = 0.7

# Проверка наличия API ключа
if not OPENAI_API_KEY:
    raise ValueError(
        "OPENAI_API_KEY не найден в переменных окружения. "
        "Пожалуйста, создайте файл .env и добавьте OPENAI_API_KEY=ваш_ключ"
    )

