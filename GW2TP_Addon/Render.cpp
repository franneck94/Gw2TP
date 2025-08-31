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

Price GW2TPHelper::fetchPrice(int item_id)
{
    const auto full_url = api_url + L"price?item_id=" + std::to_wstring(item_id);
    auto future = HTTPClient::GetRequestAsync(full_url);
    auto response = future.get();

    try
    {
        json j = json::parse(response);

        // Access some values
        int buy = j["buy"];
        int sell = j["sell"];

        auto [buy_g, buy_s, buy_c] = copper_to_gsc(buy);
        auto [sell_g, sell_s, sell_c] = copper_to_gsc(sell);

        return Price{.gold = buy_g, .silver = buy_s, .copper = buy_c};
    }
    catch (const json::parse_error &e)
    {
        std::cerr << "JSON parse error: " << e.what() << std::endl;
    }
    catch (const json::type_error &e)
    {
        std::cerr << "JSON type error: " << e.what() << std::endl;
    }

    return Price{.gold = -1, .silver = -1, .copper = -1};
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

    renderPriceTable("Ectoplasm", 19721);

    ImGui::End();
}

void _row(const std::string name, const Price &price)
{
    ImGui::TableNextRow();
    ImGui::TableNextColumn();
    ImGui::Text(name.c_str());
    ImGui::TableNextColumn();
    ImGui::Text("%d", price.gold);
    ImGui::TableNextColumn();
    ImGui::Text("%d", price.silver);
    ImGui::TableNextColumn();
    ImGui::Text("%d", price.copper);
}

void GW2TPHelper::renderPriceTable(const char *label, int item_id)
{
    static bool first_load = true;
    static Price price;

    if (first_load)
    {
        first_load = false;
        price = GW2TPHelper::fetchPrice(item_id);
    }

    if (ImGui::BeginTable(label, 4, ImGuiTableFlags_Borders))
    {
        ImGui::TableSetupColumn(std::to_string(item_id).c_str());
        ImGui::TableSetupColumn("Gold");
        ImGui::TableSetupColumn("Silver");
        ImGui::TableSetupColumn("Copper");
        ImGui::TableHeadersRow();

        _row("Buy", price);
        _row("Sell", price);
        _row("Flip", price);

        ImGui::EndTable();
    }
}

bool GW2TPHelper::refresh_prices()
{
    return true;
}
