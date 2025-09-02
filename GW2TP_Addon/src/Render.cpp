#include <iostream>
#include <list>
#include <map>
#include <ranges>
#include <string>

#include "httpclient/httpclient.h"
#include "imgui.h"

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

    void get_row_data(const std::map<std::string, int> &kv)
    {
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

            const auto gold = name0.ends_with("_g") ? val0 : name1.ends_with("_g") ? val1 : val2;
            const auto silver = name0.ends_with("_s") ? val0 : name1.ends_with("_s") ? val1 : val2;
            const auto copper = name0.ends_with("_c") ? val0 : name1.ends_with("_c") ? val1 : val2;

            const auto transformed_name = get_clean_category_name(name0, true);

            add_row(transformed_name, Price{
                                          .copper = copper,
                                          .silver = silver,
                                          .gold = gold,
                                      });
        }
    }

    void get_row_data_ecto(const std::map<std::string, int> &kv)
    {
        for (size_t i = 0; i < kv.size(); i += 1)
        {
            auto it = std::next(kv.begin(), i);
            auto name = std::next(it, 0)->first;
            const auto val = std::next(it, 0)->second;

            const auto transformed_name = get_clean_category_name(name, true);

            // TODO
            add_row(transformed_name, Price{
                                          .copper = 0,
                                          .silver = 0,
                                          .gold = 0,
                                      });
        }
    }

    void center_next_element(const char *label = "")
    {
        float windowWidth = ImGui::GetWindowSize().x;
        float buttonWidth = ImGui::CalcTextSize(label).x + ImGui::GetStyle().FramePadding.x * 2.0f;
        ImGui::SetCursorPosX((windowWidth - buttonWidth) * 0.5f);
    }
}

void Render::render_table(std::string request_id)
{
    const auto &kv = data.api_data[request_id];
    if (API::COMMANDS_LIST.find(request_id) == API::COMMANDS_LIST.end() || data.api_data.find(request_id) == data.api_data.end() || data.api_data[request_id].empty())
        return;

    ImGuiTableFlags flags = ImGuiTableFlags_Borders | ImGuiTableColumnFlags_NoSort;
    ImGui::SetNextItemWidth(400);
    if (ImGui::BeginTable(("Prices##" + request_id).c_str(), 4, flags))
    {
        add_header(request_id);

        if (API::COMMANDS_LIST.find(request_id) != API::COMMANDS_LIST.end())
        {
            get_row_data(kv);
        }
        else
        {
            assert(false);
        }

        ImGui::EndTable();
    }
}

void Render::render()
{
    if (ImGui::Begin("GW2TP"))
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
            const auto child_size = ImVec2(NAME_COLUMN_WIDTH_PX + 3 * NUMBER_COLUMN_WIDTH_PX + OFFSET_PX, 150.0F);
            ImGui::BeginChild(("tableChild" + std::to_string(idx)).c_str(), child_size, false, ImGuiWindowFlags_AlwaysAutoResize);
            render_table(command);
            ImGui::EndChild();
            if (ImGui::GetWindowSize().x > 1.5f * child_size.x && idx % 2 == 0)
                ImGui::SameLine();
            ++idx;
        }
    }

    ImGui::End();
}
