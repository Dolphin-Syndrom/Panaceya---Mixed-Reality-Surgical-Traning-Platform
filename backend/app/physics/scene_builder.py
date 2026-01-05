"""SOFA scene builders for different surgical procedures."""

from abc import ABC, abstractmethod
from typing import Optional, List, Tuple, TYPE_CHECKING, Any
import numpy as np
import logging

try:
    import Sofa
    import Sofa.Core
    SOFA_AVAILABLE = True
except ImportError:
    SOFA_AVAILABLE = False
    # Create mock types for when SOFA is not available
    if not TYPE_CHECKING:
        Sofa = Any

logger = logging.getLogger(__name__)


class SceneBuilder(ABC):
    """Abstract base class for SOFA scene builders."""
    
    def __init__(self, gravity: List[float] = [0, -9.81, 0]):
        """Initialize scene builder.
        
        Args:
            gravity: Gravity vector [x, y, z] in m/s²
        """
        self.gravity = gravity
    
    @abstractmethod
    def create_scene(self, root: Any) -> Any:
        """Create the SOFA scene.
        
        Args:
            root: SOFA root node
            
        Returns:
            Configured root node
        """
        pass
    
    def _add_required_plugins(self, root: Any) -> None:
        """Add required SOFA plugins.
        
        Args:
            root: SOFA root node
        """
        plugins = [
            'SofaPython3',
            'SofaOpenglVisual',
            'SofaLoader',
            'SofaMeshCollision',
            'SofaDeformable',
            'SofaEngine',
            'SofaConstraint',
            'SofaGeneralLoader',
            'SofaBoundaryCondition',
        ]
        
        for plugin in plugins:
            try:
                root.addObject('RequiredPlugin', name=plugin)
            except Exception as e:
                logger.warning(f"Could not load plugin {plugin}: {e}")
    
    def _setup_collision_pipeline(self, root: Any) -> None:
        """Setup collision detection pipeline.
        
        Args:
            root: SOFA root node
        """
        root.addObject('CollisionPipeline', depth=6, verbose=False)
        root.addObject('BruteForceBroadPhase')
        root.addObject('BVHNarrowPhase')
        root.addObject('CollisionResponse', response='PenalityContactForceField')
        root.addObject('LocalMinDistance', 
                       alarmDistance=0.5, 
                       contactDistance=0.2,
                       angleCone=0.01)
    
    def _setup_solver(self, root: Any) -> None:
        """Setup time integration and linear solver.
        
        Args:
            root: SOFA root node
        """
        root.addObject('EulerImplicitSolver', 
                       rayleighStiffness=0.1, 
                       rayleighMass=0.1)
        root.addObject('CGLinearSolver', 
                       iterations=25, 
                       tolerance=1e-5, 
                       threshold=1e-5)


