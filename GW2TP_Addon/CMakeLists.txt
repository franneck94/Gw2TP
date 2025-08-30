cmake_minimum_required(VERSION 3.20)
project(GW2TP_Addon)

set(CMAKE_CXX_STANDARD 23)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

include(FetchContent)
FetchContent_Declare(
    imgui
    GIT_REPOSITORY https://github.com/ocornut/imgui.git
    GIT_TAG v1.89.9
)
FetchContent_MakeAvailable(imgui)

add_library(third_party_libs STATIC)
target_include_directories(third_party_libs PUBLIC
    ${imgui_SOURCE_DIR}
    ${imgui_SOURCE_DIR}/backends
)
file(GLOB IMGUI_SOURCES
    ${imgui_SOURCE_DIR}/*.cpp
    ${imgui_SOURCE_DIR}/backends/imgui_impl_win32.cpp
    ${imgui_SOURCE_DIR}/backends/imgui_impl_dx11.cpp
)
target_sources(third_party_libs PRIVATE ${IMGUI_SOURCES} ${KIERO_SOURCES})

add_library(nexus INTERFACE
    "nexus/Nexus.h"
)
add_library(mumble INTERFACE
    "mumble/Mumble.h"
)
add_library(rtapi INTERFACE
    "rtapi/RTAPI.hpp"
)

target_link_libraries(third_party_libs PRIVATE
    d3d11
    d3dcompiler
    nexus
    mumble
    rtapi
)

add_library(Shared STATIC
    "Shared.cpp"
)
target_link_libraries(Shared PRIVATE
    third_party_libs
)

add_library(Settings STATIC
    "Settings.cpp"
)
target_link_libraries(Settings PRIVATE
    third_party_libs
    Shared
)

add_library(entry SHARED
    "entry.cpp"
)
target_link_libraries(entry PRIVATE
    third_party_libs
    Shared
    Settings
)
