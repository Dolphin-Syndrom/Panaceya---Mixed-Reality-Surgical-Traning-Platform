from typing import TypedDict, List, Annotated
import operator
from pydantic import BaseModel, Field

# --- Pydantic Models for Strict Validation ---
class SurgicalAction(BaseModel):
    action_type: str = Field(..., description="The surgical move (e.g., 'incision')")
    tool_id: str = Field(..., description="The instrument used (e.g., 'scalpel')")
    force_vector: List[float] = Field(..., description="[x, y, z] force applied")
    timestamp: float

# --- The Agent State (The Canvas) ---
class SurgicalState(TypedDict):
    # Input
    current_action: dict
    
    # Internal Agent scratchpads
    safety_flags: List[str]
    technique_score: float
    technique_advice: str
    
    # The Log (Memory) - Annotated with 'add' to append logs instead of overwriting
    procedure_logs: Annotated[List[dict], operator.add]
    
    # Final Output
    final_feedback: str
