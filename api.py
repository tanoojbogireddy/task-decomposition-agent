from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from src.graph import build_graph
import time

app = FastAPI(title="Planner-Executor API", version="1.0")

# Enable CORS for React frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class GoalRequest(BaseModel):
    goal: str

class PlanResponse(BaseModel):
    goal: str
    tasks: list
    total_tasks: int

class ExecutionResponse(BaseModel):
    goal: str
    tasks: list
    execution_results: dict
    final_answer: str
    time_taken: float

@app.get("/health")
async def health():
    """Health check endpoint."""
    return {"status": "ok"}

@app.post("/execute")
async def execute_goal(request: GoalRequest):
    """Execute planner-executor pipeline."""
    try:
        start_time = time.time()
        
        graph = build_graph()
        initial_state = {
            "user_goal": request.goal,
            "task_list": None,
            "execution_results": {},
            "final_answer": ""
        }
        
        result = graph.invoke(initial_state)
        elapsed_time = time.time() - start_time
        
        # Format response
        tasks = []
        if result["task_list"]:
            for task in result["task_list"].tasks:
                tasks.append({
                    "id": task.task_id,
                    "description": task.description,
                    "tools": task.tools
                })
        
        return ExecutionResponse(
            goal=result["user_goal"],
            tasks=tasks,
            execution_results=result.get("execution_results", {}),
            final_answer=result.get("final_answer", ""),
            time_taken=elapsed_time
        )
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)