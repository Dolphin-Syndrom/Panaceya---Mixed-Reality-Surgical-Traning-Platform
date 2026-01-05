"""Mesh updater for computing and streaming mesh deformations."""

from typing import Dict, List, Optional, Tuple
import numpy as np
from scipy.spatial import KDTree
import logging

from app.physics.physics_state import PhysicsUpdate, ObjectState

logger = logging.getLogger(__name__)


class MeshUpdater:
    """Handles mesh deformation computation and interpolation.
    
    Computes mesh updates from SOFA physics engine and prepares them
    for streaming to frontend clients via WebSocket.
    """
    
    def __init__(
        self,
        interpolate: bool = True,
        decimation_factor: int = 1
    ):
        """Initialize mesh updater.
        
        Args:
            interpolate: Whether to interpolate between physics steps
            decimation_factor: Factor to reduce mesh resolution for streaming
        """
        self.interpolate = interpolate
        self.decimation_factor = decimation_factor
        
        # Cache for previous state (for interpolation)
        self._previous_state: Optional[Dict[str, np.ndarray]] = None
        self._current_state: Optional[Dict[str, np.ndarray]] = None
    
    def update_from_sofa(
        self,
        physics_update: PhysicsUpdate
    ) -> Dict[str, ObjectState]:
        """Process physics update from SOFA engine.
        
        Args:
            physics_update: Raw physics update from SOFA
            
        Returns:
            Dictionary of object states ready for streaming
        """
        object_states = {}
        
        for obj_name, mesh_data in physics_update.meshes.items():
            # Convert to numpy for processing
            positions = np.array(mesh_data["positions"])
            velocities = np.array(mesh_data.get("velocities")) if mesh_data.get("velocities") else None
            
            # Apply decimation if needed
            if self.decimation_factor > 1:
                positions, velocities = self._decimate_mesh(
                    positions, velocities, self.decimation_factor
                )
            
            # Store current state for interpolation
            if self._previous_state is None:
                self._previous_state = {}
            
            self._previous_state[obj_name] = self._current_state.get(obj_name) if self._current_state else positions
            
            if self._current_state is None:
                self._current_state = {}
            self._current_state[obj_name] = positions
            
            # Create object state
            object_states[obj_name] = ObjectState(
                name=obj_name,
                object_type="deformable",
                positions=positions.tolist(),
                velocities=velocities.tolist() if velocities is not None else None
            )
        
        return object_states
    
    def _decimate_mesh(
        self,
        positions: np.ndarray,
        velocities: Optional[np.ndarray],
        factor: int
    ) -> Tuple[np.ndarray, Optional[np.ndarray]]:
        """Reduce mesh resolution for bandwidth optimization.
        
        Args:
            positions: Vertex positions (N, 3)
            velocities: Vertex velocities (N, 3) or None
            factor: Decimation factor (keep every Nth vertex)
            
        Returns:
            Decimated positions and velocities
        """
        # Simple uniform decimation (keep every Nth vertex)
        decimated_positions = positions[::factor]
        decimated_velocities = velocities[::factor] if velocities is not None else None
        
        logger.debug(
            f"Decimated mesh from {len(positions)} to {len(decimated_positions)} vertices"
        )
        
        return decimated_positions, decimated_velocities
    
    def interpolate_state(
        self,
        object_name: str,
        alpha: float
    ) -> Optional[np.ndarray]:
        """Interpolate between previous and current state.
        
        Used for smooth rendering when physics runs slower than display framerate.
        
        Args:
            object_name: Name of object to interpolate
            alpha: Interpolation factor (0 = previous, 1 = current)
            
        Returns:
            Interpolated positions or None if not available
        """
        if not self.interpolate:
            return None
        
        if self._previous_state is None or self._current_state is None:
            return None
        
        if object_name not in self._previous_state or object_name not in self._current_state:
            return None
        
        prev = self._previous_state[object_name]
        curr = self._current_state[object_name]
        
        # Linear interpolation
        interpolated = prev * (1 - alpha) + curr * alpha
        
        return interpolated
    
    def compute_mesh_diff(
        self,
        object_name: str,
        threshold: float = 0.001
    ) -> Optional[Dict[int, List[float]]]:
        """Compute differential update (only changed vertices).
        
        Reduces bandwidth by only sending vertices that moved significantly.
        
        Args:
            object_name: Object name
            threshold: Minimum displacement to consider as change (meters)
            
        Returns:
            Dictionary mapping vertex index to new position
        """
        if self._previous_state is None or self._current_state is None:
            return None
        
        if object_name not in self._previous_state or object_name not in self._current_state:
            return None
        
        prev = self._previous_state[object_name]
        curr = self._current_state[object_name]
        
        # Compute displacements
        displacements = np.linalg.norm(curr - prev, axis=1)
        
        # Find vertices that moved more than threshold
        changed_indices = np.where(displacements > threshold)[0]
        
        if len(changed_indices) == 0:
            return None
        
        # Build differential update
        diff = {
            int(idx): curr[idx].tolist()
            for idx in changed_indices
        }
        
        logger.debug(
            f"Mesh diff for {object_name}: {len(diff)}/{len(curr)} vertices changed"
        )
        
        return diff
    
    def compute_deformation_metrics(
        self,
        object_name: str
    ) -> Optional[Dict[str, float]]:
        """Compute deformation metrics for analysis.
        
        Useful for detecting tissue damage or excessive deformation.
        
        Args:
            object_name: Object name
            
        Returns:
            Dictionary of deformation metrics
        """
        if self._previous_state is None or self._current_state is None:
            return None
        
        if object_name not in self._previous_state or object_name not in self._current_state:
            return None
        
        prev = self._previous_state[object_name]
        curr = self._current_state[object_name]
        
        # Compute displacement field
        displacement = curr - prev
        displacement_magnitude = np.linalg.norm(displacement, axis=1)
        
        metrics = {
            "max_displacement": float(np.max(displacement_magnitude)),
            "mean_displacement": float(np.mean(displacement_magnitude)),
            "std_displacement": float(np.std(displacement_magnitude)),
            "total_deformation_energy": float(np.sum(displacement_magnitude ** 2))
        }
        
        return metrics
    
    def find_nearest_vertex(
        self,
        object_name: str,
        point: List[float]
    ) -> Optional[Tuple[int, float]]:
        """Find nearest vertex to a point (for tool interaction).
        
        Args:
            object_name: Object name
            point: 3D point [x, y, z]
            
        Returns:
            Tuple of (vertex_index, distance) or None
        """
        if self._current_state is None or object_name not in self._current_state:
            return None
        
        positions = self._current_state[object_name]
        
        # Build KD-tree for efficient nearest neighbor search
        tree = KDTree(positions)
        
        # Query nearest point
        distance, index = tree.query(point)
        
        return int(index), float(distance)
    
    def reset(self) -> None:
        """Reset internal state."""
        self._previous_state = None
        self._current_state = None
        logger.info("Mesh updater reset")
