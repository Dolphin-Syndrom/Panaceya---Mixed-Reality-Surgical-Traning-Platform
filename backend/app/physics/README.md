# Physics Module - SOFA Integration

## Overview

This module provides Python integration with the SOFA Framework for real-time surgical physics simulation on the backend server. The physics engine runs headless (without GUI) and streams mesh deformations to connected clients via WebSocket.

## Architecture

```
┌─────────────────────────────────────────────────────────┐
│                  FastAPI Backend                        │
│  ┌──────────────────────────────────────────────────┐  │
│  │         Physics API Routes                       │  │
│  │  /api/physics/simulations/*                      │  │
│  └────────────┬─────────────────────────────────────┘  │
│               │                                         │
│  ┌────────────▼─────────────────────────────────────┐  │
│  │         SOFA Engine (sofa_engine.py)            │  │
│  │  • Scene management                              │  │
│  │  • Simulation loop                               │  │
│  │  • Force application                             │  │
│  └────────────┬─────────────────────────────────────┘  │
│               │                                         │
│  ┌────────────▼─────────────────────────────────────┐  │
│  │       Scene Builder (scene_builder.py)          │  │
│  │  • Liver surgery scene                           │  │
│  │  • Laparoscopy scene                             │  │
│  │  • Custom organs                                 │  │
│  └────────────┬─────────────────────────────────────┘  │
│               │                                         │
│  ┌────────────▼─────────────────────────────────────┐  │
│  │      Mesh Updater (mesh_updater.py)             │  │
│  │  • Mesh decimation                               │  │
│  │  • Interpolation                                 │  │
│  │  • Differential updates                          │  │
│  └──────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────┘
                       │
                       │ WebSocket
                       ▼
            ┌──────────────────┐
            │  Frontend Client │
            │  (Three.js)      │
            └──────────────────┘
```

## Components

### 1. SOFA Engine (`sofa_engine.py`)
Main physics engine wrapper that manages SOFA simulations.

**Features:**
- Headless simulation (no GUI)
- Async simulation loop
- Force application API
- State extraction

**Example:**
```python
from app.physics import SOFAEngine, LiverSurgerySceneBuilder

# Create engine
engine = SOFAEngine(dt=0.01)  # 100 Hz simulation

# Create scene
builder = LiverSurgerySceneBuilder()
engine.create_scene(builder)

# Run simulation
await engine.start_simulation(duration=10.0)
```

### 2. Scene Builder (`scene_builder.py`)
Constructs SOFA scenes programmatically.

**Available Scenes:**
- `LiverSurgerySceneBuilder` - Deformable liver with FEM
- `LaparoscopySceneBuilder` - Multi-organ laparoscopic scene

**Example:**
```python
from app.physics import LiverSurgerySceneBuilder

builder = LiverSurgerySceneBuilder(
    liver_mesh_path="path/to/liver.vtk",
    young_modulus=3000.0,  # Pa (soft tissue)
    poisson_ratio=0.45,     # Nearly incompressible
    total_mass=1.5          # kg
)
```

### 3. Mesh Updater (`mesh_updater.py`)
Processes physics updates for efficient streaming.

**Features:**
- Mesh decimation (reduce bandwidth)
- Interpolation (smooth rendering)
- Differential updates (only changed vertices)
- Deformation metrics

**Example:**
```python
from app.physics import MeshUpdater

updater = MeshUpdater(
    interpolate=True,
    decimation_factor=2  # Keep every 2nd vertex
)

# Process SOFA update
object_states = updater.update_from_sofa(physics_update)

# Get only changed vertices
diff = updater.compute_mesh_diff("Liver", threshold=0.001)
```

### 4. Physics State (`physics_state.py`)
Pydantic models for physics data.

**Models:**
- `PhysicsUpdate` - Single frame update
- `PhysicsState` - Complete simulation state
- `ObjectState` - Individual object state
- `ToolInteraction` - User interaction event
- `SimulationConfig` - Simulation parameters

## API Endpoints

### Create Simulation
```http
POST /api/physics/simulations/create
Content-Type: application/json

{
  "scene_type": "liver",
  "dt": 0.01,
  "gravity": [0, -9.81, 0],
  "young_modulus": 3000.0,
  "poisson_ratio": 0.45
}
```

**Response:**
```json
{
  "simulation_id": "uuid-here",
  "timestamp": 0.0,
  "step": 0,
  "is_running": false,
  "dt": 0.01,
  "objects": {}
}
```

### Start Simulation
```http
POST /api/physics/simulations/{sim_id}/start?duration=60.0
```

