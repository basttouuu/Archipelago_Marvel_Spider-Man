#include "memory.h"
#include <psapi.h>

namespace Memory {
    uintptr_t FindPattern(std::string_view pattern, std::string_view mask) {
        MODULEINFO moduleInfo{};
        HMODULE hModule = GetModuleHandleA(nullptr);
        if (!GetModuleInformation(GetCurrentProcess(), hModule, &moduleInfo, sizeof(moduleInfo)))
            return 0;

        auto* base = reinterpret_cast<const uint8_t*>(moduleInfo.lpBaseOfDll);
        const size_t size = moduleInfo.SizeOfImage;
        const size_t patternLen = mask.length();

        for (size_t i = 0; i < size - patternLen; ++i) {
            bool found = true;
            for (size_t j = 0; j < patternLen; ++j) {
                if (mask[j] != '?' && pattern[j] != static_cast<char>(base[i + j])) {
                    found = false;
                    break;
                }
            }
            if (found) {
                return reinterpret_cast<uintptr_t>(&base[i]);
            }
        }
        return 0;
    }

    uintptr_t ResolveRelativeAddress(uintptr_t instructionAddress, int offsetToDisplacement, int instructionLength) {
        if (!instructionAddress) return 0;
        int32_t displacement = *reinterpret_cast<int32_t*>(instructionAddress + offsetToDisplacement);
        return instructionAddress + instructionLength + displacement;
    }
}
