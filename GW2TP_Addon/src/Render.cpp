#include <iostream>
#include <list>
#include <map>
#include <ranges>
#include <string>

#include "httpclient/httpclient.h"
#include "imgui.h"

#include "API.h"
#include "Constants.h"
#include "Data.h"
#include "Render.h"

namespace
{
    std::string get_clean_category_name(const std::string &input, const bool skip_last_two)
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

        if (skip_last_two)
            return {view.begin(), view.end() - 2};
        else
            return {view.begin(), view.end()};
    }

    void remove_substring(std::string &str, const std::string &sub)
    {
        size_t pos;
        while ((pos = str.find(sub)) != std::string::npos)
        {
            str.erase(pos, sub.size());
        }
    }

    void add_row(const std::string name, const Price &price)
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

    void add_header(const std::string name)
    {
        const auto transformed_name = get_clean_category_name(name, false);

        ImGui::TableSetupColumn(transformed_name.c_str(), ImGuiTableColumnFlags_WidthFixed, Render::NAME_COLUMN_WIDTH_PX);
        ImGui::TableSetupColumn("G", ImGuiTableColumnFlags_WidthFixed, Render::NUMBER_COLUMN_WIDTH_PX);
        ImGui::TableSetupColumn("S", ImGuiTableColumnFlags_WidthFixed, Render::NUMBER_COLUMN_WIDTH_PX);
        ImGui::TableSetupColumn("C", ImGuiTableColumnFlags_WidthFixed, Render::NUMBER_COLUMN_WIDTH_PX);
        ImGui::TableHeadersRow();
    }

    template <size_t N>
    void _get_ordered_row_data(const std::array<const char *, N> &keys, const std::vector<std::pair<std::string, Price>> &rows)
    {
        for (const auto &key : keys)
        {
            auto it = std::find_if(rows.begin(), rows.end(), [&key](const auto &pair)
                                   { return pair.first == key; });
            if (it != rows.end())
            {
                const auto name = get_clean_category_name(it->first, false);
                const auto price = it->second;

                add_row(name, price);
            }
            else
            {
                assert(false);
            }
        }
    }

    void get_row_data(const std::map<std::string, int> &kv, const std::string &request_id)
    {
        auto rows = std::vector<std::pair<std::string, Price>>{};

        for (size_t i = 0; i < kv.size() - 2; i += 3)
        {
            auto it = std::next(kv.begin(), i);

            if (it->first.find("_g") == std::string::npos && it->first.find("_s") == std::string::npos && it->first.find("_c") == std::string::npos)
            {
                ++i;
                ++it;
            }

            auto name0 = std::next(it, 0)->first;
            auto name1 = std::next(it, 1)->first;
            auto name2 = std::next(it, 2)->first;

            const auto val0 = std::next(it, 0)->second;
            const auto val1 = std::next(it, 1)->second;
            const auto val2 = std::next(it, 2)->second;

            const auto gold = name0.ends_with("_g") ? val0 : name1.ends_with("_g") ? val1
                                                                                   : val2;
            const auto silver = name0.ends_with("_s") ? val0 : name1.ends_with("_s") ? val1
                                                                                     : val2;
            const auto copper = name0.ends_with("_c") ? val0 : name1.ends_with("_c") ? val1
                                                                                     : val2;

            const auto transformed_name = std::string{name0.substr(0, name0.size() - 2)};

            rows.emplace_back(transformed_name, Price{
                                                    .copper = copper,
                                                    .silver = silver,
                                                    .gold = gold,
                                                });
        }

        // runes
        if (request_id == "scholar_rune")
        {
            _get_ordered_row_data(API::SCHOLAR_RUNE_NAMES, rows);
        }
        else if (request_id == "dragonhunter_rune")
        {
            _get_ordered_row_data(API::DRAGONHUNTER_RUNE_NAMES, rows);
        }
        else if (request_id == "guardian_rune")
        {
            _get_ordered_row_data(API::GUARDIAN_RUNE_NAMES, rows);
        }
        // relics
        else if (request_id == "relic_of_fireworks")
        {
            _get_ordered_row_data(API::FIREWORKS_NAMES, rows);
        }
        else if (request_id == "relic_of_thief")
        {
            _get_ordered_row_data(API::THIEF_NAMES, rows);
        }
        else if (request_id == "relic_of_aristocracy")
        {
            _get_ordered_row_data(API::ARISTOCRACY_NAMES, rows);
        }
        // gear
        if (request_id == "rare_weapon_craft")
        {
            _get_ordered_row_data(API::RARE_WEAPON_CRAFT_NAMES, rows);
        }
        else if (request_id == "rare_gear_salvage")
        {
            _get_ordered_row_data(API::RARE_GEAR_NAMES, rows);
        }
        else if (request_id == "ecto")
        {
            for (const auto &[name, price] : rows)
            {
                add_row(name, price);
            }
        }
        // gear
        else if (request_id == "gear_salvage")
        {
            _get_ordered_row_data(API::GEAR_SALVAGE_NAMES, rows);
        }
        else if (request_id == "common_gear_salvage")
        {
            _get_ordered_row_data(API::COMMON_GEAR_NAMES, rows);
        }
        // t5
        else if (request_id == "t5_mats_buy")
        {
            _get_ordered_row_data(API::MATS_CRAFT_COMPARE_NAMES, rows);
        }
        else if (request_id == "t5_mats_sell")
        {
            // TODO
        }
        // forge
        else if (request_id == "smybol_enh_forge")
        {
            _get_ordered_row_data(API::FORGE_ENH_NAMES, rows);
        }
        else if (request_id == "loadstone_forge")
        {
            _get_ordered_row_data(API::LOADSTONE_NAMES, rows);
        }
        else
        {
            int i = 2;
        }
    }

    void center_next_element(const char *label = "")
    {
        float windowWidth = ImGui::GetWindowSize().x;
        float buttonWidth = ImGui::CalcTextSize(label).x + ImGui::GetStyle().FramePadding.x * 2.0f;
        ImGui::SetCursorPosX((windowWidth - buttonWidth) * 0.5f);
    }
}

