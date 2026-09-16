cmake_minimum_required(VERSION 3.20)
project(SpiderManArchipelagoMod CXX)

set(CMAKE_CXX_STANDARD 20)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

# Garantit l'alignement du runtime MSVC dynamique et la compatibilité des fonctions vectorisées STL
if(MSVC)
    set(CMAKE_MSVC_RUNTIME_LIBRARY "MultiThreaded$<$<CONFIG:Debug>:Debug>DLL")
    add_compile_options(/permissive- /Zc:preprocessor)
endif()

find_package(nlohmann_json CONFIG REQUIRED)
find_package(ixwebsocket CONFIG REQUIRED)
find_package(minhook CONFIG REQUIRED)

add_library(dxgi SHARED
    src/dllmain.cpp
    src/proxy_dxgi.h
    src/proxy_dxgi.cpp
    src/network.h
    src/network.cpp
    src/memory.h
    src/memory.cpp
    src/hooks.h
    src/hooks.cpp
)

target_include_directories(dxgi PRIVATE src)
target_link_libraries(dxgi PRIVATE
    nlohmann_json::nlohmann_json
    ixwebsocket::ixwebsocket
    minhook::minhook
    ws2_32
    crypt32
    bcrypt
)

set_target_properties(dxgi PROPERTIES
    PREFIX ""
    OUTPUT_NAME "dxgi"
)
