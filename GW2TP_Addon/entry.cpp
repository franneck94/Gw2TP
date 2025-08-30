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

#include "Settings.h"
#include "Shared.h"
#include "Version.h"

namespace dx = DirectX;

void ProcessKeybind(const char *aIdentifier);
void OnWindowResized(void *aEventArgs);
void OnMumbleIdentityUpdated(void *aEventArgs);

void AddonLoad(AddonAPI *aApi);
void AddonUnload();
void AddonRender();
void AddonOptions();
void AddonShortcut();

HMODULE hSelf;
AddonDefinition AddonDef{};
std::filesystem::path AddonPath;
std::filesystem::path SettingsPath;

const char *COMPASS_TOGGLEVIS = "KB_COMPASS_TOGGLEVIS";
const char *WINDOW_RESIZED = "EV_WINDOW_RESIZED";
const char *MUMBLE_IDENTITY_UPDATED = "EV_MUMBLE_IDENTITY_UPDATED";
const char *HR_TEX = "TEX_SEPARATOR_DETAIL";

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
    AddonDef.Signature = 17;
    AddonDef.APIVersion = NEXUS_API_VERSION;
    AddonDef.Name = "Compass";
    AddonDef.Version.Major = 0;
    AddonDef.Version.Minor = 1;
    AddonDef.Version.Build = 0;
    AddonDef.Version.Revision = 0;
    AddonDef.Author = "Raidcore";
    AddonDef.Description = "Adds a simple compass widget to the UI, as well as to your character in the world.";
    AddonDef.Load = AddonLoad;
    AddonDef.Unload = AddonUnload;
    AddonDef.Flags = EAddonFlags_None;
    AddonDef.Provider = EUpdateProvider_GitHub;
    AddonDef.UpdateLink = "https://github.com/RaidcoreGG/GW2-Compass";

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

    MumbleLink = (Mumble::Data *)APIDefs->GetResource("DL_MUMBLE_LINK");
    MumbleIdentity = (Mumble::Identity *)APIDefs->GetResource("DL_MUMBLE_LINK_IDENTITY");
    NexusLink = (NexusLinkData *)APIDefs->GetResource("DL_NEXUS_LINK");
    RTAPIData = (RTAPI::RealTimeData *)APIDefs->GetResource(DL_RTAPI);

    APIDefs->RegisterKeybindWithString(COMPASS_TOGGLEVIS, ProcessKeybind, "(null)");
    APIDefs->SubscribeEvent(WINDOW_RESIZED, OnWindowResized);
    APIDefs->SubscribeEvent(MUMBLE_IDENTITY_UPDATED, OnMumbleIdentityUpdated);
    APIDefs->AddSimpleShortcut("QAS_COMPASS", AddonShortcut);
    APIDefs->RegisterRender(ERenderType_Render, AddonRender);
    APIDefs->RegisterRender(ERenderType_OptionsRender, AddonOptions);

    AddonPath = APIDefs->GetAddonDirectory("Compass");
    SettingsPath = APIDefs->GetAddonDirectory("Compass/settings.json");
    std::filesystem::create_directory(AddonPath);
    Settings::Load(SettingsPath);

    OnWindowResized(nullptr); // initialise self
}
void AddonUnload()
{
    APIDefs->DeregisterRender(AddonOptions);
    APIDefs->DeregisterRender(AddonRender);
    APIDefs->RemoveSimpleShortcut("QAS_COMPASS");
    APIDefs->UnsubscribeEvent(WINDOW_RESIZED, OnWindowResized);
    APIDefs->DeregisterKeybind(COMPASS_TOGGLEVIS);

    MumbleLink = nullptr;
    MumbleIdentity = nullptr;
    NexusLink = nullptr;
    RTAPIData = nullptr;

    Settings::Save(SettingsPath);
}

void AddonRender()
{
    if (!NexusLink || !MumbleLink || !MumbleIdentity || MumbleLink->Context.IsMapOpen || !NexusLink->IsGameplay)
    {
        return;
    }
}

void AddonOptions()
{
    ImGui::Text("Compass");
}

void AddonShortcut()
{
}

void ProcessKeybind(const char *aIdentifier)
{
    std::string str = aIdentifier;

    /* if COMPASS_TOGGLEVIS is passed, we toggle the compass visibility */
    if (str == COMPASS_TOGGLEVIS)
    {
        Settings::IsWidgetEnabled = !Settings::IsWidgetEnabled;
    }
}

void OnWindowResized(void *aEventArgs)
{
}

void OnMumbleIdentityUpdated(void *aEventArgs)
{
    MumbleIdentity = (Mumble::Identity *)aEventArgs;
}
