# Copyright (c) 2023, AgiBot Inc.
# All rights reserved.

file(GLOB_RECURSE BAGTRANS_SRC_FILES ${CMAKE_CURRENT_SOURCE_DIR}/../bagtrans/*)

set(BAGTRANS_BUILD_DIR ${CMAKE_BINARY_DIR}/bagtrans_pkg)

add_custom_target(
  bagtrans
  WORKING_DIRECTORY ${BAGTRANS_BUILD_DIR}/bagtrans
  # Build wheel
  COMMAND ${PYTHON_EXECUTABLE} -m build --wheel --no-isolation -v
  COMMENT "${PYTHON_EXECUTABLE} -m build --wheel --no-isolation -v"
  # Build executable
  COMMAND ${PYTHON_EXECUTABLE} -m PyInstaller ${BAGTRANS_BUILD_DIR}/bagtrans/bagtrans/bagtrans.spec --distpath ${BAGTRANS_BUILD_DIR}/bagtrans/dist
  COMMENT "${PYTHON_EXECUTABLE} -m PyInstaller ${BAGTRANS_BUILD_DIR}/bagtrans/bagtrans/bagtrans.spec --distpath ${BAGTRANS_BUILD_DIR}/bagtrans/dist"
  DEPENDS ${BAGTRANS_SRC_FILES})

add_custom_target(
  copy_ros2_plugin_proto_files_bagtrans
  COMMAND ${CMAKE_COMMAND} -E copy_directory ${CMAKE_INSTALL_PREFIX}/lib/ ${BAGTRANS_BUILD_DIR}/bagtrans/ros2_plugin_proto/lib/
  COMMAND ${CMAKE_COMMAND} -E copy_directory ${CMAKE_INSTALL_PREFIX}/local/ ${BAGTRANS_BUILD_DIR}/bagtrans/ros2_plugin_proto/local/
  COMMAND ${CMAKE_COMMAND} -E copy_directory ${CMAKE_INSTALL_PREFIX}/share/ros2_plugin_proto/ ${BAGTRANS_BUILD_DIR}/bagtrans/ros2_plugin_proto/share/ros2_plugin_proto/
  COMMENT "Copying ROS2 files"
  DEPENDS aimrt::plugins::ros2_plugin)

add_custom_target(
  copy_bagtrans_pkg
  COMMAND ${CMAKE_COMMAND} -E make_directory ${BAGTRANS_BUILD_DIR}/bagtrans/
  COMMAND ${CMAKE_COMMAND} -E copy_directory ${CMAKE_CURRENT_SOURCE_DIR}/../bagtrans ${BAGTRANS_BUILD_DIR}/bagtrans/
  COMMAND ${CMAKE_COMMAND} -E copy_if_different ${PROJECT_SOURCE_DIR}/VERSION ${PROJECT_SOURCE_DIR}/LICENSE ${BAGTRANS_BUILD_DIR}
  COMMENT "Copying bagtrans files")

add_dependencies(bagtrans copy_ros2_plugin_proto_files_bagtrans copy_bagtrans_pkg)
