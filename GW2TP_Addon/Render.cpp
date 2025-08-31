#include <iostream>
#include <string>

#include <DirectXMath.h>
#include <Windows.h>

#include "httpclient/httpclient.h"
#include "imgui.h"
#include "imgui_extensions.h"
#include "mumble/Mumble.h"
#include "nexus/Nexus.h"
#include "nlohmann/json.hpp"
#include "rtapi/RTAPI.hpp"

#include "Render.h"
#include "Shared.h"

using json = nlohmann::json;

static std::tuple<int, int, int> copper_to_gsc(int copper)
{
    bool negative = copper < 0;
    int abs_copper = std::abs(copper);

    int gold = abs_copper / 10'000;
    int silver = (abs_copper % 10'000) / 100;
    int rest = abs_copper % 100;

    if (negative)
    {
        gold = -gold;
        silver = -silver;
        rest = -rest;
    }

    return {gold, silver, rest};
}

static json _parse_json(const std::string &response)
{
    try
    {
        json j = json::parse(response);

        return j;
    }
    catch (const json::parse_error &e)
    {
        std::cerr << "JSON parse error: " << e.what() << std::endl;
    }
    catch (const json::type_error &e)
    {
        std::cerr << "JSON type error: " << e.what() << std::endl;
    }

    return json{};
}

static void _head(const char *name)
{
    ImGui::TableSetupColumn(name);
    ImGui::TableSetupColumn("Gold");
    ImGui::TableSetupColumn("Silver");
    ImGui::TableSetupColumn("Copper");
    ImGui::TableHeadersRow();
}

static void _row(const char *name, const Price &price)
{
    ImGui::TableNextRow();
    ImGui::TableNextColumn();
    ImGui::Text(name);
    ImGui::TableNextColumn();
    ImGui::Text("%d", price.gold);
    ImGui::TableNextColumn();
    ImGui::Text("%d", price.silver);
    ImGui::TableNextColumn();
    ImGui::Text("%d", price.copper);
}

static std::string _wstring_to_string(const std::wstring &wstr)
{
    int size_needed = WideCharToMultiByte(CP_UTF8, 0, &wstr[0],
                                          (int)wstr.size(), NULL, 0, NULL, NULL);
    std::string str(size_needed, 0);
    WideCharToMultiByte(CP_UTF8, 0, &wstr[0], (int)wstr.size(),
                        &str[0], size_needed, NULL, NULL);
    return str;
}

std::vector<std::pair<std::string, json>> GW2TPHelper::fetch_item_id_price(int item_id)
{
    const auto full_url = api_url + L"price?item_id=" + std::to_wstring(item_id);
    auto future = HTTPClient::GetRequestAsync(full_url);
    auto response = future.get();
    auto j = _parse_json(response);

    std::vector<std::pair<std::string, json>> kv_pairs;

    for (auto &el : j.items())
    {
        kv_pairs.emplace_back(el.key(), el.value());
    }

    return kv_pairs;
}

std::vector<std::pair<std::string, json>> GW2TPHelper::fetch_command(const std::wstring &command)
{
    const auto full_url = api_url + command;
    auto future = HTTPClient::GetRequestAsync(full_url);
    auto response = future.get();
    auto j = _parse_json(response);

    std::vector<std::pair<std::string, json>> kv_pairs;

    for (auto &el : j.items())
    {
        kv_pairs.emplace_back(el.key(), el.value());
    }

    return kv_pairs;
}

void GW2TPHelper::render_options()
{
    ImGui::Begin("GW2 Trading Post Helper Options");

    ImGui::End();
}

void GW2TPHelper::render()
{
    ImGui::Begin("GW2 Trading Post Helper");

    if (ImGui::Button("Refresh Prices"))
    {
        GW2TPHelper::refresh_prices();
    }

    for (const auto command : API::COMMANDS_LIST)
    {
        render_table(command);
    }

    ImGui::End();
}

void GW2TPHelper::render_table(const std::wstring item_id)
{
    const auto label_ = _wstring_to_string(item_id);

    if (ImGui::BeginTable(label_.c_str(), 4, ImGuiTableFlags_Borders))
    {
        _head(label_.c_str());
        const auto curr_fetched_kv = fetched_kv.find(item_id);
        if (curr_fetched_kv != fetched_kv.end())
        {
            for (const auto &[key, value] : curr_fetched_kv->second)
            {
                int _value = -1;
                // value.get<int>();
                Price price;
                price.copper = _value;
                price.silver = _value;
                price.gold = _value;
                _row(key.c_str(), price);
            }
        }

        ImGui::EndTable();
    }
}

bool GW2TPHelper::refresh_prices()
{
    if (!loaded_prices)
    {
        loaded_prices = true;
        fetched_kv.clear();

        for (const auto command : API::COMMANDS_LIST)
        {
            auto curr_fetched_kv = GW2TPHelper::fetch_command(command);
            fetched_kv[command] = curr_fetched_kv;
        }
    }

    return loaded_prices;
}
