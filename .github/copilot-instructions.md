## Project Overview
You are helping build **Panaceya AI** - a gamified surgical training platform with a **Python backend** handling AI multi-agent orchestration and a **React frontend** for 3D visualization and user interaction.

## Startup Instructions - Always run these commands to set up the environment:
- **Runtime Environment**: panacea
- **Activate Environment**: `conda activate panacea` or `C:\Users\"Darth Vader"\anaconda3\envs\panacea\python.exe`

## Architecture Overview

### Backend: Python + FastAPI + LangGraph
- **API Framework**: FastAPI (async, high-performance REST API)
- **Multi-Agent Orchestration**: LangGraph for state-based agent workflows
- **AI Integration**: LangChain + Azure OpenAI SDK
- **Task Queue**: Celery (for long-running agent tasks)
- **Database**: Azure Cosmos DB (via Python SDK)
- **Caching**: Redis (for agent responses)

### Frontend: React + Three.js
- **3D Rendering**: Three.js with React Three Fiber
- **UI Framework**: React 18+ with TypeScript
- **Styling**: Tailwind CSS
- **State Management**: Zustand
- **API Client**: Axios with React Query

---

## Tech Stack (Backend)

### Core Dependencies
```python
# API Framework
fastapi
uvicorn[standard]
python-multipart

# Multi-Agent Orchestration
langgraph
langchain
langchain-openai

# Azure AI Services
azure-ai-openai
azure-cognitiveservices-vision-computervision
azure-cognitiveservices-speech
azure-cosmos

# Data Processing
pydantic
pydantic-settings

# Async & Background Tasks
celery
redis

# Utils
python-dotenv
httpx
```

---

## Project Structure

```
backend/
├── app/
│   ├── __init__.py
│   ├── main.py                    # FastAPI app entry point
│   ├── config.py                  # Configuration management
│   ├── agents/
│   │   ├── __init__.py
│   │   ├── orchestrator.py        # Main orchestrator using LangGraph
│   │   ├── technique_analyzer.py  # Technique analysis agent
│   │   ├── safety_monitor.py      # Safety monitoring agent
│   │   ├── learning_coach.py      # Adaptive learning agent
│   │   ├── knowledge_tutor.py     # Q&A and context agent
│   │   └── base.py                # Base agent class
│   ├── services/
│   │   ├── __init__.py
│   │   ├── azure_openai.py        # Azure OpenAI client
│   │   ├── azure_vision.py        # Computer Vision client
│   │   ├── azure_speech.py        # Speech Services client
│   │   └── cosmos_db.py           # Database operations
│   ├── models/
│   │   ├── __init__.py
│   │   ├── surgical_action.py     # Surgical action data models
│   │   ├── agent_response.py      # Agent response models
│   │   ├── user.py                # User and progress models
│   │   └── procedure.py           # Surgical procedure models
│   ├── api/
│   │   ├── __init__.py
│   │   ├── routes/
│   │   │   ├── surgical.py        # Surgical simulation endpoints
│   │   │   ├── agents.py          # Agent interaction endpoints
│   │   │   ├── users.py           # User management endpoints
│   │   │   └── analytics.py       # Performance analytics endpoints
│   │   └── websocket.py           # WebSocket for real-time feedback
│   ├── utils/
│   │   ├── __init__.py
│   │   ├── logging.py             # Structured logging
│   │   ├── error_handlers.py      # Custom error handlers
│   │   └── validators.py          # Input validation
│   └── tasks/
│       ├── __init__.py
│       └── agent_tasks.py         # Celery background tasks
├── tests/
│   ├── __init__.py
│   ├── test_agents/
│   ├── test_api/
│   └── conftest.py
├── alembic/                       # Database migrations
├── requirements.txt
├── requirements-dev.txt
├── .env.example
├── Dockerfile
└── README.md

frontend/
├── src/
│   ├── components/
│   │   ├── 3d/
│   │   │   ├── AnatomyViewer.tsx
│   │   │   ├── SurgicalTools.tsx
│   │   │   └── PhysicsEngine.tsx
│   │   ├── ui/
│   │   │   ├── ToolPalette.tsx
│   │   │   ├── FeedbackPanel.tsx
│   │   │   └── ScoreDisplay.tsx
│   │   └── game/
│   │       ├── ProcedureSelector.tsx
│   │       └── Leaderboard.tsx
│   ├── services/
│   │   └── api.ts                 # Backend API client
│   ├── hooks/
│   │   ├── useSurgicalSimulation.ts
│   │   ├── useAgentFeedback.ts
│   │   └── useWebSocket.ts
│   ├── store/
│   │   ├── simulationStore.ts
│   │   └── userStore.ts
│   └── types/
│       ├── surgical.types.ts
│       └── api.types.ts
├── public/
│   └── models/                    # 3D GLTF models
├── package.json
└── vite.config.ts
```

