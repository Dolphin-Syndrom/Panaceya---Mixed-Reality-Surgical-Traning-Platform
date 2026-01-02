## Project Overview
You are helping build **Panaceya AI** - a gamified surgical training platform with a **hybrid architecture**:
- **Frontend**: React + Three.js for web-based 3D visualization and UI
- **Backend**: Python FastAPI with LangGraph for AI multi-agent orchestration
- **Physics Server**: SOFA framework computing realistic surgical physics on backend
- **Communication**: REST API + WebSocket for real-time physics streaming

## Startup Instructions - Always run these commands to set up the environment:
- **Runtime Environment**: panacea
- **Activate Environment**: `conda activate panacea` or `C:\Users\"Darth Vader"\anaconda3\envs\panacea\python.exe`

## Architecture Overview

```
┌─────────────────────────────────────────────────────────────┐
│                       Web Browser (Client)                       │
│  ┌───────────────────────────────────────────────────────┐  │
│  │  React + Three.js Frontend                            │  │
│  │  • 3D surgical visualization                          │  │
│  │  • Interactive UI controls                            │  │
│  │  • Real-time rendering                                │  │
│  └────────────┬──────────────────────────────────────────┘  │
└───────────────┼───────────────────────────────────────────────┘
                │
                │ WebSocket (physics updates)
                │ REST API (actions, feedback)
                │
                ▼
┌─────────────────────────────────────────────────────────────┐
│                   Python Backend Server                          │
│  ┌──────────────────┐         ┌──────────────────────────┐   │
│  │  FastAPI         │◄────────┤  SOFA Physics Engine     │   │
│  │  • LangGraph AI  │         │  • Headless simulation   │   │
│  │  • Agent Router  │         │  • FEM computation       │   │
│  │  • WebSocket Hub │         │  • Collision detection   │   │
│  └────────┬─────────┘         └──────────────────────────┘   │
│           │                                                    │
│           ▼                                                    │
│  ┌──────────────────────────────────────────────────────┐     │
│  │  Azure AI Services                                   │     │
│  │  • OpenAI (GPT-4o) • Computer Vision • Speech       │     │
│  └──────────────────────────────────────────────────────┘     │
└─────────────────────────────────────────────────────────────┘
```

### Frontend: React + Three.js (Web)
- **Framework**: React 18+ with TypeScript
- **3D Rendering**: Three.js with React Three Fiber
- **Physics Visualization**: Render mesh updates from SOFA physics server
- **UI Components**: Tailwind CSS + Shadcn UI
- **State Management**: Zustand (lightweight state)
- **Real-time Communication**: WebSocket client for physics updates
- **API Client**: Axios with React Query for caching
- **Build Tool**: Vite (fast development)

### Backend: Python + FastAPI + LangGraph
- **API Framework**: FastAPI (async, high-performance REST API)
- **Multi-Agent Orchestration**: LangGraph for state-based agent workflows
- **AI Integration**: LangChain + Azure OpenAI SDK
- **Physics Engine**: SOFA (headless, server-side computation)
- **WebSocket Server**: FastAPI WebSocket for real-time physics streaming
- **Task Queue**: Celery (for long-running agent tasks)
- **Database**: Azure Cosmos DB (via Python SDK)
- **Caching**: Redis (for agent responses and physics state)

---

## Tech Stack

### Frontend Dependencies (package.json)
```json
{
  "dependencies": {
    "react": "^18.2.0",
    "react-dom": "^18.2.0",
    "@react-three/fiber": "^8.15.0",
    "@react-three/drei": "^9.88.0",
    "three": "^0.159.0",
    "zustand": "^4.4.0",
    "axios": "^1.6.0",
    "@tanstack/react-query": "^5.0.0",
    "tailwindcss": "^3.3.0",
    "@radix-ui/react-*": "latest",
    "socket.io-client": "^4.6.0"
  },
  "devDependencies": {
    "typescript": "^5.2.0",
    "vite": "^5.0.0",
    "@types/react": "^18.2.0",
    "@types/three": "^0.159.0"
  }
}
```

