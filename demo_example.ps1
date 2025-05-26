# HunYuan3D-v2 to UE5 Demo Example Script for Windows
# Configuration - Update these paths
$SAMPLE_OBJ = "D:/ue5/mesh_runtime_placement/data/result/mesh.obj"  # Path to your sample mesh
$REPO_PATH = "D:/ue5/mesh_runtime_placement"  # Path to this repository
$ASSET_PATH = "/Game/LLMGenerated/Meshes"
$MESH_NAME = "ChairBP"  # This will be the name of the blueprint
$SPAWN_LOCATION = "0,0,100"  # X,Y,Z coordinates

Write-Host "========================================================"
Write-Host "HunYuan3D-v2 to Unreal Engine 5 Runtime Mesh Placement Demo"
Write-Host "========================================================"

# Check if sample mesh exists
if (-not (Test-Path $SAMPLE_OBJ)) {
    Write-Host "Error: Sample mesh file not found at $SAMPLE_OBJ"
    Write-Host "Please place a sample .obj file at this location or update the script."
    exit 1
}

Write-Host "Step 1: Import OBJ to UE5 and Create Blueprint"
Write-Host "--------------------------------------------"
Write-Host "Please run the following code in UE5's Python console:"
Write-Host ""
Write-Host "import sys"
Write-Host "sys.path.append('$REPO_PATH')"
Write-Host "import hunyuan3d_ue5_demo as demo"
Write-Host "blueprint_path = demo.import_to_ue5('$SAMPLE_OBJ', '$ASSET_PATH', '$MESH_NAME')"
Write-Host "print(f'Blueprint created at: {blueprint_path}')"
Write-Host ""

Read-Host -Prompt "After running the above in UE5's Python console, press Enter to continue..."

Write-Host ""
Write-Host "Step 2: Start the game in UE5"
Write-Host "-----------------------------"
Write-Host "Please click the 'Play' button in UE5 editor to start the game."
Write-Host "This is required for UnrealCV to connect to the running game."
Write-Host ""

Read-Host -Prompt "After starting the game in UE5, press Enter to continue..."

Write-Host ""
Write-Host "Step 3: Place the blueprint in the game using UnrealCV"
Write-Host "-------------------------------------------------------"
Write-Host "Running command to place the object in the game:"
Write-Host "python hunyuan3d_ue5_demo.py --action place --blueprint_path $ASSET_PATH/$MESH_NAME --location $SPAWN_LOCATION"
Write-Host ""

Read-Host -Prompt "Press Enter to execute this command..."

# Run the command to place the object in the game
Set-Location -Path $REPO_PATH
python hunyuan3d_ue5_demo.py --action place --blueprint_path "$ASSET_PATH/$MESH_NAME" --location "$SPAWN_LOCATION"

Write-Host ""
Write-Host "========================================================"
Write-Host "Demo Complete"
Write-Host "========================================================"
Write-Host "You have successfully completed the runtime mesh placement demo."
