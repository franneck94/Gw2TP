#define CPPHTTPLIB_OPENSSL_SUPPORT
#include <iostream>
#include <string>

#include <DirectXMath.h>
#include <Windows.h>

// #include "cpr/cpr.h"
#include "imgui.h"
#include "imgui_extensions.h"
#include "mumble/Mumble.h"
#include "nexus/Nexus.h"
#include "rtapi/RTAPI.hpp"

#include "Render.h"
#include "Shared.h"

Price GW2TPHelper::fetchPrice(int item_id)
{
    // auto r = cpr::Get(cpr::Url{GW2TPHelper::api_url + "/api/price?item_id=83008"});
    // std::cout << r.status_code << "\n"
    //           << r.text << std::endl;

    return Price{};
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
    if (ImGui::BeginTable(label, 4, ImGuiTableFlags_Borders))
    {
        ImGui::TableSetupColumn(std::to_string(item_id).c_str());
        ImGui::TableSetupColumn("Gold");
        ImGui::TableSetupColumn("Silver");
        ImGui::TableSetupColumn("Copper");
        ImGui::TableHeadersRow();

        Price price = GW2TPHelper::fetchPrice(item_id);
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
