#pragma once
#include <windows.h>
#include <cstdint>
#include <string_view>

namespace Memory {
    uintptr_t FindPattern(std::string_view pattern, std::string_view mask);
    uintptr_t ResolveRelativeAddress(uintptr_t instructionAddress, int offsetToDisplacement, int instructionLength);
}
