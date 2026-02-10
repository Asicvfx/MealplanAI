"""
Агент для анализа физических показателей и расчета макронутриентов.
"""
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain.output_parsers import PydanticOutputParser

from src.models.schemas import UserInput, NutritionAnalysis
from src.utils.config import MODEL_NAME, TEMPERATURE


class NutritionAgent:
    """Агент для анализа питания на основе физических показателей."""
    
    def __init__(self):
        """Инициализация агента."""
        self.llm = ChatOpenAI(
            model=MODEL_NAME,
            temperature=TEMPERATURE
        )
        self.output_parser = PydanticOutputParser(pydantic_object=NutritionAnalysis)
        
        self.prompt = ChatPromptTemplate.from_messages([
            ("system", """Ты эксперт-диетолог с глубокими знаниями в области нутрициологии.
Твоя задача - проанализировать физические показатели пользователя и рассчитать:
1. Базальный метаболизм (BMR) по формуле Миффлина-Сан Жеора
2. Дневную норму калорий с учетом цели
3. Оптимальное соотношение макронутриентов (белки, жиры, углеводы)
4. Рекомендации по питанию

Для расчета BMR используй формулы:
- Мужчины: BMR = 10 × вес(кг) + 6.25 × рост(см) - 5 × возраст + 5
- Женщины: BMR = 10 × вес(кг) + 6.25 × рост(см) - 5 × возраст - 161

Для расчета дневной нормы калорий:
- Похудение: BMR × 1.2 - 500 ккал
- Набор массы: BMR × 1.5 + 300 ккал
- Поддержание: BMR × 1.4

Соотношение макронутриентов:
- Похудение: белки 35%, жиры 25%, углеводы 40%
- Набор массы: белки 30%, жиры 20%, углеводы 50%
- Поддержание: белки 30%, жиры 25%, углеводы 45%

{format_instructions}"""),
            ("user", """Проанализируй следующие данные пользователя:

Цель: {goal}
Пол: {gender}
Вес: {weight} кг
Рост: {height} см
Возраст: {age} лет

Рассчитай BMR, дневную норму калорий, макронутриенты и дай рекомендации.""")
        ])
    
    def analyze(self, user_input: UserInput) -> NutritionAnalysis:
        """
        Анализирует физические показатели пользователя.
        
        Args:
            user_input: Входные данные пользователя
            
        Returns:
            NutritionAnalysis: Результат анализа
        """
        # Подготовка промпта
        formatted_prompt = self.prompt.format_messages(
            goal=user_input.goal,
            gender=user_input.gender,
            weight=user_input.weight,
            height=user_input.height,
            age=user_input.age,
            format_instructions=self.output_parser.get_format_instructions()
        )
        
        # Вызов LLM
        response = self.llm.invoke(formatted_prompt)
        
        # Парсинг ответа
        nutrition_analysis = self.output_parser.parse(response.content)
        
        return nutrition_analysis