### Backend Dependencies (requirements.txt)
```python
# API Framework
fastapi
uvicorn[standard]
python-multipart
websockets

# Multi-Agent Orchestration
langgraph
langchain
langchain-openai

# Azure AI Services
azure-ai-openai
azure-cognitiveservices-vision-computervision
azure-cognitiveservices-speech
azure-cosmos

# SOFA Physics Engine (headless)
SOFA  # Install from: https://www.sofa-framework.org
SofaPython3

# Data Processing
pydantic
pydantic-settings
numpy
scipy

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
frontend/
├── src/
│   ├── main.tsx                   # Application entry point
│   ├── App.tsx                    # Main app component
│   ├── components/
│   │   ├── 3d/
│   │   │   ├── SurgicalScene.tsx  # Main Three.js scene
│   │   │   ├── DeformableOrgan.tsx # Organ mesh renderer
│   │   │   ├── SurgicalTool.tsx   # Tool renderer
│   │   │   ├── Lighting.tsx       # Scene lighting
│   │   │   └── Camera.tsx         # Camera controls
│   │   ├── ui/
│   │   │   ├── ToolPalette.tsx    # Tool selection UI
│   │   │   ├── FeedbackPanel.tsx  # AI feedback display
│   │   │   ├── ScoreDisplay.tsx   # Performance metrics
│   │   │   ├── ProcedureSelector.tsx
│   │   │   └── Leaderboard.tsx
│   │   └── game/
│   │       ├── Tutorial.tsx
│   │       └── LevelProgress.tsx
│   ├── hooks/
│   │   ├── usePhysicsStream.ts    # WebSocket physics updates
│   │   ├── useAgentFeedback.ts    # AI feedback hook
│   │   └── useSurgicalAction.ts   # Action tracking
│   ├── services/
│   │   ├── api.ts                 # REST API client
│   │   ├── websocket.ts           # WebSocket client
│   │   └── physics-interpolation.ts # Smooth physics rendering
│   ├── store/
│   │   ├── simulationStore.ts     # Simulation state
│   │   ├── userStore.ts           # User state
│   │   └── physicsStore.ts        # Physics state from server
│   └── types/
│       ├── surgical.types.ts
│       ├── physics.types.ts
│       └── api.types.ts
├── public/
├── package.json
├── vite.config.ts
├── tailwind.config.js
└── tsconfig.json

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
│   ├── physics/
│   │   ├── __init__.py
│   │   ├── sofa_engine.py         # SOFA physics engine (headless)
│   │   ├── scene_builder.py       # Build SOFA scenes
│   │   ├── physics_state.py       # Physics state management
│   │   └── mesh_updater.py        # Compute mesh deformations
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
│   │   ├── procedure.py           # Surgical procedure models
│   │   └── physics_state.py       # Physics state models
│   ├── api/
│   │   ├── __init__.py
│   │   ├── websocket.py           # WebSocket endpoints
│   │   ├── routes/
│   │   │   ├── __init__.py
│   │   │   ├── agents.py
│   │   │   ├── analytics.py
│   │   │   ├── surgical.py
│   │   │   ├── physics.py         # Physics simulation endpoints
│   │   │   └── users.py
│   ├── tasks/
│   │   ├── __init__.py
│   │   └── agent_tasks.py
│   └── utils/
│       ├── __init__.py
│       ├── error_handlers.py
│       ├── logging.py
│       └── validators.py
├── tests/
│   ├── __init__.py
│   ├── conftest.py
│   ├── test_agents/
│   │   └── __init__.py
│   ├── test_api/
│   │   └── __init__.py
│   └── test_physics/
│       └── __init__.py
├── requirements.txt
├── requirements-dev.txt
├── pytest.ini
├── Dockerfile
└── README.md
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
### CORS for SOFA frontend (running locally)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:*"],  # SOFA Python client
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
        result = await super()*  # SOFA client (any port)cess_action(action)
        
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
COSSOFA Framework Integration

### Architecture Overview
```
┌─────────────────────────────────────────────────────────────┐
│                    SOFA Frontend (Python)                    │
│  ┌────────────────┐  ┌──────────────┐  ┌─────────────────┐ │
│  │  PyQt6 GUI     │  │ SOFA Scene   │  │  API Client     │ │
│  │  (Controls)    │◄─┤  (Physics)   │◄─┤  (HTTP/WS)      │ │
│  └────────────────┘  └──────────────┘  └─────────────────┘ │
│           │                  │                    │          │
└───────────┼──────────────────┼────────────────────┼──────────┘
            │                  │                    │
            │                  │           ┌────────▼──────────┐
            │                  │           │  FastAPI Backend  │
            │                  │           │  ┌──────────────┐ │
            │                  │           │  │ LangGraph    │ │
            │                  └───────────┼─►│ Multi-Agent  │ │
            │                              │  │ Orchestrator │ │
            │                              │  └──────────────┘ │
            │                              └───────────────────┘
            │
    ┌───────▼────────┐
    │  User Input    │
    │ (Mouse/Haptic) │
    └────────────────┘
