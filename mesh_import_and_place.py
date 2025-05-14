#!/usr/bin/env python3
import os
import sys
import unreal
import argparse
import time
import unrealcv

# Define command line arguments
parser = argparse.ArgumentParser(description='Import OBJ mesh to UE5 and place it at runtime')
parser.add_argument('--obj_path', type=str, required=True, help='Path to the .obj mesh file')
parser.add_argument('--project_path', type=str, required=True, help='Path to UE5 project directory')
parser.add_argument('--output_asset_path', type=str, default='/Game/Meshes', help='Asset path in UE5 content browser')
parser.add_argument('--blueprint_name', type=str, default='MeshBP', help='Name for the generated blueprint')
parser.add_argument('--location', type=str, default='0,0,100', help='Spawn location (X,Y,Z)')
args = parser.parse_args()

def import_obj_to_uasset():
    """Import OBJ file to UE5 and create a static mesh asset"""
    print(f"Importing OBJ file: {args.obj_path}")
    
    # Set import options
    import_options = unreal.FbxImportUI()
    import_options.set_editor_property('import_mesh', True)
    import_options.set_editor_property('import_textures', True)
    import_options.set_editor_property('import_materials', True)
    import_options.static_mesh_import_data.set_editor_property('combine_meshes', True)
    
    # Import task
    task = unreal.AssetImportTask()
    task.set_editor_property('automated', True)
    task.set_editor_property('destination_path', args.output_asset_path)
    task.set_editor_property('destination_name', os.path.splitext(os.path.basename(args.obj_path))[0])
    task.set_editor_property('filename', args.obj_path)
    task.set_editor_property('replace_existing', True)
    task.set_editor_property('save', True)
    task.options = import_options
    
    # Execute import
    unreal.AssetToolsHelpers.get_asset_tools().import_asset_tasks([task])
    
    # Get the imported asset path
    mesh_asset_path = f"{args.output_asset_path}/{os.path.splitext(os.path.basename(args.obj_path))[0]}"
    print(f"Mesh imported as: {mesh_asset_path}")
    
    return mesh_asset_path

def create_blueprint_from_mesh(mesh_asset_path):
    """Create a blueprint from the imported static mesh"""
    print(f"Creating blueprint from mesh: {mesh_asset_path}")
    
    # Create factory for blueprint
    factory = unreal.BlueprintFactory()
    factory.set_editor_property('parent_class', unreal.Actor)
    
    # Create the blueprint asset
    blueprint_path = f"{args.output_asset_path}/{args.blueprint_name}"
    asset_tools = unreal.AssetToolsHelpers.get_asset_tools()
    blueprint = asset_tools.create_asset(args.blueprint_name, args.output_asset_path, unreal.Blueprint, factory)
    
    # Add static mesh component to the blueprint
    blueprint_compiler = unreal.KismetCompilerUtilities.get_default_object()
    mesh_component = unreal.KismetSystemLibrary.add_component(blueprint, unreal.StaticMeshComponent)
    
    # Load the static mesh asset
    mesh_asset = unreal.EditorAssetLibrary.load_asset(mesh_asset_path)
    mesh_component.set_static_mesh(mesh_asset)
    
    # Compile the blueprint
    unreal.EditorLoadingAndSavingUtils.save_dirty_packages(False, True)
    blueprint_compiler.compile_blueprint(blueprint)
    
    print(f"Blueprint created at: {blueprint_path}")
    return blueprint_path

def runtime_placement_with_unrealcv():
    """Connect to UnrealCV and place the mesh at runtime"""
    print("Connecting to UnrealCV for runtime placement...")
    
    # Connect to UnrealCV
    client = unrealcv.Client(('localhost', 9000))
    
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
        print("Failed to connect to UnrealCV")
        return False
    
    print("Connected to UnrealCV")
    
    # Parse location
    x, y, z = map(float, args.location.split(','))
    
    # Get the full path to the blueprint asset
    blueprint_full_path = f"{args.output_asset_path}/{args.blueprint_name}.{args.blueprint_name}"
    
    # Spawn the blueprint at the specified location
    response = client.request(f'vset /objects/spawn {blueprint_full_path} {x} {y} {z}')
    print(f"Spawn response: {response}")
    
    # Keep the connection open to allow for further commands
    print("Object placed successfully. Press Ctrl+C to exit.")
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("Exiting...")
        client.disconnect()
    
    return True

def main():
    # Step 1: Import OBJ to UAsset
    mesh_asset_path = import_obj_to_uasset()
    
    # Step 2: Create Blueprint from mesh
    blueprint_path = create_blueprint_from_mesh(mesh_asset_path)
    
    # Step 3: Place the object at runtime using UnrealCV
    runtime_placement_with_unrealcv()

if __name__ == "__main__":
    main() 