"""Physics state management and data structures."""

from typing import Dict, Any, List, Optional, TYPE_CHECKING
from pydantic import BaseModel, Field
import numpy as np

if TYPE_CHECKING:
    from typing import Dict


class PhysicsUpdate(BaseModel):
    """Physics state update sent to clients.
    
    Contains mesh positions, velocities, and metadata for rendering.
    """
    
    timestamp: float = Field(..., description="Simulation time in seconds")
    step: int = Field(..., description="Simulation step number")
    meshes: Dict[str, Dict[str, Any]] = Field(
        default_factory=dict,
        description="Mesh data keyed by object name"
    )
    
    class Config:
        json_schema_extra = {
            "example": {
                "timestamp": 1.25,
                "step": 125,
                "meshes": {
                    "Liver": {
                        "positions": [[0.0, 1.0, 0.0], [1.0, 1.0, 0.0]],
                        "velocities": [[0.0, -0.1, 0.0], [0.0, -0.1, 0.0]]
                    }
                }
            }
        }


class PhysicsState(BaseModel):
    """Complete physics simulation state.
    
    Represents the full state of a physics simulation at a given moment.
    """
    
    simulation_id: str = Field(..., description="Unique simulation identifier")
    timestamp: float = Field(..., description="Current simulation time")
    step: int = Field(..., description="Current step number")
    is_running: bool = Field(default=False, description="Simulation running status")
    dt: float = Field(default=0.01, description="Timestep in seconds")
    
    objects: Dict[str, 'ObjectState'] = Field(
        default_factory=dict,
        description="State of all objects in simulation"
    )
    
    class Config:
        json_schema_extra = {
            "example": {
                "simulation_id": "sim_123456",
                "timestamp": 5.67,
                "step": 567,
                "is_running": True,
                "dt": 0.01,
                "objects": {}
            }
        }


class ObjectState(BaseModel):
    """State of a single physics object.
    
    Contains positions, velocities, and forces for mesh vertices.
    """
    
    name: str = Field(..., description="Object name")
    object_type: str = Field(..., description="Type: 'deformable', 'rigid', 'static'")
    
    positions: List[List[float]] = Field(
        default_factory=list,
        description="Vertex positions [[x,y,z], ...]"
    )
    
    velocities: Optional[List[List[float]]] = Field(
        None,
        description="Vertex velocities [[vx,vy,vz], ...]"
    )
    
    forces: Optional[List[List[float]]] = Field(
        None,
        description="Forces on vertices [[fx,fy,fz], ...]"
    )
    
    indices: Optional[List[List[int]]] = Field(
        None,
        description="Face indices for rendering [[v0,v1,v2], ...]"
    )
    
    class Config:
        json_schema_extra = {
            "example": {
                "name": "Liver",
                "object_type": "deformable",
                "positions": [[0.0, 0.0, 0.0], [1.0, 0.0, 0.0]],
                "velocities": [[0.0, -0.1, 0.0], [0.0, -0.1, 0.0]],
                "forces": None,
                "indices": [[0, 1, 2], [1, 2, 3]]
            }
        }


class ToolInteraction(BaseModel):
    """Represents a tool interaction with the physics simulation.
    
    Used to apply forces, constraints, or other interactions from user input.
    """
    
    tool_id: str = Field(..., description="Surgical tool identifier")
    interaction_type: str = Field(
        ...,
        description="Type: 'force', 'constraint', 'cut', 'grasp'"
    )
    
    target_object: str = Field(..., description="Target object name")
    target_point: Optional[List[float]] = Field(
        None,
        description="3D point of interaction [x, y, z]"
    )
    
    force_vector: Optional[List[float]] = Field(
        None,
        description="Applied force [fx, fy, fz] in Newtons"
    )
    
    constraint_indices: Optional[List[int]] = Field(
        None,
        description="Vertex indices to constrain"
    )
    
    timestamp: float = Field(..., description="When interaction occurred")
    
    class Config:
        json_schema_extra = {
            "example": {
                "tool_id": "scalpel_01",
                "interaction_type": "force",
                "target_object": "Liver",
                "target_point": [0.5, 1.2, 0.3],
                "force_vector": [0.0, -5.0, 0.0],
                "constraint_indices": None,
                "timestamp": 1234567890.123
            }
        }


class SimulationConfig(BaseModel):
    """Configuration for physics simulation.
    
    Defines simulation parameters and scene setup.
    """
    
    scene_type: str = Field(..., description="Scene type: 'liver', 'laparoscopy', etc.")
    dt: float = Field(default=0.01, description="Timestep in seconds")
    gravity: List[float] = Field(
        default=[0, -9.81, 0],
        description="Gravity vector [x, y, z]"
    )
    
    # Material properties
    young_modulus: float = Field(
        default=3000.0,
        description="Young's modulus (Pa) for soft tissue"
    )
    poisson_ratio: float = Field(
        default=0.45,
        description="Poisson's ratio (0.5 = incompressible)"
    )
    
    # Solver parameters
    solver_iterations: int = Field(
        default=25,
        description="Linear solver max iterations"
    )
    solver_tolerance: float = Field(
        default=1e-5,
        description="Linear solver convergence tolerance"
    )
    
    # Collision parameters
    collision_alarm_distance: float = Field(
        default=0.5,
        description="Distance to trigger collision alarm (mm)"
    )
    collision_contact_distance: float = Field(
        default=0.2,
        description="Contact distance for collision response (mm)"
    )
    
    class Config:
        json_schema_extra = {
            "example": {
                "scene_type": "liver",
                "dt": 0.01,
                "gravity": [0, -9.81, 0],
                "young_modulus": 3000.0,
                "poisson_ratio": 0.45,
                "solver_iterations": 25,
                "solver_tolerance": 1e-5,
                "collision_alarm_distance": 0.5,
                "collision_contact_distance": 0.2
            }
        }


# Rebuild forward references
PhysicsState.model_rebuild()
