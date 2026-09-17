#include "network.h"
#include <ixwebsocket/IXWebSocket.h>
#include <nlohmann/json.hpp>
#include <iostream>
#include <cstdint>

static ix::WebSocket s_ws;
static Network::ItemCallback s_itemCallback = nullptr;

namespace Network {

    void Start(ItemCallback onItemReceived, uint16_t ipcPort) {
        s_itemCallback = onItemReceived;

        std::string url = "ws://127.0.0.1:" + std::to_string(ipcPort) + "/";
        s_ws.setUrl(url);
        std::cout << "[AP-Mod] Connexion vers " << url << std::endl;

        s_ws.setOnMessageCallback([](const ix::WebSocketMessagePtr& msg) {
            if (msg->type == ix::WebSocketMessageType::Open) {
                std::cout << "[AP-Mod] Connecte au client Python !" << std::endl;

            } else if (msg->type == ix::WebSocketMessageType::Message) {
                try {
                    auto json = nlohmann::json::parse(msg->str);
                    if (json.contains("command") && json["command"] == "GIVE_ITEM") {
                        int64_t itemId = json["item_id"].get<int64_t>();
                        if (s_itemCallback) {
                            s_itemCallback(itemId);
                        }
                    }
                } catch (const nlohmann::json::exception& e) {
                    std::cout << "[AP-Mod] Erreur parsing JSON : " << e.what() << std::endl;
                }

            } else if (msg->type == ix::WebSocketMessageType::Error) {
                std::cout << "[AP-Mod] Erreur WebSocket : " << msg->errorInfo.reason << std::endl;

            } else if (msg->type == ix::WebSocketMessageType::Close) {
                std::cout << "[AP-Mod] Connexion fermee par le client Python. Reconnexion automatique..." << std::endl;
            }
        });

        s_ws.enableAutomaticReconnection();
        // Attendre 2s entre les tentatives de reconnexion (défaut IXWebSocket)
        s_ws.setMinWaitBetweenReconnectionRetries(2000);
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
        // sendText est thread-safe dans IXWebSocket (utilisé dans le callback)
        s_ws.sendText(payload.dump());
    }

} // namespace Network
