from langgraph.graph import StateGraph, END
from app.models.state import SurgicalState
from app.agents import safety_monitor

# --- SMART MOCKS (Dynamic Logic for Testing) ---

def technique_stub(state):
    """
    Simulates a vision system. 
    It 'looks' at the action_type to decide the score.
    """
    # Defensive check if current_action is missing (mock robustness)
    action_type = state.get("current_action", {}).get("action_type", "").lower()
    
    # Simulate detecting a tremor based on a keyword in the input
    if "tremor" in action_type or "shaky" in action_type:
        return {
            "technique_score": 0.45, 
            "technique_advice": "⚠️ High jitter detected. Stabilize your wrist."
        }
    
    return {
        "technique_score": 0.95, 
        "technique_advice": "✅ Smooth trajectory. Excellent control."
    }

def scribe_stub(state):
    """
    The 'Scribe' aggregates logs.
    """
    # Create the new log entry
    current_logs = state.get("procedure_logs", [])
    new_log = {
        "step_number": len(current_logs) + 1,
        "action": state["current_action"]["action_type"],
        "tool": state["current_action"]["tool_id"],
        "safety_status": state.get("safety_flags", ["Unknown"])[0],
        "technique_score": state.get("technique_score", 0.0)
    }
    # Return it as a list (LangGraph's reducer will append this to the main list)
    return {"procedure_logs": [new_log]}

def coach_stub(state):
    """
    The 'Learning Coach' synthesizes feedback.
    Priority: Safety > Technique > Praise
    """
    safety_msgs = str(state.get("safety_flags", ""))
    tech_score = state.get("technique_score", 1.0)
    
    # 1. Safety Block (Highest Priority)
    if "CRITICAL" in safety_msgs:
        return {"final_feedback": "🛑 STOP! Critical safety violation detected."}
    
    # 2. Technique Correction
    if tech_score < 0.7:
        return {"final_feedback": f"💡 Coaching: {state['technique_advice']}"}
    
    # 3. Praise
    return {"final_feedback": "✅ Perfect execution. Proceed to next step."}

# --- BUILD THE GRAPH ---
workflow = StateGraph(SurgicalState)

# Add Nodes
workflow.add_node("safety_monitor", safety_monitor.safety_monitor_agent)
workflow.add_node("technique_analyzer", technique_stub)
workflow.add_node("scribe", scribe_stub)
workflow.add_node("learning_coach", coach_stub)

# Define Flow
# 1. Start with Safety & Technique (Parallel start simulated by sequential for MVP)
workflow.set_entry_point("safety_monitor")
workflow.add_edge("safety_monitor", "technique_analyzer")

# 2. Then Log it
workflow.add_edge("technique_analyzer", "scribe")

# 3. Then Coach user
workflow.add_edge("scribe", "learning_coach")
workflow.add_edge("learning_coach", END)

app = workflow.compile()
