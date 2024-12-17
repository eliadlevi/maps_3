cmake_minimum_required(VERSION 3.8)
project(shared_interfaces)

# Find required tools
find_package(rosidl_default_generators REQUIRED)
find_package(builtin_interfaces REQUIRED)

# Generate message interfaces
rosidl_generate_interfaces(${PROJECT_NAME}
  "msg/SegmentationMask.msg"
  DEPENDENCIES builtin_interfaces
)

# Export runtime dependencies
ament_export_dependencies(rosidl_default_runtime)

ament_package()
