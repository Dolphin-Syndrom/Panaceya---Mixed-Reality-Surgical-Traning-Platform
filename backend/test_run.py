import sys
import os

# Ensure backend is in path
current_dir = os.path.dirname(os.path.abspath(__file__))
backend_dir = os.path.join(current_dir, 'app')
sys.path.append(current_dir)

from app.agents.orchestrator import app

# Mock Input (Simulating the Frontend)
test_input = {
    "current_action": {
        "action_type": "incision",
        "tool_id": "scalpel",
        "force_vector": [50.0, 50.0, 20.0], # High force ~73.0
        "timestamp": 123456.789
    }
}

# Run the Brain
try:
    print("Invoking Agent Workflow...")
    result = app.invoke(test_input)

    print("--- AGENT FEEDBACK ---")
    print(result["final_feedback"])
    print("\n--- PROCEDURE LOGS ---")
    print(result.get("procedure_logs", "No logs found"))
except Exception as e:
    print(f"Error occurred: {e}")
