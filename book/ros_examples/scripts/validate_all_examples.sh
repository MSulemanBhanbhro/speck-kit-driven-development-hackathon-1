#!/bin/bash

# Script to validate all ROS 2 examples in the book
# This script tests that all examples can be built and basic functionality works

echo "Validating all ROS 2 examples..."

# Check if we're in the right directory
if [ ! -f "package.xml" ] && [ ! -d "ros_examples" ]; then
    echo "Error: This script should be run from the workspace root directory"
    exit 1
fi

# Check if ROS 2 environment is sourced
if [ -z "$ROS_DISTRO" ]; then
    echo "Error: ROS 2 environment not sourced. Please source ROS 2 setup script."
    exit 1
fi

echo "ROS 2 distribution: $ROS_DISTRO"

# Function to validate a Python script
validate_python_script() {
    local script_path="$1"

    if [ ! -f "$script_path" ]; then
        echo "⚠️  Script not found: $script_path"
        return 1
    fi

    # Check if it's a valid Python file
    if python3 -m py_compile "$script_path" 2>/dev/null; then
        echo "✅ Valid Python syntax: $script_path"
        return 0
    else
        echo "❌ Invalid Python syntax: $script_path"
        python3 -m py_compile "$script_path"  # Show the actual error
        return 1
    fi
}

# Function to check if a package has the required files
validate_package_structure() {
    local package_dir="$1"

    if [ ! -d "$package_dir" ]; then
        echo "⚠️  Package directory not found: $package_dir"
        return 1
    fi

    # Check for basic package files
    local has_setup_py=0
    local has_package_xml=0

    if [ -f "$package_dir/setup.py" ] || [ -f "$package_dir/CMakeLists.txt" ]; then
        has_setup_py=1
    fi

    if [ -f "$package_dir/package.xml" ]; then
        has_package_xml=1
    fi

    if [ $has_setup_py -eq 1 ] && [ $has_package_xml -eq 1 ]; then
        echo "✅ Valid package structure: $package_dir"
        return 0
    else
        echo "❌ Incomplete package structure: $package_dir"
        return 1
    fi
}

# Validate basic publisher/subscriber examples
echo ""
echo "🔍 Validating Basic Publisher/Subscriber Examples..."
validate_package_structure "ros_examples/basic_publisher"
validate_package_structure "ros_examples/basic_subscriber"
validate_python_script "ros_examples/basic_publisher/publisher.py"
validate_python_script "ros_examples/basic_subscriber/subscriber.py"

# Validate service examples
echo ""
echo "🔍 Validating Service Examples..."
validate_package_structure "ros_examples/service_server"
validate_package_structure "ros_examples/service_client"
validate_python_script "ros_examples/service_server/server.py"
validate_python_script "ros_examples/service_client/client.py"

# Validate action examples
echo ""
echo "🔍 Validating Action Examples..."
validate_package_structure "ros_examples/action_server"
validate_package_structure "ros_examples/action_client"
validate_python_script "ros_examples/action_server/action_server.py"
validate_python_script "ros_examples/action_client/action_client.py"

# Validate node implementation examples
echo ""
echo "🔍 Validating Node Implementation Examples..."
validate_package_structure "ros_examples/node_implementation"
validate_python_script "ros_examples/node_implementation/sensor_node.py"
validate_python_script "ros_examples/node_implementation/control_server.py"
validate_python_script "ros_examples/node_implementation/control_client.py"
validate_python_script "ros_examples/node_implementation/parametric_node.py"

# Validate robot description
echo ""
echo "🔍 Validating Robot Description..."
validate_package_structure "ros_examples/robot_description"
if [ -f "ros_examples/robot_description/urdf/basic_humanoid.urdf" ]; then
    echo "✅ Basic humanoid URDF found"
else
    echo "❌ Basic humanoid URDF not found"
fi

if [ -f "ros_examples/robot_description/urdf/humanoid.xacro" ]; then
    echo "✅ Humanoid XACRO found"
else
    echo "❌ Humanoid XACRO not found"
fi

# Validate advanced patterns
echo ""
echo "🔍 Validating Advanced Patterns..."
validate_package_structure "ros_examples/advanced_patterns"
validate_python_script "ros_examples/advanced_patterns/lifecycle_node.py"
validate_python_script "ros_examples/advanced_patterns/param_server.py"

# Validate integration example
echo ""
echo "🔍 Validating Integration Example..."
validate_package_structure "ros_examples/integration_example"
validate_python_script "ros_examples/integration_example/integration_demo.py"