class LiverSurgerySceneBuilder(SceneBuilder):
    """Scene builder for liver surgery simulation.
    
    Creates a deformable liver model using FEM with surgical tool interaction.
    """
    
    def __init__(
        self,
        liver_mesh_path: Optional[str] = None,
        young_modulus: float = 3000.0,
        poisson_ratio: float = 0.45,
        total_mass: float = 1.5,
        gravity: List[float] = [0, -9.81, 0]
    ):
        """Initialize liver surgery scene.
        
        Args:
            liver_mesh_path: Path to liver mesh file (.vtk or .obj)
            young_modulus: Young's modulus (Pa) for tissue elasticity
            poisson_ratio: Poisson's ratio (nearly incompressible)
            total_mass: Total mass of liver (kg)
            gravity: Gravity vector
        """
        super().__init__(gravity)
        self.liver_mesh_path = liver_mesh_path or "assets/meshes/organs/liver.vtk"
        self.young_modulus = young_modulus
        self.poisson_ratio = poisson_ratio
        self.total_mass = total_mass
        
        self.liver_node: Optional[Any] = None
        self.tool_node: Optional[Any] = None
    
    def create_scene(self, root: Any) -> Any:
        """Create liver surgery scene.
        
        Args:
            root: SOFA root node
            
        Returns:
            Configured root node with liver and surgical tools
        """
        # Basic setup
        root.gravity = self.gravity
        
        # Add plugins
        self._add_required_plugins(root)
        
        # Setup collision and solver
        self._setup_collision_pipeline(root)
        self._setup_solver(root)
        
        # Create deformable liver
        self.liver_node = self._create_liver(root)
        
        # Create surgical tool
        self.tool_node = self._create_surgical_tool(root)
        
        logger.info("Liver surgery scene created successfully")
        return root
    
    def _create_liver(self, root: Any) -> Any:
        """Create deformable liver model using FEM.
        
        Args:
            root: Parent node
            
        Returns:
            Liver node
        """
        liver = root.addChild('Liver')
        
        # Load tetrahedral mesh
        liver.addObject(
            'MeshVTKLoader',
            name='loader',
            filename=self.liver_mesh_path
        )
        
        liver.addObject(
            'TetrahedronSetTopologyContainer',
            src='@loader',
            name='topo'
        )
        
        liver.addObject(
            'MechanicalObject',
            name='dofs',
            template='Vec3d'
        )
        
        # Mass
        liver.addObject('UniformMass', totalMass=self.total_mass)
        
        # FEM force field (Neo-Hookean material model)
        liver.addObject(
            'TetrahedronFEMForceField',
            name='FEM',
            youngModulus=self.young_modulus,
            poissonRatio=self.poisson_ratio,
            method='large'  # Large displacement formulation
        )
        
        # Fix some vertices to prevent drift
        liver.addObject(
            'BoxROI',
            name='fixedROI',
            box=[-10, 45, -10, 10, 55, 10],
            drawBoxes=True
        )
        
        liver.addObject(
            'FixedConstraint',
            indices='@fixedROI.indices'
        )
        
        # Visual model (surface rendering)
        visual = self._create_visual_model(liver)
        
        # Collision model (surface collision)
        collision = self._create_collision_model(liver)
        
        return liver
    
    def _create_visual_model(
        self, 
        parent: Any
    ) -> Any:
        """Create visual representation for organ.
        
        Args:
            parent: Parent node (e.g., Liver)
            
        Returns:
            Visual node
        """
        visual = parent.addChild('Visual')
        
        visual.addObject(
            'OglModel',
            name='visualModel',
            src='@../loader',
            color='0.8 0.3 0.2 1.0'  # Reddish-brown for liver
        )
        
        visual.addObject(
            'BarycentricMapping',
            input='@../dofs',
            output='@visualModel'
        )
        
        return visual
    
    def _create_collision_model(
        self,
        parent: Any
    ) -> Any:
        """Create collision model for organ.
        
        Args:
            parent: Parent node
            
        Returns:
            Collision node
        """
        collision = parent.addChild('Collision')
        
        collision.addObject(
            'TriangleSetTopologyContainer',
            src='@../loader'
        )
        
        collision.addObject(
            'MechanicalObject',
            name='collisionDofs'
        )
        
        collision.addObject('TriangleCollisionModel')
        collision.addObject('LineCollisionModel')
        collision.addObject('PointCollisionModel')
        
        collision.addObject(
            'BarycentricMapping',
            input='@../dofs',
            output='@collisionDofs'
        )
        
        return collision
    
    def _create_surgical_tool(
        self,
        root: Any,
        initial_position: List[float] = [0, 30, 50]
    ) -> Any:
        """Create surgical tool (scalpel/probe).
        
        Args:
            root: Parent node
            initial_position: Initial tool position [x, y, z]
            
        Returns:
            Tool node
        """
        tool = root.addChild('SurgicalTool')
        
        # Rigid body mechanics
        tool.addObject(
            'MechanicalObject',
            name='dofs',
            template='Rigid3d',
            position=[*initial_position, 0, 0, 0, 1]  # x,y,z, qx,qy,qz,qw
        )
        
        tool.addObject('UniformMass', totalMass=0.05)  # 50g tool
        
        # Collision (simplified sphere at tool tip)
        collision = tool.addChild('Collision')
        collision.addObject(
            'MechanicalObject',
            template='Vec3d',
            position=[0, 0, -20]  # Tool tip offset
        )
        
        collision.addObject(
            'SphereCollisionModel',
            radius=1.0
        )
        
        collision.addObject(
            'RigidMapping',
            input='@../dofs',
            output='@.'
        )
        
        return tool
    
    def get_liver_node(self) -> Optional[Any]:
        """Get liver node reference.
        
        Returns:
            Liver node or None
        """
        return self.liver_node
    
    def get_tool_node(self) -> Optional[Any]:
        """Get tool node reference.
        
        Returns:
            Tool node or None
        """
        return self.tool_node


class LaparoscopySceneBuilder(SceneBuilder):
    """Scene builder for laparoscopic surgery simulation.
    
    Includes multiple organs and laparoscopic instruments.
    """
    
    def __init__(self, gravity: List[float] = [0, -9.81, 0]):
        """Initialize laparoscopy scene.
        
        Args:
            gravity: Gravity vector
        """
        super().__init__(gravity)
    
    def create_scene(self, root: Any) -> Any:
        """Create laparoscopy scene.
        
        Args:
            root: SOFA root node
            
        Returns:
            Configured root node
        """
        # Basic setup
        root.gravity = self.gravity
        
        self._add_required_plugins(root)
        self._setup_collision_pipeline(root)
        self._setup_solver(root)
        
        # Create abdominal cavity with multiple organs
        # TODO: Implement full laparoscopy scene
        
        logger.info("Laparoscopy scene created successfully")
        return root
