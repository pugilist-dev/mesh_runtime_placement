# HunYuan3D-v2 to Unreal Engine 5 Integration

This project provides a set of Python scripts for importing 3D meshes generated from HunYuan3D-v2 into Unreal Engine 5 and placing them in a game at runtime using UnrealCV.

## Features

- Import OBJ mesh files into Unreal Engine 5
- Convert the imported meshes to UE5 Static Mesh Assets (.uasset)
- Create Blueprint Assets from the Static Meshes
- Place the objects in a running UE5 game using UnrealCV
- Interactive runtime control of the placed objects

## Requirements

- Unreal Engine 5
- [UnrealCV Plugin](https://github.com/unrealcv/unrealcv) installed in your UE5 project
- Python 3.7+
- Python packages:
  - `unrealcv` (install with `pip install unrealcv`)

## Setup Instructions

1. **Install UnrealCV Plugin in your UE5 project**:
   - Clone the UnrealCV repository or download the plugin
   - Install the plugin to your UE5 project
   - Or create a new project with the plugin included

2. **Create a blank UE5 project**:
   - Use the "Blank" template for best results
   - Enable the UnrealCV plugin in the project settings

3. **Copy these scripts to your project directory**:
   - `hunyuan3d_ue5_demo.py`: Main script for the complete workflow
   - `unreal_engine_import.py`: Script for importing OBJ files into UE5
   - `place_mesh_runtime.py`: Script for runtime placement using UnrealCV
   - `mesh_import_and_place.py`: Combined script for batch processing

## Usage

### Full Workflow

For a complete workflow (import mesh → create blueprint → place in game):

```bash
python hunyuan3d_ue5_demo.py --action full --obj_path /path/to/your/mesh.obj
```

This will guide you through the process step by step.

### Step-by-Step Workflow

#### 1. Import OBJ Mesh into UE5

Run the following in your UE5 Python Editor Console (Window → Developer Tools → Python Console):

```python
import sys
sys.path.append('/path/to/these/scripts')
import hunyuan3d_ue5_demo as demo
bp_path = demo.import_to_ue5('/path/to/your/mesh.obj', '/Game/Meshes', 'MeshBP')
print(f'Use this blueprint path: {bp_path}')
```

#### 2. Place the Blueprint in Runtime

After the import is complete, run:

```bash
python hunyuan3d_ue5_demo.py --action place --blueprint_path /Game/Meshes/MeshBP
```

### Additional Options

```
--asset_path: Path in the UE5 content browser (default: /Game/Meshes)
--blueprint_name: Name for the generated blueprint (default: MeshBP)
--location: Spawn location in X,Y,Z format (default: 0,0,100)
--rotation: Rotation in Pitch,Yaw,Roll format (default: 0,0,0)
--scale: Scale in X,Y,Z format (default: 1,1,1)
```

## Example: Complete Workflow

1. Generate a 3D mesh using HunYuan3D-v2
2. Save the mesh as OBJ file
3. Start your UE5 project with UnrealCV plugin enabled
4. Import the mesh and create a blueprint:
   ```python
   # In UE5 Python Console
   import sys
   sys.path.append('/path/to/scripts')
   import hunyuan3d_ue5_demo as demo
   demo.import_to_ue5('/path/to/mesh.obj')
   ```
5. Start the game (click Play in UE5 editor)
6. Place the object in the running game:
   ```bash
   python hunyuan3d_ue5_demo.py --action place --blueprint_path /Game/Meshes/MeshBP
   ```

## Troubleshooting

1. **Connection Issues with UnrealCV**:
   - Make sure the UnrealCV plugin is enabled in your UE5 project
   - Ensure the game is running in Play mode before attempting to connect
   - Check if the default port (9000) is already in use

2. **OBJ Import Failures**:
   - Verify the OBJ file is valid and complete
   - Try importing manually through the UE5 editor to check for specific errors

3. **Python Errors**:
   - Ensure you're running the import script in UE5's Python console, not your system Python
   - Verify that all required Python modules are installed

## License

This project is provided as-is under the MIT License.

## Acknowledgments

- HunYuan3D-v2 for generating the 3D meshes
- UnrealCV team for the plugin that enables runtime interaction
- Unreal Engine team for the Python API 