#include <cmath>
#include <filesystem>
#include <fstream>
#include <mutex>
#include <string>
#include <vector>

#include <DirectXMath.h>
#include <Windows.h>

#include "imgui.h"
#include "imgui_extensions.h"
#include "mumble/Mumble.h"
#include "nexus/Nexus.h"
#include "rtapi/RTAPI.hpp"

#include "Render.h"
#include "Settings.h"
#include "Shared.h"
#include "Version.h"

namespace dx = DirectX;

void AddonLoad(AddonAPI *aApi);
void AddonUnload();
void AddonRender();
void AddonOptions();

HMODULE hSelf;
AddonDefinition AddonDef{};
std::filesystem::path AddonPath;
std::filesystem::path SettingsPath;

BOOL APIENTRY DllMain(HMODULE hModule, DWORD ul_reason_for_call, LPVOID lpReserved)
{
    switch (ul_reason_for_call)
    {
    case DLL_PROCESS_ATTACH:
        hSelf = hModule;
        break;
    case DLL_PROCESS_DETACH:
        break;
    case DLL_THREAD_ATTACH:
        break;
    case DLL_THREAD_DETACH:
        break;
    }
    return TRUE;
}

extern "C" __declspec(dllexport) AddonDefinition *GetAddonDef()
{
    AddonDef.Signature = -1245535;
    AddonDef.APIVersion = NEXUS_API_VERSION;
    AddonDef.Name = "GW2TP";
    AddonDef.Version.Major = MAJOR;
    AddonDef.Version.Minor = MINOR;
    AddonDef.Version.Build = BUILD;
    AddonDef.Version.Revision = REVISION;
    AddonDef.Author = "Franneck.1274";
    AddonDef.Description = "API Fetch from https://gw2tp-production.up.railway.app/";
    AddonDef.Load = AddonLoad;
    AddonDef.Unload = AddonUnload;
    AddonDef.Flags = EAddonFlags_None;
    AddonDef.Provider = EUpdateProvider_GitHub;
    AddonDef.UpdateLink = "https://github.com/franneck94/Gw2TP";

    return &AddonDef;
}

void OnAddonLoaded(int *aSignature)
{
    if (!aSignature)
    {
        return;
    }
}
void OnAddonUnloaded(int *aSignature)
{
    if (!aSignature)
    {
        return;
    }
}

void AddonLoad(AddonAPI *aApi)
{
    APIDefs = aApi;
    ImGui::SetCurrentContext((ImGuiContext *)APIDefs->ImguiContext);
    ImGui::SetAllocatorFunctions((void *(*)(size_t, void *))APIDefs->ImguiMalloc, (void (*)(void *, void *))APIDefs->ImguiFree); // on imgui 1.80+

    NexusLink = (NexusLinkData *)APIDefs->GetResource("DL_NEXUS_LINK");
    RTAPIData = (RTAPI::RealTimeData *)APIDefs->GetResource(DL_RTAPI);
    APIDefs->RegisterRender(ERenderType_Render, AddonRender);
    APIDefs->RegisterRender(ERenderType_OptionsRender, AddonOptions);
    AddonPath = APIDefs->GetAddonDirectory("GW2TP");
    SettingsPath = APIDefs->GetAddonDirectory("GW2TP/settings.json");
    std::filesystem::create_directory(AddonPath);
    Settings::Load(SettingsPath);
}
void AddonUnload()
{
    APIDefs->DeregisterRender(AddonOptions);
    APIDefs->DeregisterRender(AddonRender);

    NexusLink = nullptr;
    RTAPIData = nullptr;

    Settings::Save(SettingsPath);
}

void AddonRender()
{
    if (!NexusLink || !NexusLink->IsGameplay)
    {
        return;
    }

    static Render render;
    render.requesting();
    render.storing();
    render.render();
}

void AddonOptions()
{
}
