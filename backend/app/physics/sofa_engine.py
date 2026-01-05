"""SOFA physics engine wrapper for headless simulation."""

import asyncio
from typing import Optional, Dict, Any, List
import numpy as np
from pathlib import Path
import logging

try:
    import Sofa
    import Sofa.Core
    import Sofa.Simulation
    import SofaRuntime
    SOFA_AVAILABLE = True
except ImportError:
    SOFA_AVAILABLE = False
    # Create mock module for type hints when SOFA not available
    class _MockSofa:
        class Core:
            class Node:
                pass
    Sofa = _MockSofa()  # type: ignore
    logging.warning("SOFA Framework not installed. Physics simulation will be disabled.")

from app.physics.physics_state import PhysicsState, PhysicsUpdate

logger = logging.getLogger(__name__)


class SOFAEngine:
    """Headless SOFA physics engine for surgical simulation.
    
    This class manages SOFA simulations on the backend server without GUI,
    streaming physics updates to connected clients via WebSocket.
    
    Attributes:
        root_node: SOFA scene root node
        simulation_running: Whether simulation is actively running
        dt: Simulation timestep (seconds)
        current_step: Current simulation step counter
    """
    
    def __init__(self, dt: float = 0.01):
        """Initialize SOFA engine.
        
        Args:
            dt: Simulation timestep in seconds (default: 0.01 = 100Hz)
        """
        if not SOFA_AVAILABLE:
            raise RuntimeError(
                "SOFA Framework not installed. "
                "Please install from https://www.sofa-framework.org"
            )
        
        self.dt = dt
        self.root_node: Optional[Sofa.Core.Node] = None
        self.simulation_running = False
        self.current_step = 0
        self._simulation_task: Optional[asyncio.Task] = None
        
        # Load required SOFA plugins
        self._load_plugins()
    
    def _load_plugins(self) -> None:
        """Load required SOFA plugins."""
        try:
            SofaRuntime.PluginRepository.addFirstPath(
                str(Path.home() / "sofa" / "plugins")
            )
        except Exception as e:
            logger.warning(f"Could not set plugin path: {e}")
    
    def create_scene(self, scene_builder) -> Sofa.Core.Node:
        """Create a SOFA scene using a scene builder.
        
        Args:
            scene_builder: Scene builder instance with create_scene method
            
        Returns:
            SOFA root node
        """
        # Create root node
        self.root_node = Sofa.Core.Node("root")
        
        # Configure root node
        self.root_node.dt = self.dt
        self.root_node.gravity = [0, -9.81, 0]
        
        # Let scene builder configure the scene
        scene_builder.create_scene(self.root_node)
        
        # Initialize simulation
        Sofa.Simulation.init(self.root_node)
        
        logger.info(f"SOFA scene created with dt={self.dt}s")
        return self.root_node
    
    def step(self) -> PhysicsUpdate:
        """Execute one simulation step.
        
        Returns:
            PhysicsUpdate containing mesh positions and metadata
        """
        if not self.root_node:
            raise RuntimeError("Scene not initialized. Call create_scene first.")
        
        # Execute one simulation step
        Sofa.Simulation.animate(self.root_node, self.dt)
        self.current_step += 1
        
        # Extract physics state
        update = self._extract_physics_state()
        
        return update
    
    def _extract_physics_state(self) -> PhysicsUpdate:
        """Extract current physics state from SOFA scene.
        
        Returns:
            PhysicsUpdate with current mesh positions and velocities
        """
        meshes = {}
        
        # Traverse scene graph and extract deformable object states
        for child in self.root_node.children:
            if hasattr(child, 'getMechanicalState'):
                mech_state = child.getMechanicalState()
                if mech_state:
                    name = child.name.value
                    
                    # Get positions
                    positions = np.array(mech_state.position.value)
                    
                    # Get velocities if available
                    velocities = None
                    if hasattr(mech_state, 'velocity'):
                        velocities = np.array(mech_state.velocity.value)
                    
                    meshes[name] = {
                        "positions": positions.tolist(),
                        "velocities": velocities.tolist() if velocities is not None else None,
                    }
        
        return PhysicsUpdate(
            timestamp=self.current_step * self.dt,
            step=self.current_step,
            meshes=meshes
        )
    
    async def start_simulation(self, duration: Optional[float] = None) -> None:
        """Start simulation loop.
        
        Args:
            duration: Simulation duration in seconds (None = infinite)
        """
        if self.simulation_running:
            logger.warning("Simulation already running")
            return
        
        self.simulation_running = True
        logger.info(f"Starting SOFA simulation (duration={duration}s)")
        
        steps = int(duration / self.dt) if duration else None
        step_count = 0
        
        while self.simulation_running:
            if steps and step_count >= steps:
                break
            
            # Execute simulation step
            self.step()
            step_count += 1
            
            # Yield control to other tasks
            await asyncio.sleep(0)
    
    def stop_simulation(self) -> None:
        """Stop simulation loop."""
        self.simulation_running = False
        logger.info("SOFA simulation stopped")
    
    def reset_simulation(self) -> None:
        """Reset simulation to initial state."""
        if self.root_node:
            Sofa.Simulation.reset(self.root_node)
            self.current_step = 0
            logger.info("SOFA simulation reset")
    
    def apply_force(
        self, 
        object_name: str, 
        point_index: int, 
        force: List[float]
    ) -> None:
        """Apply external force to a simulation object.
        
        Args:
            object_name: Name of the object in scene graph
            point_index: Index of the point to apply force to
            force: Force vector [fx, fy, fz] in Newtons
        """
        if not self.root_node:
            raise RuntimeError("Scene not initialized")
        
        # Find object in scene graph
        obj_node = self.root_node.getChild(object_name)
        if not obj_node:
            raise ValueError(f"Object '{object_name}' not found in scene")
        
        # Get mechanical state
        mech_state = obj_node.getMechanicalState()
        if not mech_state:
            raise ValueError(f"Object '{object_name}' has no mechanical state")
        
        # Apply force (implementation depends on SOFA force field setup)
        # This is a simplified example - actual implementation may vary
        logger.debug(
            f"Applying force {force} to {object_name} at point {point_index}"
        )
    
    def get_object_state(self, object_name: str) -> Optional[Dict[str, Any]]:
        """Get state of a specific object.
        
        Args:
            object_name: Name of the object
            
        Returns:
            Dictionary with positions, velocities, and forces
        """
        if not self.root_node:
            return None
        
        obj_node = self.root_node.getChild(object_name)
        if not obj_node:
            return None
        
        mech_state = obj_node.getMechanicalState()
        if not mech_state:
            return None
        
        return {
            "positions": np.array(mech_state.position.value).tolist(),
            "velocities": np.array(mech_state.velocity.value).tolist(),
        }
    
    def cleanup(self) -> None:
        """Cleanup SOFA resources."""
        if self.simulation_running:
            self.stop_simulation()
        
        if self.root_node:
            Sofa.Simulation.unload(self.root_node)
            self.root_node = None
        
        logger.info("SOFA engine cleaned up")
    
    def __del__(self):
        """Destructor to ensure cleanup."""
        try:
            self.cleanup()
        except:
            pass