```

### Setting Up SOFA Scene
```python
import Sofa
import SofaRuntime
from typing import Optional
import numpy as np

class BaseSurgicalScene:
    """Base class for SOFA surgical simulation scenes."""
    
    def __init__(self, root_node: Sofa.Core.Node):
        self.root = root_node
        self.dt = 0.01  # 100 Hz simulation
        self.gravity = [0, -9.81, 0]
        
    def create_scene(self, root: Sofa.Core.Node):
        """Create the SOFA scene graph."""
        # Scene settings
        root.gravity = self.gravity
        root.dt = self.dt
        
        # Required plugins
        root.addObject('RequiredPlugin', name='SofaPython3')
        root.addObject('RequiredPlugin', name='SofaOpenglVisual')
        root.addObject('RequiredPlugin', name='SofaLoader')
        root.addObject('RequiredPlugin', name='SofaMeshCollision')
        root.addObject('RequiredPlugin', name='SofaDeformable')
        root.addObject('RequiredPlugin', name='SofaEngine')
        root.addObject('RequiredPlugin', name='SofaConstraint')
        
        # Visual style
        root.addObject('VisualStyle', displayFlags='showVisual showBehaviorModels')
        
        # Collision pipeline
        root.addObject('CollisionPipeline', depth=6, verbose=False)
        root.addObject('BruteForceBroadPhase')
        root.addObject('BVHNarrowPhase')
        root.addObject('CollisionResponse', response='PenalityContactForceField')
        root.addObject('LocalMinDistance', 
                       alarmDistance=0.5, 
                       contactDistance=0.2,
                       angleCone=0.01)
        
        # Time integration
        root.addObject('EulerImplicitSolver', 
                       rayleighStiffness=0.1, 
                       rayleighMass=0.1)
        root.addObject('CGLinearSolver', 
                       iterations=25, 
                       tolerance=1e-5, 
                       threshold=1e-5)
        
        return root

