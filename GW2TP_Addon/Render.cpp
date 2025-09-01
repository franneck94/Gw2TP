#include <Windows.h>
#include <chrono>
#include <future>
#include <iostream>
#include <list>
#include <map>
#include <string>
#include <vector>

#include "imgui.h"
#include "nlohmann/json.hpp"

#include "httpclient/httpclient.h"

#include "Constants.h"
#include "Render.h"

using json = nlohmann::json;

static std::string get_clean_category_name(const std::string &input)
{
    auto view = input | std::views::transform(
                            [newWord = true](char c) mutable
                            {
                                if (c == '_')
                                {
                                    newWord = true;
                                    return ' ';
                                }
                                if (newWord)
                                {
                                    newWord = false;
                                    return static_cast<char>(std::toupper(static_cast<unsigned char>(c)));
                                }
                                return static_cast<char>(std::tolower(static_cast<unsigned char>(c)));
                            });

    return {view.begin(), view.end()};
}

static void remove_substring(std::string &str, const std::string &sub)
{
    size_t pos;
    while ((pos = str.find(sub)) != std::string::npos)
    {
        str.erase(pos, sub.size());
    }
}

static std::map<std::string, int> _collect_json(const json &jval, const std::string &prefix)
{
    std::map<std::string, int> kv;

    if (jval.is_object())
    {
        for (auto it = jval.begin(); it != jval.end(); ++it)
        {
            auto _kv = _collect_json(it.value(), prefix.empty() ? it.key() : prefix + "." + it.key());
            for (const auto &[k, v] : _kv)
                kv[k] = v;
        }
    }
    else if (jval.is_array())
    {
        for (size_t i = 0; i < jval.size(); ++i)
        {
            auto _kv = _collect_json(jval[i], prefix + "[" + std::to_string(i) + "]");
            for (const auto &[k, v] : _kv)
                kv[k] = v;
        }
    }
    else
    {
        if (jval.is_number_integer())
        {
            kv[prefix] = static_cast<int>(jval);
        }
    }

    return kv;
}

static void _row(const std::string name, const Price &price)
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

static void _head(const std::string name)
{
    const auto transformed_name = get_clean_category_name(name);

    ImGui::TableSetupColumn(transformed_name.c_str(), ImGuiTableColumnFlags_WidthFixed, NAME_COLUMN_WIDTH_PX);
    ImGui::TableSetupColumn("Gold", ImGuiTableColumnFlags_WidthFixed, NUMBER_COLUMN_WIDTH_PX);
    ImGui::TableSetupColumn("Silver", ImGuiTableColumnFlags_WidthFixed, NUMBER_COLUMN_WIDTH_PX);
    ImGui::TableSetupColumn("Copper", ImGuiTableColumnFlags_WidthFixed, NUMBER_COLUMN_WIDTH_PX);
    ImGui::TableHeadersRow();
}

static void _get_row_data(const std::map<std::string, int> &kv)
{
    for (size_t i = 0; i < kv.size(); i += 3)
    {
        auto it = std::next(kv.begin(), i);
        auto name = it->first;
        remove_substring(name, "_c");
        const auto transformed_name = get_clean_category_name(name);
        const auto gold = std::next(it, 0)->second;
        const auto silver = std::next(it, 1)->second;
        const auto copper = std::next(it, 2)->second;
        _row(transformed_name, Price{gold, silver, copper});
    }
}

void Render::render_table(std::string request_id)
{
    const auto &kv = api_data[request_id];
    if (API::COMMANDS_LIST.find(request_id) == API::COMMANDS_LIST.end() || api_data.find(request_id) == api_data.end() || api_data[request_id].empty())
        return;

    ImGuiTableFlags flags = ImGuiTableFlags_Borders | ImGuiTableColumnFlags_NoSort;
    ImGui::SetNextItemWidth(400);
    if (ImGui::BeginTable(("Prices##" + request_id).c_str(), 4, flags))
    {
        _head(request_id);

        if (
            request_id == "scholar_rune" ||
            request_id == "dragonhunter_rune" ||
            request_id == "guardian_rune" ||
            request_id == "relic_of_fireworks" ||
            request_id == "relic_of_aristocracy" ||
            request_id == "relic_of_thief" ||
            request_id == "rare_weapon_craft" ||
            request_id == "rare_gear_salvage" ||
            request_id == "ecto" ||
            request_id == "gear_salvage" ||
            request_id == "common_gear_salvage" ||
            request_id == "t5_mats_buy" ||
            request_id == "t5_mats_sel" ||
            request_id == "profits" ||
            request_id == "get_price" ||
            request_id == "smybol_enh_forge" ||
            request_id == "loadstone_forge" ||
            request_id == "thumbnail.height")
        {
            if (kv.size() % 3 == 0)
                _get_row_data(kv);
        }
        else
        {
            assert(false);
        }

        ImGui::EndTable();
    }
}

void Render::requesting()
{
    if (!requested)
    {
        std::wcout << "Requesting data from API...\n";
        futures.clear();

        for (auto command : API::COMMANDS_LIST)
        {
            const auto wstr_url = std::wstring(API::PRODUCTION_API_URL.begin(), API::PRODUCTION_API_URL.end()) + L"/" + std::wstring(command.begin(), command.end());
            auto future = HTTPClient::GetRequestAsync(wstr_url);
            auto req = Request(std::move(command), std::move(future));
            futures.push_back(std::move(req));
        }

        requested = true;
        api_data.clear();
    }
}

void Render::storing()
{
    if (futures.size() == 0)
        loaded = true;
    else
        loaded = false;

    auto it = futures.begin();

    while (it != futures.end())
    {
        if (it->future.wait_for(std::chrono::seconds(0)) == std::future_status::ready)
        {
            const auto request_id = it->request_id;
            const auto request = it->future.get();
            auto j = json::parse(request);

            auto kv = _collect_json(j, "");

            api_data[request_id] = kv;
            it = futures.erase(it);
            return; /* return early in this frame */
        }

        ++it;
    }
}

void Render::render()
{
    if (ImGui::Begin("mainWWindow"))
    {
        const char *label = "Refresh Data";
        float windowWidth = ImGui::GetWindowSize().x;
        float buttonWidth = ImGui::CalcTextSize(label).x + ImGui::GetStyle().FramePadding.x * 2.0f;
        ImGui::SetCursorPosX((windowWidth - buttonWidth) * 0.5f);

        if (ImGui::Button(label))
        {
            loaded = false;
            requested = false;
            api_data.clear();
            futures.clear();
            requesting();
        }

        if (!loaded)
        {
            ImGui::Text("Loading...");
            ImGui::End();

            return;
        }

        auto idx = 0U;
        for (const auto command : API::COMMANDS_LIST)
        {
            const auto child_size = ImVec2(NAME_COLUMN_WIDTH_PX + 3 * NUMBER_COLUMN_WIDTH_PX + 100.0F, 100);
            ImGui::BeginChild(("tableChild" + std::to_string(idx)).c_str(), child_size, false, ImGuiWindowFlags_AlwaysAutoResize);
            render_table(command);
            ImGui::EndChild();
            if (idx % 2 == 0)
                ImGui::SameLine();
            ++idx;
        }
    }

    ImGui::End();
}
