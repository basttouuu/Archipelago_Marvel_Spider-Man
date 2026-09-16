#pragma once
#include <cstdint>
#include <functional>

namespace Network {
    using ItemCallback = std::function<void(int64_t itemId)>;

    void Start(ItemCallback onItemReceived);
    void Stop();
    void SendLocationCheck(int64_t locationId);
}
