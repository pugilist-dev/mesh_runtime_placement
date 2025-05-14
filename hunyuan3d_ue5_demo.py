#!/usr/bin/env python3
"""
HunYuan3D-v2 to Unreal Engine 5 Demo
====================================

This script automates the process of:
1. Taking a HunYuan3D-v2 generated OBJ mesh
2. Importing it into UE5 as a .uasset
3. Creating a Blueprint from the mesh
4. Placing the object in a UE5 game at runtime using UnrealCV

Requirements:
- Python 3.7+
- UnrealCV Python client (pip install unrealcv)
- Access to Unreal Engine Python API
- Unreal Engine 5 with UnrealCV plugin installed

Usage examples:
--------------
# Import a mesh into UE5 (run in UE5 Python console)
python -c "import hunyuan3d_ue5_demo as demo; demo.import_to_ue5('/path/to/mesh.obj')"

# Place an existing blueprint in runtime
python hunyuan3d_ue5_demo.py --action place --blueprint_path /Game/Meshes/MeshBP

# Full workflow (requires UE5 to be running)
python hunyuan3d_ue5_demo.py --action full --obj_path /path/to/mesh.obj
"""

import os
import sys
import argparse
import time
import subprocess

try:
    import unrealcv
except ImportError:
    print("Warning: UnrealCV module not found. Runtime placement won't work.")
    print("Install with: pip install unrealcv")

def parse_arguments():
    """
    Parse command line arguments for the script.
    
    This function defines and processes the command line interface for the script,
    including validation of required arguments based on the selected action.
    
    Available actions:
    - import: Import a mesh into UE5 (requires obj_path)
    - place: Place a blueprint in a running game (requires blueprint_path)
    - full: Complete workflow from import to placement (requires obj_path)
    
    Returns:
        argparse.Namespace: The parsed command line arguments
    """
    parser = argparse.ArgumentParser(description='HunYuan3D-v2 to UE5 Import and Placement')
    parser.add_argument('--action', type=str, choices=['import', 'place', 'full'], required=True,
                        help='Action to perform: import, place, or full workflow')
    parser.add_argument('--obj_path', type=str, 
                        help='Path to the OBJ mesh file (required for import and full actions)')
    parser.add_argument('--project_path', type=str,
                        help='Path to UE5 project directory')
    parser.add_argument('--asset_path', type=str, default='/Game/Meshes',
                        help='Asset path in UE5 content browser')
    parser.add_argument('--blueprint_name', type=str, default='MeshBP',
                        help='Name for the generated blueprint')
    parser.add_argument('--blueprint_path', type=str,
                        help='Full path to existing blueprint (for place action)')
    parser.add_argument('--location', type=str, default='0,0,100',
                        help='Location to place the object (X,Y,Z)')
    parser.add_argument('--rotation', type=str, default='0,0,0',
                        help='Rotation of the object (Pitch,Yaw,Roll)')
    parser.add_argument('--scale', type=str, default='1,1,1',
                        help='Scale of the object (X,Y,Z)')
    
    args = parser.parse_args()
    
    # Validate arguments
    if args.action in ['import', 'full'] and not args.obj_path:
        parser.error("--obj_path is required for import and full actions")
    
    if args.action == 'place' and not args.blueprint_path:
        parser.error("--blueprint_path is required for place action")
    
    return args

def import_to_ue5(obj_path, asset_path='/Game/Meshes', blueprint_name='MeshBP'):
    """
    This function should be run from within UE5's Python console.
    It imports an OBJ file and creates a blueprint.
    
    Returns the path to the created blueprint.
    """
    try:
        import unreal
    except ImportError:
        print("Error: This function must be run from within Unreal Engine's Python console")
        print("You cannot run this directly from your regular Python environment")
        return None
    
    # Import the local script to avoid code duplication
    local_dir = os.path.dirname(os.path.abspath(__file__))
    sys.path.append(local_dir)
    
    try:
        import unreal_engine_import
        mesh_path, bp_path = unreal_engine_import.import_obj_to_uasset(
            obj_path, asset_path, blueprint_name
        )
        print(f"Successfully imported {obj_path} to {mesh_path}")
        print(f"Created blueprint at {bp_path}")
        return bp_path
    except Exception as e:
        print(f"Error importing mesh: {e}")
        return None