---

## Python Coding Standards

### General Principles
- Follow PEP 8 style guide
- Use type hints for all function signatures
- Write docstrings for all public functions (Google style)
- Use async/await for I/O operations
- Prefer Pydantic models over raw dictionaries
- Use dataclasses for simple data structures

### Example Code Style
```python
from typing import List, Optional
from pydantic import BaseModel, Field

class SurgicalAction(BaseModel):
    """Represents a single surgical action taken by the user.
    
    Attributes:
        action_type: Type of surgical action (cut, suture, clamp, etc.)
        tool_used: The surgical tool used
        target_location: 3D coordinates of the action
        timestamp: When the action occurred
        force_applied: Force magnitude (0-100)
    """
    action_type: str = Field(..., description="Type of surgical action")
    tool_used: str = Field(..., description="Surgical tool identifier")
    target_location: tuple[float, float, float]
    timestamp: float
    force_applied: float = Field(ge=0, le=100)
    
    class Config:
        json_schema_extra = {
            "example": {
                "action_type": "incision",
                "tool_used": "scalpel_15",
                "target_location": [0.5, 1.2, 0.3],
                "timestamp": 1234567890.123,
                "force_applied": 45.5
            }
        }
```

---

## LangGraph Multi-Agent Pattern

### State Definition
```python
from typing import TypedDict, Annotated, Sequence
from langchain_core.messages import BaseMessage
import operator

class AgentState(TypedDict):
    """Shared state between all agents."""
    messages: Annotated[Sequence[BaseMessage], operator.add]
    surgical_action: dict
    technique_feedback: Optional[dict]
    safety_alerts: List[dict]
    learning_suggestions: Optional[dict]
    knowledge_response: Optional[str]
    next_agent: str  # Which agent should run next
```

### Orchestrator with LangGraph
```python
from langgraph.graph import StateGraph, END
from langchain_openai import AzureChatOpenAI

class SurgicalAgentOrchestrator:
    """Orchestrates multiple specialized agents using LangGraph."""
    
    def __init__(self):
        self.llm = AzureChatOpenAI(
            deployment_name="gpt-4o",
            temperature=0.3
        )
        self.graph = self._build_graph()
    
    def _build_graph(self) -> StateGraph:
        """Build the agent workflow graph."""
        workflow = StateGraph(AgentState)
        
        # Add agent nodes
        workflow.add_node("router", self._route_to_agents)
        workflow.add_node("technique_analyzer", self._analyze_technique)
        workflow.add_node("safety_monitor", self._monitor_safety)
        workflow.add_node("learning_coach", self._provide_coaching)
        workflow.add_node("knowledge_tutor", self._answer_questions)
        workflow.add_node("aggregator", self._aggregate_responses)
        
        # Define edges
        workflow.set_entry_point("router")
        
        # Conditional routing based on action type
        workflow.add_conditional_edges(
            "router",
            self._determine_agents_needed,
            {
                "technique": "technique_analyzer",
                "safety": "safety_monitor",
                "learning": "learning_coach",
                "question": "knowledge_tutor",
                "all": "technique_analyzer"  # Default: run all
            }
        )
        
        # Connect agents to aggregator
        workflow.add_edge("technique_analyzer", "aggregator")
        workflow.add_edge("safety_monitor", "aggregator")
        workflow.add_edge("learning_coach", "aggregator")
        workflow.add_edge("knowledge_tutor", "aggregator")
        workflow.add_edge("aggregator", END)
        
        return workflow.compile()
    
    def _determine_agents_needed(self, state: AgentState) -> str:
        """Decide which agents should process this action."""
        action = state["surgical_action"]
        
        # Critical safety check always runs
        if action.get("involves_vital_structure"):
            return "safety"
        
        # User asking a question
        if action.get("type") == "question":
            return "question"
        
        # Regular surgical action - run all agents
        return "all"
    
    async def process_action(
        self, 
        surgical_action: dict
    ) -> dict:
        """Process a surgical action through the agent graph."""
        initial_state = {
            "messages": [],
            "surgical_action": surgical_action,
            "technique_feedback": None,
            "safety_alerts": [],
            "learning_suggestions": None,
            "knowledge_response": None,
            "next_agent": "router"
        }
        
        # Execute the graph
        final_state = await self.graph.ainvoke(initial_state)
        
        return {
            "technique": final_state.get("technique_feedback"),
            "safety": final_state.get("safety_alerts"),
            "coaching": final_state.get("learning_suggestions"),
            "knowledge": final_state.get("knowledge_response")
        }
```

