"""
Утилиты для визуализации результатов.
"""
import json
from typing import Dict, Any


def print_nutrition_analysis(analysis: Dict[str, Any]) -> None:
    """
    Красиво выводит анализ питания.
    
    Args:
        analysis: Словарь с данными анализа
    """
    print("\n" + "="*60)
    print("📊 АНАЛИЗ ФИЗИЧЕСКИХ ПОКАЗАТЕЛЕЙ")
    print("="*60)
    
    print(f"\n🔥 Базальный метаболизм (BMR): {analysis['bmr']:.0f} ккал")
    print(f"📈 Дневная норма калорий: {analysis['daily_calories']:.0f} ккал")
    
    print("\n💪 Макронутриенты:")
    print(f"  • Белки: {analysis['protein_g']:.0f} г")
    print(f"  • Жиры: {analysis['fats_g']:.0f} г")
    print(f"  • Углеводы: {analysis['carbs_g']:.0f} г")
    
    print(f"\n📝 Рекомендации:")
    print(f"  {analysis['recommendations']}")


def print_preferences_analysis(analysis: Dict[str, Any]) -> None:
    """
    Красиво выводит анализ предпочтений.
    
    Args:
        analysis: Словарь с данными анализа
    """
    print("\n" + "="*60)
    print("🥗 АНАЛИЗ ПИЩЕВЫХ ПРЕДПОЧТЕНИЙ")
    print("="*60)
    
    print(f"\n✅ Разрешенные продукты ({len(analysis['allowed_foods'])} шт.):")
    for i, food in enumerate(analysis['allowed_foods'][:10], 1):
        print(f"  {i}. {food}")
    if len(analysis['allowed_foods']) > 10:
        print(f"  ... и еще {len(analysis['allowed_foods']) - 10} продуктов")
    
    print(f"\n❌ Запрещенные продукты ({len(analysis['restricted_foods'])} шт.):")
    for i, food in enumerate(analysis['restricted_foods'][:10], 1):
        print(f"  {i}. {food}")
    if len(analysis['restricted_foods']) > 10:
        print(f"  ... и еще {len(analysis['restricted_foods']) - 10} продуктов")
    
    print(f"\n📝 Рекомендации:")
    print(f"  {analysis['recommendations']}")


def print_daily_plan(day_plan: Dict[str, Any]) -> None:
    """
    Красиво выводит план на день.
    
    Args:
        day_plan: Словарь с планом на день
    """
    print(f"\n{'='*60}")
    print(f"📅 {day_plan['day'].upper()}")
    print(f"{'='*60}")
    
    for meal in day_plan['meals']:
        print(f"\n🍽️  {meal['name']} ({meal['time']})")
        print(f"   Калории: {meal['calories']:.0f} ккал | "
              f"Б: {meal['protein_g']:.0f}г | "
              f"Ж: {meal['fats_g']:.0f}г | "
              f"У: {meal['carbs_g']:.0f}г")
        print("   Продукты:")
        for food in meal['foods']:
            print(f"     • {food}")
    
    print(f"\n📊 Итого за день:")
    print(f"   Калории: {day_plan['total_calories']:.0f} ккал")
    print(f"   Белки: {day_plan['total_protein_g']:.0f}г | "
          f"Жиры: {day_plan['total_fats_g']:.0f}г | "
          f"Углеводы: {day_plan['total_carbs_g']:.0f}г")


def print_weekly_plan(weekly_plan: Dict[str, Any]) -> None:
    """
    Красиво выводит недельный план.
    
    Args:
        weekly_plan: Словарь с недельным планом
    """
    print("\n" + "="*60)
    print("📋 НЕДЕЛЬНЫЙ ПЛАН ПИТАНИЯ")
    print("="*60)
    
    print(f"\n{weekly_plan['summary']}")
    
    for day_plan in weekly_plan['week_plan']:
        print_daily_plan(day_plan)
    
    # Статистика по неделе
    total_calories = sum(day['total_calories'] for day in weekly_plan['week_plan'])
    avg_calories = total_calories / len(weekly_plan['week_plan'])
    
    print("\n" + "="*60)
    print("📈 СТАТИСТИКА ПО НЕДЕЛЕ")
    print("="*60)
    print(f"\n📊 Средняя калорийность в день: {avg_calories:.0f} ккал")
    print(f"📊 Всего калорий за неделю: {total_calories:.0f} ккал")
    print(f"📊 Дней в плане: {len(weekly_plan['week_plan'])}")


def export_to_markdown(weekly_plan: Dict[str, Any], filename: str = "meal_plan.md") -> None:
    """
    Экспортирует план в Markdown формат.
    
    Args:
        weekly_plan: Словарь с недельным планом
        filename: Имя файла для сохранения
    """
    with open(filename, "w", encoding="utf-8") as f:
        f.write("# 📋 Персональный план питания\n\n")
        f.write(f"{weekly_plan['summary']}\n\n")
        
        for day_plan in weekly_plan['week_plan']:
            f.write(f"## 📅 {day_plan['day']}\n\n")
            f.write(f"**Итого за день:** {day_plan['total_calories']:.0f} ккал ")
            f.write(f"(Б: {day_plan['total_protein_g']:.0f}г, ")
            f.write(f"Ж: {day_plan['total_fats_g']:.0f}г, ")
            f.write(f"У: {day_plan['total_carbs_g']:.0f}г)\n\n")
            
            for meal in day_plan['meals']:
                f.write(f"### {meal['name']} ({meal['time']})\n\n")
                f.write(f"**Калории:** {meal['calories']:.0f} ккал | ")
                f.write(f"Б: {meal['protein_g']:.0f}г | ")
                f.write(f"Ж: {meal['fats_g']:.0f}г | ")
                f.write(f"У: {meal['carbs_g']:.0f}г\n\n")
                f.write("**Продукты:**\n")
                for food in meal['foods']:
                    f.write(f"- {food}\n")
                f.write("\n")
            f.write("---\n\n")
    
    print(f"\n💾 План экспортирован в Markdown: {filename}")


def generate_shopping_list(weekly_plan: Dict[str, Any]) -> Dict[str, int]:
    """
    Генерирует список покупок из недельного плана.
    
    Args:
        weekly_plan: Словарь с недельным планом
        
    Returns:
        Dict: Словарь с продуктами и их количеством (количество упоминаний)
    """
    shopping_list = {}
    
    for day_plan in weekly_plan['week_plan']:
        for meal in day_plan['meals']:
            for food in meal['foods']:
                # Извлекаем название продукта (до первой цифры или спец. символа)
                product_name = food.split()[0] if food else food
                
                if product_name in shopping_list:
                    shopping_list[product_name] += 1
                else:
                    shopping_list[product_name] = 1
    
    return dict(sorted(shopping_list.items(), key=lambda x: x[1], reverse=True))


def print_shopping_list(weekly_plan: Dict[str, Any]) -> None:
    """
    Выводит список покупок.
    
    Args:
        weekly_plan: Словарь с недельным планом
    """
    shopping_list = generate_shopping_list(weekly_plan)
    
    print("\n" + "="*60)
    print("🛒 СПИСОК ПОКУПОК НА НЕДЕЛЮ")
    print("="*60)
    print()
    
    for product, count in shopping_list.items():
        print(f"• {product} (используется в {count} приемах пищи)")

