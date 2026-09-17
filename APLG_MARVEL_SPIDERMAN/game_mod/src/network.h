#pragma once
#include <cstdint>
#include <functional>

namespace Network {
    using ItemCallback = std::function<void(int64_t itemId)>;

    // Port local sur lequel le client Python écoute les connexions de la DLL.
    // Doit correspondre à LOCAL_IPC_PORT dans SpidermanClient.py.
    static constexpr uint16_t DEFAULT_IPC_PORT = 51234;

    void Start(ItemCallback onItemReceived, uint16_t ipcPort = DEFAULT_IPC_PORT);
    void Stop();
    void SendLocationCheck(int64_t locationId);
}
