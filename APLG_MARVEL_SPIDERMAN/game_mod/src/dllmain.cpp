#include <windows.h>
#include <iostream>
#include "proxy_dxgi.h"
#include "network.h"
#include "hooks.h"

DWORD WINAPI ModMainThread(LPVOID) {
    AllocConsole();
    FILE* fDummy;
    freopen_s(&fDummy, "CONIN$", "r", stdin);
    freopen_s(&fDummy, "CONOUT$", "w", stdout);
    freopen_s(&fDummy, "CONOUT$", "w", stderr);
    SetConsoleTitleA("Spider-Man Remastered - Archipelago Bridge");

    std::cout << "=====================================================" << std::endl;
    std::cout << "  Marvel's Spider-Man Remastered - Archipelago Proxy " << std::endl;
    std::cout << "=====================================================" << std::endl;

    GameHooks::Install();
    Network::Start([](int64_t itemId) {
        GameHooks::ApplyItem(itemId);
    });

    return 0;
}

BOOL APIENTRY DllMain(HMODULE hModule, DWORD ul_reason_for_call, LPVOID lpReserved) {
    switch (ul_reason_for_call) {
    case DLL_PROCESS_ATTACH:
        DisableThreadLibraryCalls(hModule);
        if (ProxyDXGI::Initialize()) {
            CreateThread(nullptr, 0, ModMainThread, nullptr, 0, nullptr);
        }
        break;
    case DLL_PROCESS_DETACH:
        Network::Stop();
        GameHooks::Uninstall();
        ProxyDXGI::Shutdown();
        break;
    }
    return TRUE;
}
