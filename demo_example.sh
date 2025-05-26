#!/bin/bash
# HunYuan3D-v2 to UE5 Demo Example Script
# This script demonstrates the workflow for a sample OBJ file

# Configuration
SAMPLE_OBJ="./data/result/mesh.obj"  # Path to your sample mesh
UE5_PROJECT_PATH="D:/ue5/MyProject2/UnRealCVTest"  # Update this to your UE5 project path
ASSET_PATH="/Game/LLMGenerated"
BLUEPRINT_NAME="HunYuanMeshBP"
SPAWN_LOCATION="0,0,100"  # X,Y,Z coordinates

echo "========================================================"
echo "HunYuan3D-v2 to Unreal Engine 5 Workflow Demo"
echo "========================================================"

# Check if sample mesh exists
if [ ! -f "$SAMPLE_OBJ" ]; then
    echo "Error: Sample mesh file not found at $SAMPLE_OBJ"
    echo "Please place a sample .obj file at this location or update the script."
    exit 1
fi

echo "Step 1: Import OBJ to UE5"
echo "-------------------------"
echo "Please run the following code in UE5's Python console:"
echo ""
echo "import sys"
echo "sys.path.append('$(pwd)')"
echo "import hunyuan3d_ue5_demo as demo"
echo "bp_path = demo.import_to_ue5('$SAMPLE_OBJ', '$ASSET_PATH', '$BLUEPRINT_NAME')"
echo "print(f'Blueprint created at: {bp_path}')"
echo ""

read -p "After running the above in UE5's Python console, press Enter to continue..."

echo ""
echo "Step 2: Start the game in UE5"
echo "-----------------------------"
echo "Please click the 'Play' button in UE5 editor to start the game."
echo "This is required for UnrealCV to connect to the running game."
echo ""

read -p "After starting the game in UE5, press Enter to continue..."

echo ""
echo "Step 3: Place the object in the game using UnrealCV"
echo "--------------------------------------------------"
echo "Running command to place the object in the game:"
echo "python hunyuan3d_ue5_demo.py --action place --blueprint_path $ASSET_PATH/$BLUEPRINT_NAME --location $SPAWN_LOCATION"
echo ""

read -p "Press Enter to execute this command..."

# Run the command to place the object in the game
python hunyuan3d_ue5_demo.py --action place --blueprint_path "$ASSET_PATH/$BLUEPRINT_NAME" --location "$SPAWN_LOCATION"

echo ""
echo "========================================================"
echo "Demo Complete"
echo "========================================================"
echo "You have successfully completed the HunYuan3D to UE5 workflow demo."
echo "To run this with your own meshes, update the SAMPLE_OBJ variable in this script"
echo "or use the Python scripts directly as described in the README.md file." 