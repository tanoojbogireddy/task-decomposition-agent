from langgraph.graph import StateGraph, START, END
from langchain_core.messages import HumanMessage
from typing import TypedDict, Annotated
import operator
from src.planner import plan
from src.executor import execute_tasks
from src.schemas import TaskList

class PlannerExecutorState(TypedDict):
    user_goal: str
    task_list: TaskList
    execution_results: dict
    final_answer: str

def planner_node(state: PlannerExecutorState):
    """Planner breaks down goal into tasks."""
    goal = state["user_goal"]
    task_list = plan(goal)
    return {
        "task_list": task_list,
        "user_goal": goal
    }

def executor_node(state: PlannerExecutorState):
    """Executor runs all tasks."""
    task_list = state["task_list"]
    goal = state["user_goal"]
    
    report = execute_tasks(task_list.tasks, goal)
    
    final_answer = f"Based on your goal: {goal}\n\n"
    final_answer += f"Executed {report.completed_tasks}/{report.total_tasks} tasks\n\n"
    for result in report.results:
        if result.status == "success":
            final_answer += f"• {result.result[:500]}\n"
        else:
            final_answer += f"• Task failed: {result.error}\n"
    
    return {
        "execution_results": report.dict(),
        "final_answer": final_answer
    }

def build_graph():
    """Build the Planner-Executor graph."""
    graph = StateGraph(PlannerExecutorState)
    
    graph.add_node("planner", planner_node)
    graph.add_node("executor", executor_node)
    
    graph.add_edge(START, "planner")
    graph.add_edge("planner", "executor")
    graph.add_edge("executor", END)
    
    return graph.compile()