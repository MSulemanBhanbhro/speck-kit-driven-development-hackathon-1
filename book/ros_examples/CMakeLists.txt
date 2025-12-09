cmake_minimum_required(VERSION 3.8)
project(ros_examples)

if(CMAKE_COMPILER_IS_GNUCXX OR CMAKE_CXX_COMPILER_ID MATCHES "Clang")
  add_compile_options(-Wall -Wextra -Wpedantic)
endif()

# Find dependencies
find_package(ament_cmake REQUIRED)
find_package(rclcpp REQUIRED)
find_package(rclpy REQUIRED)
find_package(std_msgs REQUIRED)
find_package(sensor_msgs REQUIRED)
find_package(geometry_msgs REQUIRED)
find_package(example_interfaces REQUIRED)
find_package(lifecycle_msgs REQUIRED)
find_package(rosidl_default_generators REQUIRED)

# Install Python modules
ament_python_install_package(${PROJECT_NAME})

# Install Python executables
install(PROGRAMS
  basic_publisher/publisher.py
  basic_subscriber/subscriber.py
  service_server/server.py
  service_client/client.py
  node_implementation/sensor_node.py
  node_implementation/control_server.py
  node_implementation/control_client.py
  node_implementation/parametric_node.py
  action_server/action_server.py
  action_client/action_client.py
  advanced_patterns/lifecycle_node.py
  advanced_patterns/param_server.py
  integration_example/integration_demo.py
  DESTINATION lib/${PROJECT_NAME}
)

# Install launch files
install(DIRECTORY
  basic_publisher/launch
  node_implementation/launch
  robot_description/launch
  advanced_patterns/launch
  integration_example/launch
  DESTINATION share/${PROJECT_NAME}/launch
)

# Install URDF/XACRO files
install(DIRECTORY
  robot_description/urdf
  DESTINATION share/${PROJECT_NAME}/urdf
)

# Install scripts
install(PROGRAMS
  robot_description/scripts/validate_robot.sh
  DESTINATION lib/${PROJECT_NAME}
)

if(BUILD_TESTING)
  find_package(ament_lint_auto REQUIRED)
  # the following line skips the linter which checks for copyrights
  # comment the line when a copyright and license is added to all source files
  set(ament_cmake_copyright_FOUND TRUE)
  # the following line skips cpplint (only works in a git repo)
  # comment the line when this package is in a git repo and cpplint is enabled
  set(ament_cmake_cpplint_FOUND TRUE)
  ament_lint_auto_find_test_dependencies()
endif()

ament_package()