cmake_minimum_required(VERSION 3.10)
project(ER_NN)

find_package (Python3 COMPONENTS Interpreter Development REQUIRED)

execute_process(
COMMAND ${Python3_EXECUTABLE} -m pybind11 --cmakedir
OUTPUT_VARIABLE pybind11_cmake_dir
OUTPUT_STRIP_TRAILING_WHITESPACE
)
set(pybind11_DIR ${pybind11_cmake_dir})

message(STATUS "Using pybind11 found at: ${pybind11_DIR}")
find_package(pybind11 REQUIRED)

pybind11_add_module(AOBScanner SHARED src/AOBScanner.cpp)

set_target_properties(AOBScanner PROPERTIES CXX_STANDARD 11 CXX_STANDARD_REQUIRED ON)

set(INIT_PY "${CMAKE_CURRENT_BINARY_DIR}/__init__.py")
if(NOT EXISTS ${INIT_PY})
file(WRITE ${INIT_PY} "")
endif()

add_custom_command(TARGET AOBScanner POST_BUILD
COMMAND ${CMAKE_COMMAND} -E copy
$<TARGET_FILE_DIR:AOBScanner>/$<TARGET_FILE_NAME:AOBScanner>
${CMAKE_CURRENT_BINARY_DIR}/$<TARGET_FILE_NAME:AOBScanner>
)