class LiverSurgeryScene(BaseSurgicalScene):
    """Liver surgery simulation with deformable FEM model."""
    
    def __init__(self, root_node: Sofa.Core.Node):
        super().__init__(root_node)
        self.liver_node: Optional[Sofa.Core.Node] = None
        self.tool_node: Optional[Sofa.Core.Node] = None
        
    def create_scene(self, root: Sofa.Core.Node):
        """Create liver surgery scene."""
        super().create_scene(root)
        
        # Create deformable liver
        self.liver_node = self._create_liver(root)
        
        # Create surgical tool (scalpel/probe)
        self.tool_node = self._create_tool(root)
        
        # Camera
        root.addObject('InteractiveCamera', 
                       name='camera',
                       position=[0, 50, 100],
                       lookAt=[0, 0, 0])
        
        # Lighting
        root.addObject('DirectionalLight', 
                       direction=[0, -1, -1],
                       color=[1, 1, 1])
        
        return root
    
    def _create_liver(self, root: Sofa.Core.Node) -> Sofa.Core.Node:
        """Create deformable liver model using FEM."""
        liver = root.addChild('Liver')
        
        # Load mesh
        liver.addObject('MeshVTKLoader', 
                        name='loader',
                        filename='assets/meshes/organs/liver.vtk')
        liver.addObject('TetrahedronSetTopologyContainer', 
                        src='@loader',
                        name='topo')
        liver.addObject('MechanicalObject', 
                        name='dofs',
                        template='Vec3d')
        
        # Mass
        liver.addObject('UniformMass', totalMass=1.5)  # 1.5 kg liver
        
        # FEM force field (Neo-Hookean material)
        liver.addObject('TetrahedronFEMForceField',
                        name='FEM',
                        youngModulus=3000,    # Pa (soft tissue)
                        poissonRatio=0.45,    # Nearly incompressible
                        method='large')
        
        # Constraints (fix some vertices to prevent drift)
        liver.addObject('BoxROI',
                        name='fixedROI',
                        box=[-10, 45, -10, 10, 55, 10],
                        drawBoxes=True)
        liver.addObject('FixedConstraint',
                        indices='@fixedROI.indices')
        
        # Visual model
        visual = liver.addChild('Visual')
        visual.addObject('OglModel',
                         name='visualModel',
                         src='@../loader',
                         color='0.8 0.2 0.2 1.0')
        visual.addObject('BarycentricMapping',
                         input='@../dofs',
                         output='@visualModel')
        
        # Collision model
        collision = liver.addChild('Collision')
        collision.addObject('TriangleSetTopologyContainer',
                            src='@../loader')
        collision.addObject('MechanicalObject',
                            name='collisionDofs')
        collision.addObject('TriangleCollisionModel')
        collision.addObject('LineCollisionModel')
        collision.addObject('PointCollisionModel')
        collision.addObject('BarycentricMapping',
                            input='@../dofs',
                            output='@collisionDofs')
        
        return liver
    
    def _create_tool(self, root: Sofa.Core.Node) -> Sofa.Core.Node:
        """Create surgical tool (scalpel/probe)."""
        tool = root.addChild('SurgicalTool')
        
        # Load tool mesh
        tool.addObject('MeshOBJLoader',
                       name='loader',
                       filename='assets/meshes/tools/scalpel.obj')
        tool.addObject('MechanicalObject',
                       name='dofs',
                       template='Rigid3d',
                       position=[0, 30, 50, 0, 0, 0, 1])  # x,y,z, qx,qy,qz,qw
        
        # Visual
        visual = tool.addChild('Visual')
        visual.addObject('OglModel',
                         name='visualModel',
                         src='@../loader',
                         color='0.8 0.8 0.8 1.0')
        visual.addObject('RigidMapping',
                         input='@../dofs',
                         output='@visualModel')
        
        # Collision (simplified sphere at tool tip)
        collision = tool.addChild('Collision')
        collision.addObject('MechanicalObject',
                            template='Vec3d',
                            position=[0, 0, -20])  # Tool tip position
        collision.addObject('SphereCollisionModel',
                            radius=1.0)
        collision.addObject('RigidMapping',
                            input='@../dofs',
                            output='@.')
        
        return tool
    
    def get_tool_position(self) -> np.ndarray:
        """Get current tool position."""
        if self.tool_node:
            dofs = self.tool_node.getObject('dofs')
            return np.array(dofs.position.value[0][:3])
        return np.zeros(3)
    
    def set_tool_position(self, position: np.ndarray):
        """Set tool position (for mouse/haptic control)."""
        if self.tool_node:
            dofs = self.tool_node.getObject('dofs')
            current = dofs.position.value[0]
            # Keep orientation, update position
            dofs.position.value = [[*position, *current[3:]]]
```

### Main Application with Qt GUI
```python
import sys
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, 
                              QVBoxLayout, QHBoxLayout, QPushButton, 
                              QLabel, QTextEdit)
