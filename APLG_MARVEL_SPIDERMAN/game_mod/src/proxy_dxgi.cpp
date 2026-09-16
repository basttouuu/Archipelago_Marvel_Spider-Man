#include "proxy_dxgi.h"
#include <iostream>

static HMODULE s_realDxgi = nullptr;

typedef HRESULT(WINAPI* PFN_CreateDXGIFactory)(REFIID riid, void** ppFactory);
typedef HRESULT(WINAPI* PFN_CreateDXGIFactory1)(REFIID riid, void** ppFactory);
typedef HRESULT(WINAPI* PFN_CreateDXGIFactory2)(UINT Flags, REFIID riid, void** ppFactory);

static PFN_CreateDXGIFactory  oCreateDXGIFactory  = nullptr;
static PFN_CreateDXGIFactory1 oCreateDXGIFactory1 = nullptr;
static PFN_CreateDXGIFactory2 oCreateDXGIFactory2 = nullptr;

namespace ProxyDXGI {
    bool Initialize() {
        char systemPath[MAX_PATH];
        GetSystemDirectoryA(systemPath, MAX_PATH);
        strcat_s(systemPath, "\\dxgi.dll");

        s_realDxgi = LoadLibraryA(systemPath);
        if (!s_realDxgi) return false;

        oCreateDXGIFactory  = (PFN_CreateDXGIFactory)GetProcAddress(s_realDxgi, "CreateDXGIFactory");
        oCreateDXGIFactory1 = (PFN_CreateDXGIFactory1)GetProcAddress(s_realDxgi, "CreateDXGIFactory1");
        oCreateDXGIFactory2 = (PFN_CreateDXGIFactory2)GetProcAddress(s_realDxgi, "CreateDXGIFactory2");
        return true;
    }

    void Shutdown() {
        if (s_realDxgi) {
            FreeLibrary(s_realDxgi);
            s_realDxgi = nullptr;
        }
    }
}

extern "C" {
    __declspec(dllexport) HRESULT WINAPI CreateDXGIFactory(REFIID riid, void** ppFactory) {
        if (!oCreateDXGIFactory) ProxyDXGI::Initialize();
        return oCreateDXGIFactory(riid, ppFactory);
    }

    __declspec(dllexport) HRESULT WINAPI CreateDXGIFactory1(REFIID riid, void** ppFactory) {
        if (!oCreateDXGIFactory1) ProxyDXGI::Initialize();
        return oCreateDXGIFactory1(riid, ppFactory);
    }

    __declspec(dllexport) HRESULT WINAPI CreateDXGIFactory2(UINT Flags, REFIID riid, void** ppFactory) {
        if (!oCreateDXGIFactory2) ProxyDXGI::Initialize();
        return oCreateDXGIFactory2(Flags, riid, ppFactory);
    }
}