### Individual Agent Implementation
```python
from langchain.agents import AgentExecutor, create_openai_functions_agent
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.tools import tool

class TechniqueAnalyzer:
    """Agent specialized in analyzing surgical technique."""
    
    def __init__(self, llm: AzureChatOpenAI):
        self.llm = llm
        self.agent = self._create_agent()
    
    def _create_agent(self) -> AgentExecutor:
        """Create the technique analysis agent."""
        
        # Define tools this agent can use
        @tool
        def check_angle(tool_angle: float, target_angle: float) -> str:
            """Check if surgical tool angle is correct."""
            diff = abs(tool_angle - target_angle)
            if diff < 5:
                return "Perfect angle"
            elif diff < 15:
                return f"Adjust angle by {diff:.1f} degrees"
            else:
                return f"Incorrect angle - {diff:.1f}° off target"
        
        @tool
        def check_pressure(force: float, tissue_type: str) -> str:
            """Evaluate if applied pressure is appropriate."""
            thresholds = {
                "skin": 30,
                "muscle": 50,
                "organ": 20
            }
            max_force = thresholds.get(tissue_type, 40)
            
            if force > max_force:
                return f"Too much force! Reduce by {force - max_force:.1f}"
            elif force < max_force * 0.5:
                return "Insufficient force - increase pressure"
            else:
                return "Appropriate pressure"
        
        tools = [check_angle, check_pressure]
        
        prompt = ChatPromptTemplate.from_messages([
            ("system", """You are an expert surgical technique analyzer.
            Analyze the user's surgical action and provide specific, 
            actionable feedback on their technique.
            
            Focus on:
            - Tool angle and approach
            - Applied force/pressure
            - Movement precision
            - Anatomical accuracy
            
            Be encouraging but precise. If technique is good, say so.
            If improvement needed, explain exactly how to fix it."""),
            MessagesPlaceholder(variable_name="chat_history"),
            ("human", "{input}"),
            MessagesPlaceholder(variable_name="agent_scratchpad")
        ])
        
        agent = create_openai_functions_agent(self.llm, tools, prompt)
        return AgentExecutor(agent=agent, tools=tools, verbose=True)
    
    async def analyze(self, surgical_action: dict) -> dict:
        """Analyze a surgical action and return feedback."""
        input_text = f"""
        Analyze this surgical action:
        - Action: {surgical_action['action_type']}
        - Tool: {surgical_action['tool_used']}
        - Target: {surgical_action['target_location']}
        - Force: {surgical_action['force_applied']}
        - Angle: {surgical_action.get('angle', 'N/A')}
        """
        
        result = await self.agent.ainvoke({
            "input": input_text,
            "chat_history": []
        })
        
        return {
            "feedback": result["output"],
            "score": self._calculate_technique_score(surgical_action),
            "suggestions": self._extract_suggestions(result["output"])
        }
    
    def _calculate_technique_score(self, action: dict) -> float:
        """Calculate technique quality score (0-100)."""
        # Implement scoring logic based on action parameters
        score = 100.0
        
        # Deduct points for issues
        if action.get('force_applied', 0) > 80:
            score -= 20
        if action.get('angle_deviation', 0) > 15:
            score -= 15
        
        return max(0, score)
    
    def _extract_suggestions(self, feedback: str) -> List[str]:
        """Extract actionable suggestions from feedback text."""
        # Use LLM to extract structured suggestions
        # Return as list of specific actions
        return []
```

