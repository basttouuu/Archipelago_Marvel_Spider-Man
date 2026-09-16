#pragma once
#include <cstdint>

namespace GameHooks {
    bool Install();
    void Uninstall();
    void ApplyItem(int64_t itemId);
}
