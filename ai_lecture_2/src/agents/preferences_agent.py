"""
Агент для анализа пищевых предпочтений и подбора продуктов.
"""
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import ChatPromptTemplate
from langchain.output_parsers import PydanticOutputParser

from src.models.schemas import UserInput, PreferencesAnalysis
from src.utils.config import MODEL_NAME, TEMPERATURE


class PreferencesAgent:
    """Агент для анализа пищевых предпочтений пользователя."""
    
    def __init__(self):
        """Инициализация агента."""
        self.llm = ChatGoogleGenerativeAI(
            model=MODEL_NAME,
            temperature=TEMPERATURE,
            convert_system_message_to_human=True
        )
        self.output_parser = PydanticOutputParser(pydantic_object=PreferencesAnalysis)
        
        self.prompt = ChatPromptTemplate.from_messages([
            ("system", """Ты эксперт по пищевым предпочтениям и ограничениям в питании.
Твоя задача - проанализировать предпочтения пользователя и составить:
1. Список разрешенных продуктов (минимум 30-40 продуктов)
2. Список запрещенных продуктов
3. Рекомендации по выбору продуктов

Учитывай различные типы диет:
- Веган: исключить все животные продукты
- Вегетарианец: исключить мясо и рыбу
- Без глютена: исключить пшеницу, рожь, ячмень
- Без лактозы: исключить молочные продукты
- Палео: натуральные продукты, без обработанных

Для каждой диеты предложи богатый выбор продуктов из следующих категорий:
- Белковые продукты
- Углеводные продукты (крупы, злаки)
- Овощи и зелень
- Фрукты
- Источники жиров
- Специи и приправы

{format_instructions}"""),
            ("user", """Проанализируй следующие пищевые предпочтения:

Предпочтения: {preferences}
Цель: {goal}

Составь подробный список разрешенных и запрещенных продуктов, а также дай рекомендации.""")
        ])
    
    def analyze(self, user_input: UserInput) -> PreferencesAnalysis:
        """
        Анализирует пищевые предпочтения пользователя.
        
        Args:
            user_input: Входные данные пользователя
            
        Returns:
            PreferencesAnalysis: Результат анализа
        """
        # Подготовка промпта
        formatted_prompt = self.prompt.format_messages(
            preferences=user_input.preferences,
            goal=user_input.goal,
            format_instructions=self.output_parser.get_format_instructions()
        )
        
        # Вызов LLM
        response = self.llm.invoke(formatted_prompt)
        
        # Парсинг ответа
        preferences_analysis = self.output_parser.parse(response.content)
        
        return preferences_analysis

