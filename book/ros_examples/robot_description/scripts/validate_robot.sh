#!/bin/bash

# Script to validate robot description files
# This script checks if URDF and XACRO files are syntactically correct

echo "Validating robot description files..."

# Check if xacro command is available
if ! command -v xacro &> /dev/null; then
    echo "Error: xacro command not found. Please install ros-humble-xacro"
    exit 1
fi

# Check if check_urdf command is available
if ! command -v check_urdf &> /dev/null; then
    echo "Error: check_urdf command not found. Please install ros-humble-urdfdom-tools"
    exit 1
fi

# Define robot description directory
ROBOT_DESC_DIR="$(dirname "$0")/../urdf"

echo "Checking URDF files in: $ROBOT_DESC_DIR"

# Validate basic humanoid URDF
if [ -f "$ROBOT_DESC_DIR/basic_humanoid.urdf" ]; then
    echo "Validating basic_humanoid.urdf..."
    if check_urdf "$ROBOT_DESC_DIR/basic_humanoid.urdf"; then
        echo "✓ basic_humanoid.urdf is valid"
    else
        echo "✗ basic_humanoid.urdf has errors"
        exit 1
    fi
else
    echo "⚠ basic_humanoid.urdf not found"
fi

# Validate humanoid XACRO
if [ -f "$ROBOT_DESC_DIR/humanoid.xacro" ]; then
    echo "Validating humanoid.xacro..."
    if xacro "$ROBOT_DESC_DIR/humanoid.xacro" --check-order; then
        echo "✓ humanoid.xacro syntax is valid"

        # Also try to process the xacro to URDF to ensure it works completely
        if xacro "$ROBOT_DESC_DIR/humanoid.xacro" -o /tmp/humanoid_test.urdf; then
            echo "✓ humanoid.xacro can be processed to URDF"

            # Validate the processed URDF
            if check_urdf /tmp/humanoid_test.urdf; then
                echo "✓ Processed URDF from humanoid.xacro is valid"
            else
                echo "✗ Processed URDF from humanoid.xacro has errors"
                exit 1
            fi
        else
            echo "✗ humanoid.xacro cannot be processed to URDF"
            exit 1
        fi
    else
        echo "✗ humanoid.xacro has syntax errors"
        exit 1
    fi
else
    echo "⚠ humanoid.xacro not found"
fi

echo "All robot description files validated successfully!"
exit 0