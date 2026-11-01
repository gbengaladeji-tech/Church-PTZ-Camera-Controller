cmake_minimum_required(VERSION 3.13)

if(NOT DEFINED ENV{PICO_SDK_PATH})
    message(FATAL_ERROR "PICO_SDK_PATH must point to a Raspberry Pi Pico SDK checkout")
endif()
if(NOT DEFINED PICO_BOARD)
    message(FATAL_ERROR "Set PICO_BOARD to the exact W55RP20-EVB-PICO board definition")
endif()

include($ENV{PICO_SDK_PATH}/external/pico_sdk_import.cmake)
project(church_ptz_controller C CXX ASM)
set(CMAKE_C_STANDARD 11)
set(CMAKE_CXX_STANDARD 17)
pico_sdk_init()

add_library(ptz_core
    src/controller.cpp
    src/inputs.cpp
    src/joystick.cpp
    src/nextion.cpp
    src/router.cpp
    src/visca.cpp
)
target_include_directories(ptz_core PUBLIC include)

add_executable(ptz_commissioning src/pico_main.cpp)
target_link_libraries(ptz_commissioning PRIVATE ptz_core pico_stdlib)
pico_enable_stdio_usb(ptz_commissioning 1)
pico_enable_stdio_uart(ptz_commissioning 0)
pico_add_extra_outputs(ptz_commissioning)