# Validate launch files
echo ""
echo "🔍 Validating Launch Files..."
if [ -f "ros_examples/basic_publisher/launch/pub_sub_launch.py" ]; then
    validate_python_script "ros_examples/basic_publisher/launch/pub_sub_launch.py"
else
    echo "❌ Basic publisher launch file not found"
fi

if [ -f "ros_examples/node_implementation/launch/node_launch.py" ]; then
    validate_python_script "ros_examples/node_implementation/launch/node_launch.py"
else
    echo "❌ Node implementation launch file not found"
fi

if [ -f "ros_examples/advanced_patterns/launch/advanced_launch.py" ]; then
    validate_python_script "ros_examples/advanced_patterns/launch/advanced_launch.py"
else
    echo "❌ Advanced patterns launch file not found"
fi

if [ -f "ros_examples/integration_example/launch/integration_launch.py" ]; then
    validate_python_script "ros_examples/integration_example/launch/integration_launch.py"
else
    echo "❌ Integration example launch file not found"
fi

# Validate URDF files
echo ""
echo "🔍 Validating URDF Files..."
if command -v check_urdf &> /dev/null; then
    if [ -f "ros_examples/robot_description/urdf/basic_humanoid.urdf" ]; then
        if check_urdf "ros_examples/robot_description/urdf/basic_humanoid.urdf" &> /tmp/urdf_check.log; then
            echo "✅ Basic humanoid URDF is valid"
        else
            echo "❌ Basic humanoid URDF validation failed:"
            cat /tmp/urdf_check.log
        fi
    fi

    # Check if xacro is available to validate xacro files
    if command -v xacro &> /dev/null; then
        if [ -f "ros_examples/robot_description/urdf/humanoid.xacro" ]; then
            if xacro "ros_examples/robot_description/urdf/humanoid.xacro" --check-order &> /tmp/xacro_check.log; then
                echo "✅ Humanoid XACRO syntax is valid"
            else
                echo "❌ Humanoid XACRO validation failed:"
                cat /tmp/xacro_check.log
            fi
        fi
    else
        echo "⚠️  XACRO command not available, skipping XACRO validation"
    fi
else
    echo "⚠️  check_urdf command not available, skipping URDF validation"
fi

# Check for required dependencies
echo ""
echo "🔍 Checking for required dependencies..."

MISSING_DEPS=()

# Check for basic ROS 2 packages
for pkg in rclpy std_msgs sensor_msgs geometry_msgs example_interfaces lifecycle_msgs; do
    if ! python3 -c "import roslibpy" &> /dev/null && [ "$pkg" = "roslibpy" ]; then
        MISSING_DEPS+=("$pkg")
    elif ! python3 -c "from std_msgs import msg" &> /dev/null && [ "$pkg" = "std_msgs" ]; then
        # Just check if the package is importable
        python3 -c "import sys; sys.path.append('/opt/ros/$ROS_DISTRO/lib/python3.*/site-packages')" &> /dev/null
    fi
done

if [ ${#MISSING_DEPS[@]} -ne 0 ]; then
    echo "❌ Missing dependencies: ${MISSING_DEPS[*]}"
else
    echo "✅ All required dependencies available"
fi

# Summary
echo ""
echo "========================================="
echo "VALIDATION SUMMARY"
echo "========================================="

TOTAL_VALIDATED=$(find ros_examples -name "*.py" -type f | wc -l)
SYNTAX_ERRORS=$(find ros_examples -name "*.py" -type f -exec python3 -m py_compile {} \; 2>&1 | grep -c "SyntaxError\|IndentationError" || echo 0)

echo "Total Python files: $TOTAL_VALIDATED"
echo "Syntax errors: $SYNTAX_ERRORS"
echo "Files with syntax errors: $(find ros_examples -name "*.py" -type f -exec python3 -m py_compile {} \; 2>&1 | grep -E "(SyntaxError|IndentationError)" | wc -l)"

if [ "$SYNTAX_ERRORS" -eq 0 ]; then
    echo ""
    echo "🎉 All examples passed basic validation!"
    echo "Next steps:"
    echo "  1. Build the workspace: colcon build"
    echo "  2. Source the workspace: source install/setup.bash"
    echo "  3. Test individual examples with: ros2 run <package> <executable>"
    exit 0
else
    echo ""
    echo "❌ Some examples have validation errors. Please fix them before proceeding."
    exit 1
fi