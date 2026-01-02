import sys
import os
from dotenv import load_dotenv

# 1. SETUP ENV FIRST
# Load .env from project root (parent of backend folder)
root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
env_path = os.path.join(root_dir, '.env')
load_dotenv(env_path)

if not os.environ.get("GROQ_API_KEY"):
    print(f"❌ Error: GROQ_API_KEY not found in environment or .env file at {env_path}.")
else:
    print("✅ GROQ_API_KEY loaded successfully.")

# 2. SETUP PATH & IMPORTS
# Ensure backend is in path
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(current_dir)

from app.agents.orchestrator import app

print("🚀 Starting Panaceya AI (Groq Backend)...")

# TEST CASE: A Dangerous Action (Force = 90, Limit = 80)
dangerous_input = {
    "current_action": {
        "action_type": "incision",
        "tool_id": "scalpel",
        "force_vector": [60.0, 60.0, 30.0], # Magnitude ~90
        "timestamp": 123456789
    }
}

# Run the Graph
try:
    result = app.invoke(dangerous_input)
    
    print("\n--- 🛡️ SAFETY AGENT OUTPUT ---")
    print(result.get("safety_flags", ["No Output"])[0])
    
    print("\n--- 📝 SCRIBE LOGS ---")
    print(result.get("procedure_logs", "No Logs"))
    
    print("\n--- 🩺 COACH FEEDBACK ---")
    print(result.get("final_feedback", "No Feedback"))
    
    if "STOP" in str(result.get("final_feedback", "")):
        print("\n✅ SUCCESS: The system correctly identified the danger!")
    else:
        print("\n⚠️ FAILURE: The system did not catch the error.")

except Exception as e:
    print(f"Error: {e}")
