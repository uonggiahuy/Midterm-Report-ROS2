cmake_minimum_required(VERSION 3.8)
project(littlebot)

find_package(ament_cmake REQUIRED)

install(DIRECTORY 
  meshes 
  urdf 
  launch
  rviz
  DESTINATION share/${PROJECT_NAME}
)

install(PROGRAMS
  scripts/arm_controller.py
  DESTINATION lib/${PROJECT_NAME}
)

ament_package()