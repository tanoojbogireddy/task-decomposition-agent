from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage
from dotenv import load_dotenv
import os
from src.schemas import Task, TaskResult, ExecutionReport

load_dotenv()

llm = ChatGroq(model="llama-3.3-70b-versatile", temperature=0, api_key=os.getenv("GROQ_API_KEY"))

def execute_task(task: Task, context: str = "") -> TaskResult:
    """Execute a single task."""
    try:
        prompt = f"""Execute this task and provide a clear result:

Task: {task.description}
Expected output: {task.expected_output}

Provide a concise answer (2-3 sentences max)."""
        
        message = HumanMessage(content=prompt)
        response = llm.invoke([message])
        
        return TaskResult(
            task_id=task.task_id,
            task_description=task.description,
            status="success",
            result=response.content
        )
    
    except Exception as e:
        return TaskResult(
            task_id=task.task_id,
            task_description=task.description,
            status="failed",
            result="",
            error=str(e)
        )

def execute_tasks(tasks: list, goal: str) -> ExecutionReport:
    """Execute all tasks sequentially."""
    results = []
    completed = 0
    failed = 0
    
    for task in tasks:
        result = execute_task(task)
        results.append(result)
        
        if result.status == "success":
            completed += 1
        else:
            failed += 1
    
    return ExecutionReport(
        goal=goal,
        total_tasks=len(tasks),
        completed_tasks=completed,
        failed_tasks=failed,
        results=results,
        final_synthesis=f"Completed {completed}/{len(tasks)} tasks successfully"
    )