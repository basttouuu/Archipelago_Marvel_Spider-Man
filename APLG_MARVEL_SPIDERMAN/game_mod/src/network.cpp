#include "network.h"
#include <ixwebsocket/IXWebSocket.h>
#include <nlohmann/json.hpp>
#include <iostream>
#include <cstdint>
#include <cstring>

// Stub de compatibilité STL MSVC pour vcpkg ixwebsocket
extern "C" {
    size_t __cdecl __std_find_first_not_of_trivial_pos_1(
        const char* _First,
        size_t _Size,
        const char* _Target,
        size_t _Count,
        size_t _Pos
    ) {
        if (_Pos >= _Size) return static_cast<size_t>(-1);
        for (size_t i = _Pos; i < _Size; ++i) {
            bool match = false;
            for (size_t j = 0; j < _Count; ++j) {
                if (_First[i] == _Target[j]) {
                    match = true;
                    break;
                }
            }
            if (!match) return i;
        }
        return static_cast<size_t>(-1);
    }
}

static ix::WebSocket s_ws;
static Network::ItemCallback s_itemCallback = nullptr;

namespace Network {
    void Start(ItemCallback onItemReceived) {
        s_itemCallback = onItemReceived;

        std::string url = "ws://127.0.0.1:51234/";
        s_ws.setUrl(url);

        s_ws.setOnMessageCallback([](const ix::WebSocketMessagePtr& msg) {
            if (msg->type == ix::WebSocketMessageType::Open) {
                std::cout << "[AP-Mod] Connecte au client Python !" << std::endl;
            } else if (msg->type == ix::WebSocketMessageType::Message) {
                try {
                    auto json = nlohmann::json::parse(msg->str);
                    if (json.contains("command") && json["command"] == "GIVE_ITEM") {
                        int64_t itemId = json["item_id"];
                        if (s_itemCallback) {
                            s_itemCallback(itemId);
                        }
                    }
                } catch (...) {
                }
            }
        });

        s_ws.enableAutomaticReconnection();
        s_ws.start();
    }

    void Stop() {
        s_ws.stop();
    }

    void SendLocationCheck(int64_t locationId) {
        nlohmann::json payload = {
            {"event", "LOCATION_CHECKED"},
            {"location_id", locationId}
        };
        s_ws.send(payload.dump());
    }
}
