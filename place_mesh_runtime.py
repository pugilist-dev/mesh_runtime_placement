#!/usr/bin/env python3
"""
Unreal Engine 5 Runtime Mesh Placement Module
=============================================

This module provides functionality to place 3D meshes in a running Unreal Engine 5 game 
using the UnrealCV plugin. It connects to the UnrealCV server running in the game,
sends commands to spawn the object at a specified location, and provides an interactive
prompt for manipulating the object in real-time.

Requirements:
- UnrealCV Python client (pip install unrealcv)
- A running UE5 game with UnrealCV plugin enabled

Example usage:
python place_mesh_runtime.py --blueprint_path /Game/Meshes/MeshBP --location 0,0,100
"""
import unrealcv
import argparse
import time

def main():
    """
    Main function for the mesh placement tool. Parses command line arguments,
    connects to UnrealCV, spawns the specified blueprint at the given location,
    and provides an interactive command prompt for further manipulation.
    
    Command line arguments:
    --blueprint_path: Path to the blueprint asset in UE5 (e.g., /Game/Meshes/MeshBP)
    --location: Location to place the object as X,Y,Z (default: 0,0,100)
    --rotation: Rotation of the object as Pitch,Yaw,Roll (default: 0,0,0)
    --scale: Scale of the object as X,Y,Z (default: 1,1,1)
    
    Returns:
        None
    """
    parser = argparse.ArgumentParser(description='Place a UE5 blueprint at runtime using UnrealCV')
    parser.add_argument('--blueprint_path', type=str, required=True, 
                        help='Path to the blueprint asset in UE5 (e.g., /Game/Meshes/MeshBP)')
    parser.add_argument('--location', type=str, default='0,0,100', 
                        help='Location to place the object (X,Y,Z)')
    parser.add_argument('--rotation', type=str, default='0,0,0', 
                        help='Rotation of the object (Pitch,Yaw,Roll)')
    parser.add_argument('--scale', type=str, default='1,1,1', 
                        help='Scale of the object (X,Y,Z)')
    args = parser.parse_args()

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
        return
    
    print("Connected to UnrealCV!")
    
    # Parse location
    x, y, z = map(float, args.location.split(','))
    
    # Parse rotation
    pitch, yaw, roll = map(float, args.rotation.split(','))
    
    # Parse scale
    scale_x, scale_y, scale_z = map(float, args.scale.split(','))
    
    # Ensure the blueprint path is in the correct format
    bp_path = args.blueprint_path
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
        return
    
    print(f"Object spawned with ID: {response}")
    object_id = response
    
    # Set rotation if needed
    if args.rotation != '0,0,0':
        rot_cmd = f'vset /object/{object_id}/rotation {pitch} {yaw} {roll}'
        rot_response = client.request(rot_cmd)
        print(f"Set rotation: {rot_response}")
    
    # Set scale if needed
    if args.scale != '1,1,1':
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

if __name__ == "__main__":
    main() 