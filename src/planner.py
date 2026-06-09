from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage
from dotenv import load_dotenv
import os
import json
from src.schemas import TaskList, Task

load_dotenv()

llm = ChatGroq(model="llama-3.3-70b-versatile", temperature=0, api_key=os.getenv("GROQ_API_KEY"))

def plan(goal: str) -> TaskList:
    """Break down a goal into tasks."""
    prompt = f"""Break this goal into 2-3 simple tasks.
Return ONLY valid JSON with no markdown, no code blocks, just raw JSON:
{{
  "goal": "{goal}",
  "tasks": [
    {{"task_id": 1, "description": "Task 1", "tools": ["search"], "expected_output": "Results"}}
  ],
  "total_tasks": 1
}}

Goal: {goal}"""

    try:
        message = HumanMessage(content=prompt)
        response = llm.invoke([message])

        json_str = response.content.strip()
        if json_str.startswith("```"):
            json_str = json_str.split("```")[1]
            if json_str.startswith("json"):
                json_str = json_str[4:]

        task_data = json.loads(json_str)
        tasks = [Task(**task) for task in task_data.get("tasks", [])]
        return TaskList(
            goal=task_data.get("goal", goal),
            tasks=tasks,
            total_tasks=len(tasks)
        )
    except Exception:
        return TaskList(
            goal=goal,
            tasks=[Task(task_id=1, description=goal, tools=["search"], expected_output="Results")],
            total_tasks=1
        )