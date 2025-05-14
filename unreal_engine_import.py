import unreal
import os
import sys

def import_obj_to_uasset(obj_path, output_asset_path='/Game/Meshes', blueprint_name='MeshBP'):
    """
    Import an OBJ file as a Static Mesh and create a Blueprint from it
    
    Args:
        obj_path (str): Path to the .obj file
        output_asset_path (str): Asset path in the content browser
        blueprint_name (str): Name for the generated blueprint
    
    Returns:
        tuple: (mesh_asset_path, blueprint_path)
    """
    # Ensure the output directory exists
    if not unreal.EditorAssetLibrary.does_directory_exist(output_asset_path):
        unreal.EditorAssetLibrary.make_directory(output_asset_path)
    
    # Set import options for OBJ
    import_options = unreal.FbxImportUI()
    import_options.set_editor_property('import_mesh', True)
    import_options.set_editor_property('import_textures', True)
    import_options.set_editor_property('import_materials', True)
    import_options.static_mesh_import_data.set_editor_property('combine_meshes', True)
    
    # Create import task
    task = unreal.AssetImportTask()
    task.set_editor_property('automated', True)
    task.set_editor_property('destination_path', output_asset_path)
    
    # Get the filename without extension for the asset name
    filename = os.path.basename(obj_path)
    asset_name = os.path.splitext(filename)[0]
    task.set_editor_property('destination_name', asset_name)
    task.set_editor_property('filename', obj_path)
    task.set_editor_property('replace_existing', True)
    task.set_editor_property('save', True)
    task.options = import_options
    
    # Execute import
    unreal.AssetToolsHelpers.get_asset_tools().import_asset_tasks([task])
    
    # Get the imported asset path
    mesh_asset_path = f"{output_asset_path}/{asset_name}"
    print(f"Mesh imported as: {mesh_asset_path}")
    
    # Create blueprint from the mesh
    blueprint_path = create_blueprint_from_mesh(mesh_asset_path, output_asset_path, blueprint_name)
    
    return mesh_asset_path, blueprint_path

def create_blueprint_from_mesh(mesh_asset_path, output_asset_path, blueprint_name):
    """
    Create a blueprint with the mesh as a static mesh component
    
    Args:
        mesh_asset_path (str): Path to the imported mesh asset
        output_asset_path (str): Path where to save the blueprint
        blueprint_name (str): Name for the blueprint
    
    Returns:
        str: Path to the created blueprint
    """
    print(f"Creating blueprint from mesh: {mesh_asset_path}")
    
    # Create blueprint factory
    factory = unreal.BlueprintFactory()
    factory.set_editor_property('parent_class', unreal.Actor)
    
    # Create the blueprint asset
    asset_tools = unreal.AssetToolsHelpers.get_asset_tools()
    blueprint = asset_tools.create_asset(blueprint_name, output_asset_path, unreal.Blueprint, factory)
    
    # Get blueprint component
    blueprint_compiler = unreal.KismetCompilerUtilities.get_default_object()
    
    # Add static mesh component to the blueprint
    component_name = "StaticMeshComponent"
    mesh_component = unreal.EditorAddComponentUtilities.add_static_mesh_component(
        blueprint.get_editor_property('simple_construction_script'),
        component_name
    )
    
    # Load the static mesh asset and assign it to the component
    mesh_asset = unreal.EditorAssetLibrary.load_asset(mesh_asset_path)
    if mesh_asset is not None:
        mesh_component.set_editor_property('static_mesh', mesh_asset)
    
    # Compile the blueprint
    unreal.EditorLoadingAndSavingUtils.save_dirty_packages(False, True)
    blueprint_compiler.compile_blueprint(blueprint)
    
    # Save the blueprint
    unreal.EditorAssetLibrary.save_loaded_asset(blueprint)
    
    blueprint_path = f"{output_asset_path}/{blueprint_name}"
    print(f"Blueprint created at: {blueprint_path}")
    return blueprint_path

# Example usage:
# mesh_path, bp_path = import_obj_to_uasset(r"C:\Path\To\Your\Mesh.obj", "/Game/Meshes", "MyMeshBP") 