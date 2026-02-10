"""
LangGraph workflow для агентной системы составления рациона.
"""
from typing import Dict, Any
from langgraph.graph import StateGraph, END

from src.models.schemas import GraphState, UserInput
from src.agents.nutrition_agent import NutritionAgent
from src.agents.preferences_agent import PreferencesAgent
from src.agents.final_agent import FinalAgent


class MealPlannerWorkflow:
    """Workflow для создания плана питания."""
    
    def __init__(self):
        """Инициализация workflow."""
        self.nutrition_agent = NutritionAgent()
        self.preferences_agent = PreferencesAgent()
        self.final_agent = FinalAgent()
        self.graph = self._build_graph()
    
    def _build_graph(self) -> StateGraph:
        """
        Строит граф workflow.
        
        Returns:
            StateGraph: Граф состояний
        """
        # Создаем граф
        workflow = StateGraph(GraphState)
        
        # Добавляем узлы
        workflow.add_node("analyze_nutrition", self._analyze_nutrition)
        workflow.add_node("analyze_preferences", self._analyze_preferences)
        workflow.add_node("create_plan", self._create_plan)
        
        # Устанавливаем точку входа
        workflow.set_entry_point("analyze_nutrition")
        
        # Добавляем ребра (связи между узлами)
        # После анализа питания идем к анализу предпочтений
        workflow.add_edge("analyze_nutrition", "analyze_preferences")
        
        # После анализа предпочтений создаем план
        workflow.add_edge("analyze_preferences", "create_plan")
        
        # После создания плана завершаем
        workflow.add_edge("create_plan", END)
        
        # Компилируем граф
        return workflow.compile()
    
    def _analyze_nutrition(self, state: Dict[str, Any]) -> Dict[str, Any]:
        """
        Узел для анализа физических показателей.
        
        Args:
            state: Текущее состояние графа
            
        Returns:
            Dict: Обновленное состояние
        """
        try:
            user_input = state["user_input"]
            
            # Анализируем физические показатели
            nutrition_analysis = self.nutrition_agent.analyze(user_input)
            
            print(f"\n✓ Анализ питания завершен:")
            print(f"  - Дневная норма калорий: {nutrition_analysis.daily_calories} ккал")
            print(f"  - Белки: {nutrition_analysis.protein_g} г")
            print(f"  - Жиры: {nutrition_analysis.fats_g} г")
            print(f"  - Углеводы: {nutrition_analysis.carbs_g} г")
            
            return {
                "nutrition_analysis": nutrition_analysis
            }
        except Exception as e:
            print(f"\n✗ Ошибка при анализе питания: {e}")
            return {
                "error": f"Ошибка анализа питания: {str(e)}"
            }
    
    def _analyze_preferences(self, state: Dict[str, Any]) -> Dict[str, Any]:
        """
        Узел для анализа пищевых предпочтений.
        
        Args:
            state: Текущее состояние графа
            
        Returns:
            Dict: Обновленное состояние
        """
        try:
            user_input = state["user_input"]
            
            # Анализируем предпочтения
            preferences_analysis = self.preferences_agent.analyze(user_input)
            
            print(f"\n✓ Анализ предпочтений завершен:")
            print(f"  - Разрешенных продуктов: {len(preferences_analysis.allowed_foods)}")
            print(f"  - Запрещенных продуктов: {len(preferences_analysis.restricted_foods)}")
            
            return {
                "preferences_analysis": preferences_analysis
            }
        except Exception as e:
            print(f"\n✗ Ошибка при анализе предпочтений: {e}")
            return {
                "error": f"Ошибка анализа предпочтений: {str(e)}"
            }
    
    def _create_plan(self, state: Dict[str, Any]) -> Dict[str, Any]:
        """
        Узел для создания финального плана питания.
        
        Args:
            state: Текущее состояние графа
            
        Returns:
            Dict: Обновленное состояние
        """
        try:
            user_input = state["user_input"]
            nutrition_analysis = state["nutrition_analysis"]
            preferences_analysis = state["preferences_analysis"]
            
            # Создаем план питания
            weekly_plan = self.final_agent.create_plan(
                user_input,
                nutrition_analysis,
                preferences_analysis
            )
            
            print(f"\n✓ Недельный план питания создан:")
            print(f"  - Дней в плане: {len(weekly_plan.week_plan)}")
            
            return {
                "final_plan": weekly_plan
            }
        except Exception as e:
            print(f"\n✗ Ошибка при создании плана: {e}")
            return {
                "error": f"Ошибка создания плана: {str(e)}"
            }
    
    def run(self, user_input: UserInput) -> Dict[str, Any]:
        """
        Запускает workflow.
        
        Args:
            user_input: Входные данные пользователя
            
        Returns:
            GraphState: Финальное состояние с планом питания
        """
        print("\n" + "="*60)
        print("🚀 Запуск агентной системы составления рациона")
        print("="*60)
        
        # Создаем начальное состояние
        initial_state = {
            "user_input": user_input,
            "nutrition_analysis": None,
            "preferences_analysis": None,
            "final_plan": None,
            "error": None
        }
        
        # Запускаем граф
        final_state = self.graph.invoke(initial_state)
        
        print("\n" + "="*60)
        print("✅ Работа системы завершена")
        print("="*60 + "\n")
        
        # Возвращаем состояние как есть (уже GraphState типа)
        return final_state

