project (program2)
cmake_minimum_required(VERSION 3.0)

# configure OpenCV
find_package(OpenCV REQUIRED)
include_directories(${OpenCV_INCLUDE_DIRS})

# create create individual projects
add_executable(program2 program2.cpp)
target_link_libraries(program2 ${OpenCV_LIBS})