---

## FastAPI Integration

### Main Application
```python
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Startup and shutdown events."""
    # Startup
    print("Initializing agents...")
    app.state.orchestrator = SurgicalAgentOrchestrator()
    yield
    # Shutdown
    print("Shutting down...")

app = FastAPI(
    title="SurgiSim AI API",
    description="Multi-agent surgical training platform",
    version="1.0.0",
    lifespan=lifespan
)

# CORS for React frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # Vite dev server
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
from app.api.routes import surgical, users, analytics
app.include_router(surgical.router, prefix="/api/surgical", tags=["surgical"])
app.include_router(users.router, prefix="/api/users", tags=["users"])
app.include_router(analytics.router, prefix="/api/analytics", tags=["analytics"])
```

### API Endpoints
```python
from fastapi import APIRouter, HTTPException, BackgroundTasks
from app.models.surgical_action import SurgicalAction, AgentFeedback
from app.agents.orchestrator import SurgicalAgentOrchestrator

router = APIRouter()

@router.post("/analyze-action", response_model=AgentFeedback)
async def analyze_surgical_action(
    action: SurgicalAction,
    background_tasks: BackgroundTasks,
    orchestrator: SurgicalAgentOrchestrator = Depends(get_orchestrator)
):
    """Analyze a surgical action and get AI feedback from multiple agents."""
    try:
        # Process through multi-agent system
        feedback = await orchestrator.process_action(action.dict())
        
        # Log to database in background
        background_tasks.add_task(log_action, action, feedback)
        
        return AgentFeedback(**feedback)
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.websocket("/ws/real-time-feedback")
async def websocket_endpoint(websocket: WebSocket):
    """WebSocket for real-time agent feedback during procedures."""
    await websocket.accept()
    orchestrator = SurgicalAgentOrchestrator()
    
    try:
        while True:
            # Receive surgical action from frontend
            data = await websocket.receive_json()
            
            # Process through agents
            feedback = await orchestrator.process_action(data)
            
            # Send feedback back
            await websocket.send_json(feedback)
    
    except WebSocketDisconnect:
        print("Client disconnected")
```

---

## Azure Service Integration

### Azure OpenAI Service
```python
from azure.identity import DefaultAzureCredential
from openai import AzureOpenAI
from app.config import settings

class AzureOpenAIService:
    """Wrapper for Azure OpenAI API."""
    
    def __init__(self):
        self.client = AzureOpenAI(
            api_key=settings.AZURE_OPENAI_KEY,
            api_version="2024-02-15-preview",
            azure_endpoint=settings.AZURE_OPENAI_ENDPOINT
        )
    
    async def get_completion(
        self,
        messages: List[dict],
        temperature: float = 0.7,
        max_tokens: int = 500
    ) -> str:
        """Get completion from Azure OpenAI."""
        try:
            response = self.client.chat.completions.create(
                model=settings.AZURE_OPENAI_DEPLOYMENT,
                messages=messages,
                temperature=temperature,
                max_tokens=max_tokens
            )
            return response.choices[0].message.content
        
        except Exception as e:
            print(f"Azure OpenAI error: {e}")
            raise
```

---

## Testing Strategy

### Unit Tests
```python
import pytest
from app.agents.technique_analyzer import TechniqueAnalyzer

@pytest.mark.asyncio
async def test_technique_analyzer():
    """Test technique analyzer agent."""
    analyzer = TechniqueAnalyzer(mock_llm)
    
    action = {
        "action_type": "incision",
        "tool_used": "scalpel",
        "force_applied": 45.0,
        "angle": 30
    }
    
    result = await analyzer.analyze(action)
    
    assert "feedback" in result
    assert 0 <= result["score"] <= 100
    assert isinstance(result["suggestions"], list)
```

