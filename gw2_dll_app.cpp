#include <mutex>
#include <string>
#include <thread>
#include <vector>
#include <windows.h>
#include <winhttp.h>
#include <d3d11.h>
#include <dxgi.h>

#include "MinHook.h"
#include "imgui.h"
#include "imgui_impl_dx11.h"
#include "imgui_impl_win32.h"

// Globals
ID3D11Device *g_pd3dDevice = nullptr;
ID3D11DeviceContext *g_pd3dDeviceContext = nullptr;
HWND g_hWnd = nullptr;
bool g_imguiInitialized = false;
bool show_window = false;
std::vector<std::vector<std::string>> api_table_data;
std::mutex api_mutex;

// API fetch function
void FetchAPIData()
{
    std::lock_guard<std::mutex> lock(api_mutex);
    api_table_data.clear();

    HINTERNET hSession = WinHttpOpen(L"GW2Overlay/1.0", WINHTTP_ACCESS_TYPE_DEFAULT_PROXY, NULL, NULL, 0);
    if (hSession)
    {
        HINTERNET hConnect = WinHttpConnect(hSession, L"www.test.com", INTERNET_DEFAULT_HTTP_PORT, 0);
        if (hConnect)
        {
            HINTERNET hRequest = WinHttpOpenRequest(hConnect, L"GET", L"/api", NULL, WINHTTP_NO_REFERER, WINHTTP_DEFAULT_ACCEPT_TYPES, 0);
            if (hRequest)
            {
                if (WinHttpSendRequest(hRequest, WINHTTP_NO_ADDITIONAL_HEADERS, 0, WINHTTP_NO_REQUEST_DATA, 0, 0, 0) &&
                    WinHttpReceiveResponse(hRequest, NULL))
                {
                    DWORD dwSize = 0;
                    WinHttpQueryDataAvailable(hRequest, &dwSize);
                    if (dwSize > 0)
                    {
                        char *buffer = new char[dwSize + 1];
                        ZeroMemory(buffer, dwSize + 1);
                        DWORD dwDownloaded = 0;
                        WinHttpReadData(hRequest, buffer, dwSize, &dwDownloaded);
                        // Parse buffer (assume CSV for demo)
                        std::string response(buffer, dwDownloaded);
                        delete[] buffer;
                        // Example parsing: each line is a row, comma-separated
                        size_t pos = 0;
                        while ((pos = response.find('\n')) != std::string::npos)
                        {
                            std::string line = response.substr(0, pos);
                            response.erase(0, pos + 1);
                            std::vector<std::string> row;
                            size_t cpos = 0;
                            while ((cpos = line.find(',')) != std::string::npos)
                            {
                                row.push_back(line.substr(0, cpos));
                                line.erase(0, cpos + 1);
                            }
                            row.push_back(line);
                            api_table_data.push_back(row);
                        }
                    }
                }
                WinHttpCloseHandle(hRequest);
            }
            WinHttpCloseHandle(hConnect);
        }
        WinHttpCloseHandle(hSession);
    }
}

// ImGui rendering
void RenderImGui()
{
    ImGui::SetNextWindowPos(ImVec2(10, 10), ImGuiCond_Always);
    ImGui::Begin("##icon", nullptr, ImGuiWindowFlags_NoTitleBar | ImGuiWindowFlags_AlwaysAutoResize);
    if (ImGui::Button("API"))
    {
        show_window = !show_window;
        if (show_window)
        {
            std::thread(FetchAPIData).detach();
        }
    }
    ImGui::End();

    if (show_window)
    {
        std::lock_guard<std::mutex> lock(api_mutex);
        ImGui::Begin("API Data");
        if (!api_table_data.empty())
        {
            int cols = api_table_data[0].size();
            if (ImGui::BeginTable("table1", cols))
            {
                for (const auto &row : api_table_data)
                {
                    ImGui::TableNextRow();
                    for (const auto &col : row)
                    {
                        ImGui::TableNextColumn();
                        ImGui::Text("%s", col.c_str());
                    }
                }
                ImGui::EndTable();
            }
        }
        else
        {
            ImGui::Text("No data.");
        }
        ImGui::End();
    }
}

// Hooked Present
typedef HRESULT(__stdcall *Present_t)(IDXGISwapChain *, UINT, UINT);
Present_t oPresent = nullptr;

HRESULT __stdcall hkPresent(IDXGISwapChain *pSwapChain, UINT SyncInterval, UINT Flags)
{
    if (!g_imguiInitialized)
    {
        if (SUCCEEDED(pSwapChain->GetDevice(__uuidof(ID3D11Device), (void **)&g_pd3dDevice)))
        {
            g_pd3dDevice->GetImmediateContext(&g_pd3dDeviceContext);
            DXGI_SWAP_CHAIN_DESC sd;
            pSwapChain->GetDesc(&sd);
            g_hWnd = sd.OutputWindow;
            ImGui::CreateContext();
            ImGui_ImplWin32_Init(g_hWnd);
            ImGui_ImplDX11_Init(g_pd3dDevice, g_pd3dDeviceContext);
            g_imguiInitialized = true;
        }
    }
    if (g_imguiInitialized)
    {
        ImGui_ImplDX11_NewFrame();
        ImGui_ImplWin32_NewFrame();
        ImGui::NewFrame();
        RenderImGui();
        ImGui::EndFrame();
        ImGui::Render();
        ImGui_ImplDX11_RenderDrawData(ImGui::GetDrawData());
    }
    return oPresent(pSwapChain, SyncInterval, Flags);
}

// DLL entry and hook setup
DWORD WINAPI MainThread(LPVOID)
{
    // Initialize MinHook
    MH_Initialize();
    // Find IDXGISwapChain::Present address (use pattern scan or manual)
    // For demo, assume address is found and stored in presentAddr
    void *presentAddr = /* ...find Present address... */;
    MH_CreateHook(presentAddr, &hkPresent, reinterpret_cast<void **>(&oPresent));
    MH_EnableHook(presentAddr);
    return 0;
}

BOOL APIENTRY DllMain(HMODULE hModule, DWORD ul_reason_for_call, LPVOID lpReserved)
{
    if (ul_reason_for_call == DLL_PROCESS_ATTACH)
    {
        DisableThreadLibraryCalls(hModule);
        CreateThread(nullptr, 0, MainThread, nullptr, 0, nullptr);
    }
    return TRUE;
}
