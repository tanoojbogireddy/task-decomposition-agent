from pydantic import BaseModel, Field
from typing import List

class Task(BaseModel):
    """A single task to execute."""
    task_id: int
    description: str
    tools: List[str] = Field(default_factory=list)
    expected_output: str = ""

class TaskList(BaseModel):
    """A list of tasks from the planner."""
    goal: str
    tasks: List[Task]
    total_tasks: int

class TaskResult(BaseModel):
    """Result of executing a task."""
    task_id: int
    task_description: str
    status: str
    result: str
    error: str = ""

class ExecutionReport(BaseModel):
    """Final execution report."""
    goal: str
    total_tasks: int
    completed_tasks: int
    failed_tasks: int
    results: List[TaskResult]
    final_synthesis: str = ""