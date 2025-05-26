#!/usr/bin/env python3
"""
UnrealCV Command Tester
This script tries different command variations to find the right spawn command syntax.
"""

import unrealcv
import time
import sys

def test_commands():
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
    
    # Get UnrealCV version and status
    print("\n--- UNREALCV INFO ---")
    try:
        version = client.request('vget /unrealcv/version')
        print(f"UnrealCV Version: {version}")
    except:
        print("Could not get UnrealCV version")
    
    try:
        status = client.request('vget /unrealcv/status')
        print(f"UnrealCV Status: {status}")
    except:
        print("Could not get UnrealCV status")
    
    # Try to get a list of available commands
    print("\n--- TRYING TO GET COMMAND LIST ---")
    try:
        help_result = client.request('vget /unrealcv/help')
        print(f"Available commands: {help_result}")
    except Exception as e:
        print(f"Error getting help: {e}")
    
    # Try different spawn command variations
    blueprint_path = "/Game/LLMGenerated/Blueprints/HunYuanMeshBP.HunYuanMeshBP_C"
    location = "0,0,100"
    x, y, z = location.split(',')
    
    print("\n--- TESTING SPAWN COMMANDS ---")
    spawn_commands = [
        f'vset /objects/spawn {blueprint_path} {x} {y} {z}',
        f'vset /object/spawn {blueprint_path} {x} {y} {z}',
        f'vset /actor/spawn {blueprint_path} {x} {y} {z}',
        f'vrun SpawnActor {blueprint_path} {x} {y} {z}',
        f'vset /objects/create {blueprint_path} {x} {y} {z}',
        f'vset /scene/spawn {blueprint_path} {x} {y} {z}',
        f'vspawn {blueprint_path} {x} {y} {z}',
        f'vrun "SpawnActor {blueprint_path} Location=({x},{y},{z})"',
        f'vrun "Spawn {blueprint_path} {x} {y} {z}"'
    ]
    
    for cmd in spawn_commands:
        print(f"\nTrying: {cmd}")
        try:
            response = client.request(cmd)
            print(f"Response: {response}")
            if not response.startswith('error'):
                print("✓ COMMAND SUCCEEDED!")
            else:
                print("✗ Command failed")
        except Exception as e:
            print(f"Exception: {e}")
    
    # Try to get a list of all objects in the scene
    print("\n--- SCENE OBJECTS ---")
    try:
        objects = client.request('vget /objects')
        print(f"Objects in scene: {objects}")
    except Exception as e:
        print(f"Error getting objects: {e}")
    
    # Try to get player location for reference
    print("\n--- PLAYER INFO ---")
    try:
        player_loc = client.request('vget /camera/0/location')
        print(f"Player location: {player_loc}")
    except Exception as e:
        print(f"Error getting player location: {e}")
    
    print("\nDiagnostic tests completed. If any command succeeded, note it for future use.")
    client.disconnect()
    print("Disconnected from UnrealCV")

if __name__ == "__main__":
    test_commands() 