from PyQt6.QtCore import QTimer, Qt
import Sofa
import Sofa.Gui
from services.api_client import SurgicalAPIClient
from scenes.laparoscopy_scene import LiverSurgeryScene

class SurgicalSimulatorApp(QMainWindow):
    """Main application window for surgical simulator."""
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Panaceya AI - Surgical Simulator")
        self.setGeometry(100, 100, 1600, 900)
        
        # API client for backend communication
        self.api_client = SurgicalAPIClient(base_url="http://localhost:8000")
        
        # SOFA simulation
        self.sofa_root = None
        self.scene = None
        self.simulation_running = False
        
        # Action tracking
        self.action_counter = 0
        self.last_tool_position = None
        
        self._setup_ui()
        self._init_sofa()
        
        # Timer for periodic feedback requests
        self.feedback_timer = QTimer()
        self.feedback_timer.timeout.connect(self._request_ai_feedback)
        self.feedback_timer.start(2000)  # Every 2 seconds
    
    def _setup_ui(self):
        """Setup Qt UI components."""
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QHBoxLayout(central_widget)
        
        # Left panel: SOFA visualization (will be embedded)
        sofa_container = QWidget()
        sofa_container.setMinimumSize(1000, 800)
        main_layout.addWidget(sofa_container, stretch=3)
        
        # Right panel: Controls and AI feedback
        right_panel = QWidget()
        right_layout = QVBoxLayout(right_panel)
        
        # Tool selection
        tool_label = QLabel("Surgical Tools")
        tool_label.setStyleSheet("font-size: 16px; font-weight: bold;")
        right_layout.addWidget(tool_label)
        
        btn_scalpel = QPushButton("🔪 Scalpel")
        btn_forceps = QPushButton("🔧 Forceps")
        btn_suture = QPushButton("🪡 Suture")
        
        right_layout.addWidget(btn_scalpel)
        right_layout.addWidget(btn_forceps)
        right_layout.addWidget(btn_suture)
        
        # AI Feedback panel
        feedback_label = QLabel("AI Coach Feedback")
        feedback_label.setStyleSheet("font-size: 16px; font-weight: bold; margin-top: 20px;")
        right_layout.addWidget(feedback_label)
        
        self.feedback_text = QTextEdit()
        self.feedback_text.setReadOnly(True)
        self.feedback_text.setMinimumHeight(300)
        right_layout.addWidget(self.feedback_text)
        
        # Score display
        self.score_label = QLabel("Technique Score: --")
        self.score_label.setStyleSheet("font-size: 18px; padding: 10px; background: #2c3e50; color: white; border-radius: 5px;")
        right_layout.addWidget(self.score_label)
        
        # Control buttons
        btn_start = QPushButton("▶ Start Simulation")
        btn_start.clicked.connect(self._start_simulation)
        btn_pause = QPushButton("⏸ Pause")
        btn_pause.clicked.connect(self._pause_simulation)
        btn_reset = QPushButton("🔄 Reset")
        btn_reset.clicked.connect(self._reset_simulation)
        
        right_layout.addWidget(btn_start)
        right_layout.addWidget(btn_pause)
        right_layout.addWidget(btn_reset)
        right_layout.addStretch()
        
        main_layout.addWidget(right_panel, stretch=1)
    
    def _init_sofa(self):
        """Initialize SOFA simulation."""
        # Create SOFA root node
        self.sofa_root = Sofa.Core.Node("root")
        
        # Create scene
        self.scene = LiverSurgeryScene(self.sofa_root)
        self.scene.create_scene(self.sofa_root)
        
        # Initialize SOFA GUI
        Sofa.Simulation.init(self.sofa_root)
        
        # Start SOFA GUI (this will open in separate window or embed)
        Sofa.Gui.GUIManager.Init("main", "qt")
        Sofa.Gui.GUIManager.createGUI(self.sofa_root)
        Sofa.Gui.GUIManager.MainLoop(self.sofa_root)
    
    def _start_simulation(self):
        """Start SOFA simulation."""
        self.simulation_running = True
        self.feedback_text.append("✅ Simulation started")
    
    def _pause_simulation(self):
        """Pause simulation."""
        self.simulation_running = False
        self.feedback_text.append("⏸ Simulation paused")
    
    def _reset_simulation(self):
        """Reset simulation."""
        Sofa.Simulation.reset(self.sofa_root)
        self.action_counter = 0
        self.feedback_text.clear()
        self.score_label.setText("Technique Score: --")
        self.feedback_text.append("🔄 Simulation reset")
    
    async def _request_ai_feedback(self):
        """Request AI feedback from backend."""
        if not self.simulation_running:
            return
        
        # Get current tool position
        tool_pos = self.scene.get_tool_position()
        
        # Check if tool moved (action occurred)
        if self.last_tool_position is not None:
            distance = np.linalg.norm(tool_pos - self.last_tool_position)
            
            if distance > 0.5:  # Threshold for action
                # Track action
                action = {
                    "action_type": "manipulation",
                    "tool_used": "scalpel",
                    "target_location": tool_pos.tolist(),
                    "timestamp": time.time(),
                    "force_applied": 45.0  # TODO: Get from force sensor
                }
                
                # Send to backend
                try:
                    feedback = await self.api_client.analyze_action(action)
                    
                    # Display feedback
                    self._display_feedback(feedback)
                    
                except Exception as e:
                    print(f"Error getting feedback: {e}")
        
        self.last_tool_position = tool_pos.copy()
    
    def _display_feedback(self, feedback: dict):
        """Display AI feedback in UI."""
        self.feedback_text.append("\n" + "="*40)
        
        if "technique" in feedback and feedback["technique"]:
            self.feedback_text.append(f"📊 Technique: {feedback['technique']['feedback']}")
            score = feedback['technique'].get('score', 0)
            self.score_label.setText(f"Technique Score: {score:.1f}/100")
        
        if "safety" in feedback and feedback["safety"]:
            for alert in feedback["safety"]:
                self.feedback_text.append(f"⚠️ Safety: {alert}")
        
        if "coaching" in feedback and feedback["coaching"]:
            self.feedback_text.append(f"💡 Tip: {feedback['coaching']}")

