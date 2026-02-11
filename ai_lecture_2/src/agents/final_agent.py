"""
Финальный агент для составления недельного плана питания.
"""
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import ChatPromptTemplate
from langchain.output_parsers import PydanticOutputParser

from src.models.schemas import (
    UserInput,
    NutritionAnalysis,
    PreferencesAnalysis,
    WeeklyMealPlan
)
from src.utils.config import MODEL_NAME, TEMPERATURE


class FinalAgent:
    """Финальный агент для создания недельного плана питания."""
    
    def __init__(self):
        """Инициализация агента."""
        self.llm = ChatGoogleGenerativeAI(
            model=MODEL_NAME,
            temperature=TEMPERATURE,
            convert_system_message_to_human=True
        )
        self.output_parser = PydanticOutputParser(pydantic_object=WeeklyMealPlan)
        
        self.prompt = ChatPromptTemplate.from_messages([
            ("system", """Ты опытный диетолог, специализирующийся на составлении индивидуальных планов питания.
Твоя задача - составить детальный план питания на неделю на основе:
1. Анализа физических показателей (калории, макронутриенты)
2. Анализа пищевых предпочтений (разрешенные/запрещенные продукты)

Требования к плану:
- План на 7 дней (Понедельник-Воскресенье)
- 4-5 приемов пищи в день: Завтрак, Перекус, Обед, Полдник, Ужин
- Каждый прием пищи должен содержать конкретные продукты с указанием примерного количества
- Указывай калорийность и макронутриенты для каждого приема пищи
- Соблюдай дневную норму калорий (±50 ккал)
- Соблюдай баланс макронутриентов
- Используй только разрешенные продукты
- Разнообразь меню (не повторяй одинаковые блюда подряд)
- Указывай время приемов пищи

Примерное время приемов пищи:
- Завтрак: 08:00
- Перекус: 11:00
- Обед: 14:00
- Полдник: 17:00
- Ужин: 20:00

{format_instructions}"""),
            ("user", """Составь недельный план питания на основе следующих данных:

=== ПОЛЬЗОВАТЕЛЬСКИЕ ДАННЫЕ ===
Цель: {goal}
Пол: {gender}
Вес: {weight} кг
Рост: {height} см
Возраст: {age} лет
Предпочтения: {preferences}

=== АНАЛИЗ ПИТАНИЯ ===
Дневная норма калорий: {daily_calories} ккал
Белки: {protein_g} г
Жиры: {fats_g} г
Углеводы: {carbs_g} г
Рекомендации: {nutrition_recommendations}

=== АНАЛИЗ ПРЕДПОЧТЕНИЙ ===
Разрешенные продукты: {allowed_foods}
Запрещенные продукты: {restricted_foods}
Рекомендации: {preferences_recommendations}

Составь детальный план питания на неделю с учетом всех указанных параметров.""")
        ])
    
    def create_plan(
        self,
        user_input: UserInput,
        nutrition_analysis: NutritionAnalysis,
        preferences_analysis: PreferencesAnalysis
    ) -> WeeklyMealPlan:
        """
        Создает недельный план питания.
        
        Args:
            user_input: Входные данные пользователя
            nutrition_analysis: Анализ физических показателей
            preferences_analysis: Анализ пищевых предпочтений
            
        Returns:
            WeeklyMealPlan: Недельный план питания
        """
        # Подготовка промпта
        formatted_prompt = self.prompt.format_messages(
            goal=user_input.goal,
            gender=user_input.gender,
            weight=user_input.weight,
            height=user_input.height,
            age=user_input.age,
            preferences=user_input.preferences,
            daily_calories=nutrition_analysis.daily_calories,
            protein_g=nutrition_analysis.protein_g,
            fats_g=nutrition_analysis.fats_g,
            carbs_g=nutrition_analysis.carbs_g,
            nutrition_recommendations=nutrition_analysis.recommendations,
            allowed_foods=", ".join(preferences_analysis.allowed_foods),
            restricted_foods=", ".join(preferences_analysis.restricted_foods),
            preferences_recommendations=preferences_analysis.recommendations,
            format_instructions=self.output_parser.get_format_instructions()
        )
        
        # Вызов LLM
        response = self.llm.invoke(formatted_prompt)
        
        # Парсинг ответа
        weekly_plan = self.output_parser.parse(response.content)
        
        return weekly_plan