int Render::render_table(const std::string &request_id)
{
    const auto &kv = data.api_data[request_id];
    if (API::COMMANDS_LIST.find(request_id) == API::COMMANDS_LIST.end() || data.api_data.find(request_id) == data.api_data.end() || data.api_data[request_id].empty())
        return -1;

    ImGuiTableFlags flags = ImGuiTableFlags_Borders | ImGuiTableColumnFlags_NoSort;
    ImGui::SetNextItemWidth(ImGui::GetWindowContentRegionWidth() * 0.5f);
    if (ImGui::BeginTable(("Prices##" + request_id).c_str(), 4, flags))
    {
        add_header(request_id);

        if (API::COMMANDS_LIST.find(request_id) != API::COMMANDS_LIST.end())
        {
            get_row_data(kv, request_id);
        }
        else
        {
            assert(false);
        }

        ImGui::EndTable();
    }

    return static_cast<int>(ImGui::GetCursorPosY());
}

void Render::render()
{
    if (!show_window)
        return;

    if (ImGui::Begin("GW2TP", &show_window))
    {
        auto *btn_label = "Refresh Data";
        center_next_element(btn_label);

        if (ImGui::Button(btn_label))
        {
            data.loaded = false;
            data.requested = false;
            data.api_data.clear();
            data.futures.clear();

            data.requesting();
        }

        if (!data.loaded)
        {
            auto *text_label = "Loading...";
            center_next_element(text_label);
            ImGui::Text(text_label);
            ImGui::End();

            return;
        }

        auto idx = 0U;
        for (const auto command : API::COMMANDS_LIST)
        {
            const auto child_size = ImVec2(ImGui::GetWindowContentRegionWidth() * 0.5f, 150.0F);
            ImGui::BeginChild(("tableChild" + std::to_string(idx)).c_str(), child_size, false, ImGuiWindowFlags_AlwaysAutoResize);
            const auto table_height = render_table(command);
            ImGui::EndChild();
            if ((ImGui::GetWindowSize().x > 400.0F) && (idx % 2 == 0))
                ImGui::SameLine();
            else
                ImGui::SetCursorPosY(ImGui::GetCursorPosY() + table_height - 150.0F);
            ++idx;
        }
    }

    ImGui::End();
}
