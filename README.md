# Panaceya AI - Agentic Surgical Training Core

This project implements the backend for **Panaceya AI**, a multi-agent surgical training platform. It uses **LangGraph** for orchestration and **Groq (Llama-3.3-70b)** for high-speed agentic reasoning.

## Agentic Architecture
The system is composed of specialized agents working in parallel and sequence:
1.  **Safety Monitor (Groq + Tool Use):** Validates actions against physics constraints using a mock SOFA engine tool.
2.  **Technique Analyzer:** Evaluates surgical technique (simulated vision system).
3.  **Scribe:** Maintains a persistent log of the entire procedure.
4.  **Learning Coach:** Synthesizes feedback, prioritizing safety alerts over technique advice.

## Master Test Suite (`backend/test_master.py`)
We have verified the system's logic using a comprehensive 3-step simulation.

### Tested Scenarios & Performance

| Scenario | Input Description | Expected Behavior | Result |
| :--- | :--- | :--- | :--- |
| **1. Happy Path** | Standard incision, safe force (30N). | **Praise:** "Perfect execution." | ✅ PASS |
| **2. Technique Error** | "Incision with tremor", safe force. | **Coaching Warning:** "High jitter detected. Stabilize your wrist." | ✅ PASS |
| **3. Safety Violation** | Deep cut, excessive force (93N vs 80N limit). | **Safety Override:** "STOP! Critical safety violation." | ✅ PASS |

### Features Verified
- **Tool Use:** The Safety Agent correctly called `check_physics_constraints` to detect the 93N force.
- **Dynamic Response:** The Technique Agent correctly identified "tremor" keywords and adjusted advice.
- **Priority Handling:** The Coach correctly prioritized the Safety "STOP" message over technique advice in Step 3.
- **Memory Persistence:** The Scribe successfully retained a history of all 3 steps (no amnesia).

## How to Run Tests
1.  Ensure you have the `backend` dependencies installed (`pip install -r backend/requirements.txt`).
2.  Set your `GROQ_API_KEY` in the `.env` file.
3.  Run the test suite:
    ```bash
    python backend/test_master.py
    ```

## Project Files & Locations
The following files are core to the **Groq-powered Agentic System**:

### Key Agents & Logic
- **`backend/test_groq.py`**:  
  Sample script to verify the Safety Agent and Groq LLM integration.
- **`backend/app/agents/safety_monitor.py`**:  
  Contains the `safety_monitor_agent` and the `check_physics_constraints` tool.
- **`backend/app/agents/orchestrator.py`**:  
  Defines the LangGraph workflow, nodes, and edge logic.
- **`backend/app/models/state.py`**:  
  Defines the `SurgicalState` (TypedDict) passed between agents.

### Configuration
- **`backend/requirements.txt`**:  
  Python dependencies (includes `langchain-groq`, `langgraph`, etc.).
- **`.env`**:  
  Stores secrets (must contain `GROQ_API_KEY`).
