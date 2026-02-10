"""
Pydantic модели для данных системы.
"""
from typing import Literal, Optional, Dict, List, TypedDict
from pydantic import BaseModel, Field


class UserInput(BaseModel):
    """Входные данные от пользователя."""
    goal: Literal["lose_weight", "gain_weight", "maintain"] = Field(
        description="Цель: похудеть, набрать вес или поддерживать"
    )
    gender: Literal["male", "female"] = Field(description="Пол")
    weight: float = Field(description="Вес в кг", gt=0)
    height: float = Field(description="Рост в см", gt=0)
    age: int = Field(description="Возраст", gt=0, lt=120)
    preferences: str = Field(
        description="Пищевые предпочтения (например: веган, без глютена)"
    )


class NutritionAnalysis(BaseModel):
    """Результат анализа физических показателей."""
    bmr: float = Field(description="Базальный метаболизм (калории)")
    daily_calories: float = Field(description="Рекомендуемые калории в день")
    protein_g: float = Field(description="Белки в граммах")
    carbs_g: float = Field(description="Углеводы в граммах")
    fats_g: float = Field(description="Жиры в граммах")
    recommendations: str = Field(description="Рекомендации по питанию")


class PreferencesAnalysis(BaseModel):
    """Результат анализа предпочтений."""
    allowed_foods: List[str] = Field(description="Разрешенные продукты")
    restricted_foods: List[str] = Field(description="Запрещенные продукты")
    recommendations: str = Field(description="Рекомендации по продуктам")


class DayMeal(BaseModel):
    """Прием пищи."""
    name: str = Field(description="Название приема пищи")
    time: str = Field(description="Время приема пищи")
    foods: List[str] = Field(description="Список продуктов")
    calories: float = Field(description="Калорийность")
    protein_g: float = Field(description="Белки в граммах")
    carbs_g: float = Field(description="Углеводы в граммах")
    fats_g: float = Field(description="Жиры в граммах")


class DailyPlan(BaseModel):
    """План питания на день."""
    day: str = Field(description="День недели")
    meals: List[DayMeal] = Field(description="Приемы пищи")
    total_calories: float = Field(description="Общая калорийность")
    total_protein_g: float = Field(description="Общее количество белков")
    total_carbs_g: float = Field(description="Общее количество углеводов")
    total_fats_g: float = Field(description="Общее количество жиров")


class WeeklyMealPlan(BaseModel):
    """Недельный план питания."""
    week_plan: List[DailyPlan] = Field(description="План на неделю")
    summary: str = Field(description="Общее резюме плана")


class GraphState(TypedDict, total=False):
    """Состояние графа LangGraph."""
    user_input: UserInput
    nutrition_analysis: NutritionAnalysis
    preferences_analysis: PreferencesAnalysis
    final_plan: WeeklyMealPlan
    error: str

