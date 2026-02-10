"""
Тестовый скрипт для проверки работы системы.
"""
from src.models.schemas import UserInput
from src.graph.workflow import MealPlannerWorkflow
from src.utils.visualizer import print_weekly_plan, export_to_markdown
import json


def test_system():
    """Тестирует систему с различными входными данными."""
    
    # Тест 1: Веган, похудение
    print("\n" + "="*60)
    print("ТЕСТ 1: Веган, цель - похудение")
    print("="*60)
    
    user_input_1 = UserInput(
        goal="lose_weight",
        gender="male",
        weight=85.0,
        height=180.0,
        age=30,
        preferences="веган"
    )
    
    workflow = MealPlannerWorkflow()
    final_state_1 = workflow.run(user_input_1)
    
    if final_state_1.get("final_plan"):
        print("\n✅ Тест 1 пройден успешно!")
        plan_dict_1 = final_state_1["final_plan"].model_dump()
        with open("test1_vegan_lose_weight.json", "w", encoding="utf-8") as f:
            json.dump(plan_dict_1, f, ensure_ascii=False, indent=2)
        export_to_markdown(plan_dict_1, "test1_vegan_lose_weight.md")
        print("Результаты сохранены: test1_vegan_lose_weight.json, test1_vegan_lose_weight.md")
    else:
        print("\n❌ Тест 1 не пройден")
    
    # Тест 2: Без особых предпочтений, набор массы
    print("\n" + "="*60)
    print("ТЕСТ 2: Нет предпочтений, цель - набор массы")
    print("="*60)
    
    user_input_2 = UserInput(
        goal="gain_weight",
        gender="female",
        weight=55.0,
        height=165.0,
        age=25,
        preferences="Нет особых предпочтений"
    )
    
    final_state_2 = workflow.run(user_input_2)
    
    if final_state_2.get("final_plan"):
        print("\n✅ Тест 2 пройден успешно!")
        plan_dict_2 = final_state_2["final_plan"].model_dump()
        with open("test2_gain_weight.json", "w", encoding="utf-8") as f:
            json.dump(plan_dict_2, f, ensure_ascii=False, indent=2)
        export_to_markdown(plan_dict_2, "test2_gain_weight.md")
        print("Результаты сохранены: test2_gain_weight.json, test2_gain_weight.md")
    else:
        print("\n❌ Тест 2 не пройден")
    
    # Тест 3: Вегетарианец, поддержание веса
    print("\n" + "="*60)
    print("ТЕСТ 3: Вегетарианец, цель - поддержание веса")
    print("="*60)
    
    user_input_3 = UserInput(
        goal="maintain",
        gender="male",
        weight=75.0,
        height=175.0,
        age=35,
        preferences="вегетарианец, без глютена"
    )
    
    final_state_3 = workflow.run(user_input_3)
    
    if final_state_3.get("final_plan"):
        print("\n✅ Тест 3 пройден успешно!")
        plan_dict_3 = final_state_3["final_plan"].model_dump()
        with open("test3_vegetarian_maintain.json", "w", encoding="utf-8") as f:
            json.dump(plan_dict_3, f, ensure_ascii=False, indent=2)
        export_to_markdown(plan_dict_3, "test3_vegetarian_maintain.md")
        print("Результаты сохранены: test3_vegetarian_maintain.json, test3_vegetarian_maintain.md")
    else:
        print("\n❌ Тест 3 не пройден")
    
    print("\n" + "="*60)
    print("✅ ВСЕ ТЕСТЫ ЗАВЕРШЕНЫ")
    print("="*60)


if __name__ == "__main__":
    test_system()