def place_in_runtime(blueprint_path, location='0,0,100', rotation='0,0,0', scale='1,1,1'):
    """
    Places the blueprint in the running UE5 instance using UnrealCV.
    
    This function connects to a running UE5 game instance with the UnrealCV plugin,
    spawns the specified blueprint at the given location, and provides an interactive
    prompt for further manipulation of the object in real-time.
    
    Args:
        blueprint_path (str): Path to the blueprint in UE5's content browser
        location (str): Location coordinates as "X,Y,Z" string (default: "0,0,100")
        rotation (str): Rotation angles as "Pitch,Yaw,Roll" string (default: "0,0,0")
        scale (str): Scale factors as "X,Y,Z" string (default: "1,1,1")
        
    Returns:
        bool: True if the object was placed successfully, False otherwise
    """
    try:
        import unrealcv
    except ImportError:
        print("Error: UnrealCV module not found. Install with: pip install unrealcv")
        return False
    
    # Connect to UnrealCV
    client = unrealcv.Client(('localhost', 9000))
    
    print("Attempting to connect to UnrealCV...")
    
    # Try to connect for 30 seconds
    timeout = 30
    connected = False
    
    for i in range(timeout):
        if client.isconnected():
            connected = True
            break
        else:
            try:
                client.connect()
                if client.isconnected():
                    connected = True
                    break
            except:
                pass
            print(f"Waiting for UnrealCV connection... {i+1}/{timeout}")
            time.sleep(1)
    
    if not connected:
        print("Failed to connect to UnrealCV. Make sure your UE5 game is running with UnrealCV enabled.")
        return False
    
    print("Connected to UnrealCV!")
    
    # Parse location
    x, y, z = map(float, location.split(','))
    
    # Parse rotation
    pitch, yaw, roll = map(float, rotation.split(','))
    
    # Parse scale
    scale_x, scale_y, scale_z = map(float, scale.split(','))
    
    # Ensure the blueprint path is in the correct format
    bp_path = blueprint_path
    if not bp_path.endswith('_C'):
        # Add class specifier if needed
        if '.' not in bp_path:
            # Add the class name
            bp_name = bp_path.split('/')[-1]
            bp_path = f"{bp_path}.{bp_name}_C"
        else:
            # If already has a class name but missing _C
            bp_path = f"{bp_path}_C"
    
    print(f"Spawning blueprint: {bp_path}")
    
    # Spawn the blueprint at the specified location
    spawn_cmd = f'vset /objects/spawn {bp_path} {x} {y} {z}'
    response = client.request(spawn_cmd)
    
    if response.startswith('error'):
        print(f"Error spawning object: {response}")
        client.disconnect()
        return False
    
    print(f"Object spawned with ID: {response}")
    object_id = response
    
    # Set rotation if needed
    if rotation != '0,0,0':
        rot_cmd = f'vset /object/{object_id}/rotation {pitch} {yaw} {roll}'
        rot_response = client.request(rot_cmd)
        print(f"Set rotation: {rot_response}")
    
    # Set scale if needed
    if scale != '1,1,1':
        scale_cmd = f'vset /object/{object_id}/scale {scale_x} {scale_y} {scale_z}'
        scale_response = client.request(scale_cmd)
        print(f"Set scale: {scale_response}")
    
    print("\nObject placed successfully!")
    print("Commands available:")
    print("  - Press Ctrl+C to exit")
    print("  - The object ID is:", object_id)
    print("  - To move object, you can use:")
    print(f"    vset /object/{object_id}/location X Y Z")
    print(f"    vset /object/{object_id}/rotation PITCH YAW ROLL")
    print(f"    vset /object/{object_id}/scale X Y Z")
    
    try:
        while True:
            command = input("\nEnter a custom UnrealCV command (or 'exit' to quit): ")
            if command.lower() == 'exit':
                break
            
            response = client.request(command)
            print(f"Response: {response}")
    except KeyboardInterrupt:
        print("\nExiting...")
    finally:
        client.disconnect()
        print("Disconnected from UnrealCV")
    
    return True

def main():
    """
    Main entry point for the script.
    
    This function:
    1. Parses the command line arguments
    2. Based on the action parameter, performs one of the following operations:
       - import: Provides instructions for importing a mesh in UE5's Python console
       - place: Places an existing blueprint in a running UE5 game
       - full: Guides the user through the complete workflow
    
    The script can handle three different workflows:
    1. Import-only: For use within UE5's Python console
    2. Place-only: For placing existing blueprints in a running game
    3. Full workflow: A combination of both, guiding the user through each step
    """
    args = parse_arguments()
    
    if args.action == 'import':
        print("Note: This action should be run within Unreal Engine's Python console.")
        print("Please copy the following code and run it in the UE5 Python console:")
        print("\n" + "=" * 50)
        print(f"import sys")
        print(f"sys.path.append('{os.path.dirname(os.path.abspath(__file__))}')")
        print(f"import hunyuan3d_ue5_demo as demo")
        print(f"demo.import_to_ue5('{args.obj_path}', '{args.asset_path}', '{args.blueprint_name}')")
        print("=" * 50 + "\n")
    
    elif args.action == 'place':
        place_in_runtime(args.blueprint_path, args.location, args.rotation, args.scale)
    
    elif args.action == 'full':
        print("Full workflow:")
        print("1. First, import the mesh in UE5 by running the following in the UE5 Python console:")
        print("\n" + "=" * 50)
        print(f"import sys")
        print(f"sys.path.append('{os.path.dirname(os.path.abspath(__file__))}')")
        print(f"import hunyuan3d_ue5_demo as demo")
        print(f"bp_path = demo.import_to_ue5('{args.obj_path}', '{args.asset_path}', '{args.blueprint_name}')")
        print(f"print(f'Use this blueprint path: {{bp_path}}')")
        print("=" * 50 + "\n")
        
        print("2. After the import is complete, copy the blueprint path and run:")
        print(f"python {__file__} --action place --blueprint_path PASTE_BLUEPRINT_PATH_HERE --location {args.location}")
        
        # Ask if user wants to attempt runtime placement now
        bp_path = f"{args.asset_path}/{args.blueprint_name}"
        response = input(f"\nDo you want to attempt runtime placement now with path {bp_path}? (y/n): ")
        if response.lower() == 'y':
            place_in_runtime(bp_path, args.location, args.rotation, args.scale)

if __name__ == "__main__":
    main() 