### Integration Tests
```python
@pytest.mark.asyncio
async def test_orchestrator_workflow():
    """Test full multi-agent workflow."""
    orchestrator = SurgicalAgentOrchestrator()
    
    action = create_test_surgical_action()
    feedback = await orchestrator.process_action(action)
    
    assert "technique" in feedback
    assert "safety" in feedback
    assert len(feedback["safety"]) >= 0  # May or may not have alerts
```

---

## Performance Optimization

### Caching Agent Responses
```python
from functools import lru_cache
import hashlib
import json

class CachedOrchestrator:
    """Orchestrator with response caching."""
    
    def __init__(self):
        self.redis_client = redis.Redis(...)
    
    def _get_cache_key(self, action: dict) -> str:
        """Generate cache key from action."""
        action_str = json.dumps(action, sort_keys=True)
        return f"agent_response:{hashlib.md5(action_str.encode()).hexdigest()}"
    
    async def process_action(self, action: dict) -> dict:
        """Process with caching."""
        cache_key = self._get_cache_key(action)
        
        # Check cache
        cached = self.redis_client.get(cache_key)
        if cached:
            return json.loads(cached)
        
        # Process through agents
        result = await super().process_action(action)
        
        # Cache for 5 minutes
        self.redis_client.setex(cache_key, 300, json.dumps(result))
        
        return result
```

---

## Environment Configuration

### .env.example
```env
# Azure OpenAI
AZURE_OPENAI_ENDPOINT=https://your-resource.openai.azure.com/
AZURE_OPENAI_KEY=your-key-here
AZURE_OPENAI_DEPLOYMENT=gpt-4o

# Azure Computer Vision
AZURE_VISION_ENDPOINT=https://your-resource.cognitiveservices.azure.com/
AZURE_VISION_KEY=your-key-here

# Azure Cosmos DB
COSMOS_DB_ENDPOINT=https://your-account.documents.azure.com:443/
COSMOS_DB_KEY=your-key-here
COSMOS_DB_DATABASE=surgisim

# Redis Cache
REDIS_URL=redis://localhost:6379/0

# API Settings
API_HOST=0.0.0.0
API_PORT=8000
DEBUG=True
LOG_LEVEL=INFO

# CORS
FRONTEND_URL=http://localhost:5173
```

---

## Deployment

### Docker Setup
```dockerfile
FROM python:3.11-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application
COPY ./app ./app

# Run with uvicorn
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

---

## Common Patterns to Follow

### Always Use Type Hints
```python
async def process_feedback(
    action: SurgicalAction,
    user_id: str,
    session_id: Optional[str] = None
) -> AgentFeedback:
    """Process and return feedback with proper typing."""
    pass
```

### Error Handling
```python
from app.utils.error_handlers import handle_azure_error

try:
    result = await azure_service.call()
except AzureError as e:
    return handle_azure_error(e, fallback_response)
```

### Async Operations
```python
# Always use async for I/O operations
async def get_user_progress(user_id: str) -> dict:
    async with httpx.AsyncClient() as client:
        response = await client.get(f"/users/{user_id}/progress")
        return response.json()
```

---

## When Suggesting Code

1. **Use LangGraph for agent orchestration** - not manual routing
2. **Type hints are mandatory** - all functions must have them
3. **Pydantic for data validation** - never use raw dicts for API
4. **Async/await by default** - for all I/O operations
5. **FastAPI dependency injection** - for services and config
6. **Structured logging** - use Python's logging module properly
7. **Error handling** - always wrap Azure calls with try/except
8. **Testing** - suggest tests alongside implementation code

---

## Project Goals Reminder

This platform aims to:
1. **Democratize surgical training** - accessible globally
2. **Provide AI-powered multi-agent coaching** - real-time feedback
3. **Gamify learning** - engage through game mechanics
4. **Win Microsoft Imagine Cup 2026** - showcase Azure AI + Python AI frameworks

Always prioritize these goals when suggesting implementations.