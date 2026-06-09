# Task Decomposition Agent

**Break complex goals into executable tasks. Plan intelligently. Execute systematically. Get results.**

A two-agent AI system where one agent breaks down goals into structured tasks and another executes them sequentially with full context awareness.

## The Problem

Complex goals are hard. Most AI systems either:
- Try to do everything at once (messy, inefficient)
- Get confused about what to do first
- Waste API calls doing redundant work

## The Solution

**Task Decomposition** — Break goals into simple, executable steps.

User Goal → Planner Agent (breaks into tasks) → Executor Agent (runs each task sequentially) → Final Result

## How It Works

### Example: "Analyze market data"

**Step 1: Planner**
- Breaks goal into 3 tasks
- Task 1: Gather historical market data
- Task 2: Clean and preprocess data
- Task 3: Visualize and interpret results

**Step 2: Executor**
- Executes Task 1 → Gets market data
- Executes Task 2 → Cleans the data
- Executes Task 3 → Creates analysis using results from Task 1 & 2

**Result:** Complete market analysis with structured approach

## Features

 Intelligent Task Decomposition — Planner breaks goals into 2-4 clear tasks
 Sequential Execution — Tasks run one after another, building on previous results
 Context Passing — Each task sees previous task results
 Structured Output — Pydantic models for type safety
 Modern UI — Beautiful React interface with real-time updates
 Professional Design — Production-ready styling and UX
 Fast Execution — Typically completes in 1-3 seconds

## Tech Stack

**Frontend:** React 18 + Vite, Modern CSS with gradients and animations, Real-time message streaming

**Backend:** FastAPI (Python), LangGraph for agent orchestration, Groq LLM (Mixtral 8x7B), Tavily API for search

**Architecture:** REST API with CORS enabled, Pydantic for data validation, Agent-based design pattern

## Quick Start

### 1. Clone Repository

git clone https://github.com/tanoojbogireddy/task-decomposition-agent.git
cd task-decomposition-agent

### 2. Setup Environment

cp .env.example .env

Add your API keys to .env:
GROQ_API_KEY=your_groq_key
TAVILY_API_KEY=your_tavily_key

Get free keys:
- Groq: https://console.groq.com (Free tier available)
- Tavily: https://tavily.com (Free tier with generous limits)

### 3. Install Dependencies

Backend:
pip install -r requirements.txt

Frontend:
cd frontend
npm install
cd ..

### 4. Run Both Services

Terminal 1 - API:
python3 api.py

Runs on http://127.0.0.1:8000

Terminal 2 - Frontend:
cd frontend
npm run dev

Runs on http://localhost:5173

### 5. Open Browser

Go to: http://localhost:5173



### Planner Agent

Takes your goal and breaks it into structured tasks:

Goal: "Write a report on renewable energy"
Output: [{id: 1, description: "Search for market data", tools: ["search"]}, {id: 2, description: "Search for key players", tools: ["search"]}, {id: 3, description: "Write report", tools: ["write_file"]}]

### Executor Agent

Runs each task sequentially, passing context forward:

Task 1 → Search & get results
Task 2 → Search using context from Task 1
Task 3 → Write report using results from Task 1 & 2

### LangGraph Orchestration

Manages state and flow between agents:
- Planner node → Executor node → END
- State persists across steps
- Easy to extend with new nodes

## Key Concepts

**Task Decomposition**: Breaking a complex goal into simple, manageable steps.

**Sequential Execution**: Tasks run one after another, not in parallel.

**Context Passing**: Each task can see results from previous tasks.

**Structured Output**: Using Pydantic to ensure type-safe data between components.

**Agent Handoff**: Planner creates plan, Executor executes it independently.

## Example: Real World Usage

**Input:** "Create a business analysis for the AI market"

**What Happens:**
1. Planner breaks this into: Search for AI market size and growth trends, Identify key players and their market share, Compile findings into a structured report

2. Executor runs each: Task 1: Searches for market data, gets trends. Task 2: Searches for competitors using Task 1 context. Task 3: Writes comprehensive report using all results

3. Output: Professional business analysis (typically 2-3 seconds)

## API Endpoints

**Health Check:** GET /health

**Execute Goal:** POST /execute with Content-Type: application/json and body: {"goal": "Your goal here"}

**Response:** {"goal": "Your goal", "tasks": [{"id": 1, "description": "...", "tools": ["search"]}], "final_answer": "Result text here", "time_taken": 2.15}

## Performance

- Average execution time: 1-3 seconds
- Max tokens per request: 2000 (configurable)
- Concurrent requests: Limited by API rate limits
- Groq API: Very fast, free tier available


## Troubleshooting

**API not starting?** python3 -c "from fastapi import FastAPI; print('OK')"

**Import errors?** pip install -r requirements.txt

**Frontend not connecting?** Check API is running on 127.0.0.1:8000, Check CORS is enabled in api.py, Check .env has correct API keys

**Tasks not executing?** Verify Groq API key is valid, Check terminal for error messages, Try simpler goal first

## Next Steps

This is Project of a 5-project learning roadmap:

- ReAct Research Agent — Single agent with reasoning loop
- Planner-Executor Pipeline — Two agents, sequential execution
- Critic-Refiner Loop — Agents teaching each other
- Supervisor + Worker Swarm — Parallel execution
- Adaptive Meta-Orchestrator — System picks best pattern

## Learning Outcomes

By studying this code, you learn:  LangGraph agent orchestration, Multi-agent systems, Task decomposition patterns, Structured data handling with Pydantic, FastAPI + React integration, Real-time UI with async operations, Agent state management

## Contributing

Found an issue? Want to improve something? 1. Fork the repo 2. Create a feature branch 3. Submit a PR

## License

MIT — Free to use, modify, and distribute.

## Resources

- LangGraph Docs: https://langchain-ai.github.io/langgraph/
- FastAPI Docs: https://fastapi.tiangolo.com/
- React Docs: https://react.dev/
- Groq Docs: https://console.groq.com/docs

---