### WebSocket Stream
```javascript
const ws = new WebSocket('ws://localhost:8000/api/physics/simulations/{sim_id}/stream');

ws.onmessage = (event) => {
  const update = JSON.parse(event.data);
  // update.objects.Liver.positions
  // Update Three.js mesh
};
```

### Apply Tool Interaction
```http
POST /api/physics/simulations/{sim_id}/interact
Content-Type: application/json

{
  "tool_id": "scalpel_01",
  "interaction_type": "force",
  "target_object": "Liver",
  "target_point": [0.5, 1.2, 0.3],
  "force_vector": [0, -5.0, 0],
  "timestamp": 1234567890.123
}
```

## Installation

### 1. Install SOFA Framework

**Windows:**
```powershell
# Download from https://www.sofa-framework.org/download/
# Install pre-built binaries
# Add SOFA to PATH

# Verify installation
python -c "import Sofa; print('SOFA installed')"
```

**Linux:**
```bash
# Build from source or use package manager
sudo apt-get install sofa-framework
# Or follow: https://www.sofa-framework.org/community/doc/

# Install SofaPython3
python -m pip install SofaPython3
```

### 2. Install Python Dependencies
```bash
cd backend
pip install -r requirements.txt
```

### 3. Test Installation
```bash
pytest tests/test_physics/ -v
```

## Usage Example

### Backend Server
```python
from fastapi import FastAPI
from app.physics import SOFAEngine, LiverSurgerySceneBuilder

app = FastAPI()

# Create simulation endpoint
@app.post("/create-sim")
async def create_simulation():
    engine = SOFAEngine(dt=0.01)
    builder = LiverSurgerySceneBuilder()
    engine.create_scene(builder)
    
    # Start simulation
    asyncio.create_task(engine.start_simulation())
    
    return {"sim_id": "123", "status": "running"}
```

### Frontend Client (Three.js)
```javascript
import * as THREE from 'three';

// Connect to physics WebSocket
const ws = new WebSocket('ws://localhost:8000/api/physics/simulations/123/stream');

// Create Three.js mesh
const geometry = new THREE.BufferGeometry();
const material = new THREE.MeshPhongMaterial({ color: 0xff3333 });
const liverMesh = new THREE.Mesh(geometry, material);

// Update mesh on physics updates
ws.onmessage = (event) => {
  const update = JSON.parse(event.data);
  
  if (update.objects.Liver) {
    const positions = new Float32Array(
      update.objects.Liver.positions.flat()
    );
    geometry.setAttribute('position', 
      new THREE.BufferAttribute(positions, 3)
    );
    geometry.computeVertexNormals();
  }
};
```

## Performance Optimization

### 1. Mesh Decimation
Reduce vertex count for bandwidth efficiency:
```python
updater = MeshUpdater(decimation_factor=4)  # Keep 1/4 vertices
```

### 2. Differential Updates
Send only changed vertices:
```python
diff = updater.compute_mesh_diff("Liver", threshold=0.001)
# Only vertices that moved > 1mm
```

### 3. Adaptive Timestep
Adjust simulation frequency based on load:
```python
engine = SOFAEngine(dt=0.02)  # 50 Hz instead of 100 Hz
```

### 4. Client-Side Interpolation
Smooth rendering between physics updates:
```python
updater = MeshUpdater(interpolate=True)
interpolated = updater.interpolate_state("Liver", alpha=0.5)
```

## Troubleshooting

### SOFA Not Found
```
ImportError: No module named 'Sofa'
```
**Solution:** Install SOFA and ensure Python bindings are in PATH.

### Performance Issues
```
Physics updates lagging behind
```
**Solution:**
1. Increase `dt` (reduce frequency)
2. Enable mesh decimation
3. Use differential updates
4. Optimize FEM mesh resolution

### WebSocket Disconnects
```
WebSocket closed unexpectedly
```
**Solution:** Check simulation is running and engine hasn't crashed. Add error handling in WebSocket endpoint.

## Future Enhancements

- [ ] Multi-tool interaction
- [ ] Tissue cutting/tearing
- [ ] Blood flow simulation
- [ ] Haptic feedback integration
- [ ] GPU-accelerated physics (CUDA)
- [ ] Distributed simulation (multiple servers)

## References

- [SOFA Framework Documentation](https://www.sofa-framework.org/community/doc/)
- [SOFA Python3 Plugin](https://github.com/sofa-framework/SofaPython3)
- [FastAPI WebSockets](https://fastapi.tiangolo.com/advanced/websockets/)
- [Three.js BufferGeometry](https://threejs.org/docs/#api/en/core/BufferGeometry)
