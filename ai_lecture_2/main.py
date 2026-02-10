"""
Главный файл для запуска агентной системы составления рациона питания.
"""
import json
from typing import Literal

from src.models.schemas import UserInput
from src.graph.workflow import MealPlannerWorkflow
from src.utils.visualizer import (
    print_weekly_plan,
    print_shopping_list,
    export_to_markdown
)


def save_plan_to_json(plan_data: dict, filename: str = "meal_plan.json"):
    """
    Сохраняет план питания в JSON файл.
    
    Args:
        plan_data: Данные плана
        filename: Имя файла для сохранения
    """
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(plan_data, f, ensure_ascii=False, indent=2)
    print(f"\n💾 План сохранен в файл: {filename}")


def print_plan_summary(final_state):
    """
    Выводит краткую информацию о плане.
    
    Args:
        final_state: Финальное состояние графа
    """
    if final_state.get("error"):
        print(f"\n❌ Произошла ошибка: {final_state['error']}")
        return
    
    if not final_state.get("final_plan"):
        print("\n❌ План не был создан")
        return
    
    # Используем улучшенную визуализацию
    plan_dict = final_state["final_plan"].model_dump()
    print_weekly_plan(plan_dict)
    print_shopping_list(plan_dict)


def get_user_input_interactive() -> UserInput:
    """
    Интерактивный ввод данных пользователя.
    
    Returns:
        UserInput: Валидированные входные данные
    """
    print("\n" + "="*60)
    print("🍽️  СИСТЕМА СОСТАВЛЕНИЯ ПЕРСОНАЛЬНОГО РАЦИОНА ПИТАНИЯ")
    print("="*60)
    print("\nВведите ваши данные:\n")
    
    # Цель
    print("Цель (введите номер):")
    print("1. Похудеть")
    print("2. Набрать вес")
    print("3. Поддерживать вес")
    goal_input = input("Ваш выбор (1-3): ").strip()
    
    goal_map = {
        "1": "lose_weight",
        "2": "gain_weight",
        "3": "maintain"
    }
    goal = goal_map.get(goal_input, "maintain")
    
    # Пол
    print("\nПол (введите номер):")
    print("1. Мужской")
    print("2. Женский")
    gender_input = input("Ваш выбор (1-2): ").strip()
    
    gender_map = {
        "1": "male",
        "2": "female"
    }
    gender = gender_map.get(gender_input, "male")
    
    # Физические показатели
    weight = float(input("\nВес (кг): ").strip())
    height = float(input("Рост (см): ").strip())
    age = int(input("Возраст (лет): ").strip())
    
    # Предпочтения
    print("\nПищевые предпочтения:")
    print("(например: веган, вегетарианец, без глютена, без лактозы, палео)")
    preferences = input("Ваши предпочтения: ").strip()
    
    if not preferences:
        preferences = "Нет особых предпочтений"
    
    return UserInput(
        goal=goal,
        gender=gender,
        weight=weight,
        height=height,
        age=age,
        preferences=preferences
    )


def main():
    """Главная функция."""
    try:
        # Получаем данные от пользователя
        user_input = get_user_input_interactive()
        
        # Создаем workflow
        workflow = MealPlannerWorkflow()
        
        # Запускаем систему
        final_state = workflow.run(user_input)
        
        # Выводим результаты
        print_plan_summary(final_state)
        
        # Сохраняем в JSON и Markdown
        if final_state.get("final_plan"):
            plan_dict = final_state["final_plan"].model_dump()
            save_plan_to_json(plan_dict)
            export_to_markdown(plan_dict)
            
            print("\n" + "="*60)
            print("✨ Ваш персональный план питания готов!")
            print("📄 Файлы: meal_plan.json, meal_plan.md")
            print("="*60)
        
    except KeyboardInterrupt:
        print("\n\n❌ Программа прервана пользователем")
    except Exception as e:
        print(f"\n❌ Произошла ошибка: {e}")
        import traceback
        traceback.print_exc()


def run_example():
    """Запускает пример с предустановленными данными."""
    print("\n" + "="*60)
    print("🔬 ЗАПУСК ПРИМЕРА С ТЕСТОВЫМИ ДАННЫМИ")
    print("="*60)
    
    # Тестовые данные
    user_input = UserInput(
        goal="lose_weight",
        gender="male",
        weight=85.0,
        height=180.0,
        age=30,
        preferences="веган"
    )
    
    print("\nТестовые данные:")
    print(f"  Цель: Похудеть")
    print(f"  Пол: Мужской")
    print(f"  Вес: 85 кг")
    print(f"  Рост: 180 см")
    print(f"  Возраст: 30 лет")
    print(f"  Предпочтения: веган")
    
    # Создаем workflow
    workflow = MealPlannerWorkflow()
    
    # Запускаем систему
    final_state = workflow.run(user_input)
    
    # Выводим результаты
    print_plan_summary(final_state)
    
    # Сохраняем в JSON
    if final_state.final_plan:
        plan_dict = final_state.final_plan.model_dump()
        save_plan_to_json(plan_dict, "example_meal_plan.json")


if __name__ == "__main__":
    # Раскомментируйте нужную функцию:
    
    # Интерактивный режим
    main()
    
    # Или запуск примера
    # run_example()