def main():
    """Entry point."""
    app = QApplication(sys.argv)
    window = SurgicalSimulatorApp()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
```

### API Client for Backend Communication
```python
import httpx
from typing import Dict, Optional
import asyncio

class SurgicalAPIClient:
    """Client for communicating with FastAPI backend."""
    
    def __init__(self, base_url: str = "http://localhost:8000"):
        self.base_url = base_url
        self.client = httpx.AsyncClient(base_url=base_url, timeout=30.0)
    
    async def analyze_action(self, action: Dict) -> Dict:
        """Send surgical action to backend for AI analysis."""
        try:
            response = await self.client.post(
                "/api/surgical/analyze-action",
                json=action
            )
            response.raise_for_status()
            return response.json()
        except httpx.HTTPError as e:
            print(f"HTTP error: {e}")
            return {}
    
    async def get_procedure_info(self, procedure_id: str) -> Dict:
        """Get procedure details."""
        response = await self.client.get(f"/api/surgical/procedures/{procedure_id}")
        return response.json()
    
    async def submit_score(self, user_id: str, score: float, metrics: Dict):
        """Submit performance score."""
        data = {
            "user_id": user_id,
            "score": score,
            "metrics": metrics
        }
        response = await self.client.post("/api/analytics/submit-score", json=data)
        return response.json()
    
    async def close(self):
        """Close the HTTP client."""
        await self.client.aclose()
```

### Installation Instructions
```bash
# Install SOFA (from source or pre-built binaries)
# Visit: https://www.sofa-framework.org/download/

# For Windows, download pre-built binaries and add to PATH

# Install Python dependencies
cd sofa_frontend
pip install PyQt6 httpx websockets numpy scipy python-dotenv

# Ensure SOFA Python bindings are available
python -c "import Sofa; print('SOFA installed successfully')"
```

---

## MOS_DB_ENDPOINT=https://your-account.documents.azure.com:443/
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