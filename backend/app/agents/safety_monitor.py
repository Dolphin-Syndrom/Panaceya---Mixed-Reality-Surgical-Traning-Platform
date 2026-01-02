import json
from langchain_core.messages import SystemMessage
from langchain_core.tools import tool
from langchain_groq import ChatGroq
from app.models.state import SurgicalState

# --- 1. DEFINE THE TOOL (The Physics Check) ---
@tool
def check_physics_constraints(force: float, tool_type: str) -> str:
    """
    Queries the physics engine. Returns CRITICAL if force exceeds safe limits.
    """
    # Mocking SOFA engine logic for the test
    thresholds = {"scalpel": 80.0, "forceps": 50.0}
    limit = thresholds.get(tool_type, 60.0)
    
    if force > limit:
        return json.dumps({
            "status": "CRITICAL", 
            "damage": "Tissue tear detected", 
            "excess_force": round(force - limit, 2)
        })
    return json.dumps({"status": "SAFE", "damage": "None"})

# --- 2. CONFIGURE GROQ AGENT ---
# Llama 3.1 70b is fast and smart enough for agentic reasoning
# Checks for GROQ_API_KEY env var automatically or can be passed explicitly
import os
if not os.environ.get("GROQ_API_KEY"):
    # Fallback or error handling if needed, though ChatGroq usually raises validation error
    pass 

llm = ChatGroq(
    model="llama-3.3-70b-versatile",
    temperature=0
)

# Bind the tool so the LLM knows it can use it
tools = [check_physics_constraints]
llm_with_tools = llm.bind_tools(tools)

# --- 3. THE AGENT NODE ---
def safety_monitor_agent(state: SurgicalState):
    action = state["current_action"]
    
    # specialized system prompt for Safety
    system_msg = """You are a Surgical Safety Monitor.
    Your ONLY job is to validate the current action against physics constraints.
    You MUST use the 'check_physics_constraints' tool.
    If the tool returns CRITICAL, output a strict warning."""
    
    # Calculate force magnitude for the tool
    # Using Pydantic model in state input might be mixed with dict, 
    # but based on code context 'current_action' seems to be a dict
    force_mag = sum(x**2 for x in action["force_vector"]) ** 0.5
    
    user_msg = f"Action: {action['action_type']}, Tool: {action['tool_id']}, Force: {force_mag}"
    
    # Call Groq
    response = llm_with_tools.invoke([SystemMessage(content=system_msg), ("user", user_msg)])
    
    # --- TOOL EXECUTION LOGIC ---
    # If the LLM generates a tool call, we must execute it.
    if response.tool_calls:
        tool_call = response.tool_calls[0]
        if tool_call["name"] == "check_physics_constraints":
            # Execute the tool
            tool_args = tool_call["args"]
            tool_result = check_physics_constraints.invoke(tool_args)
            return {"safety_flags": [tool_result]}
            
    return {"safety_flags": [response.content]}
