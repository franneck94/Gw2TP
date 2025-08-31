#ifndef RENDER_H
#define RENDER_H

#include <map>
#include <string>
#include <tuple>
#include <utility>
#include <vector>

#include "imgui.h"
#include "nlohmann/json.hpp"

#include "Constants.h"
#include "Types.h"

using json = nlohmann::json;

class GW2TPHelper
{
private:
    const std::wstring api_url = API::DEV_API_URL;

    bool loaded_prices = false;
    std::map<std::wstring, std::vector<std::pair<std::string, json>>> fetched_kv;

    std::vector<std::pair<std::string, json>> fetch_item_id_price(int item_id);
    std::vector<std::pair<std::string, json>> fetch_command(const std::wstring &command);

public:
    GW2TPHelper() {};
    ~GW2TPHelper() {};

    void render_table(const std::wstring item_id);
    void render();
    void render_options();
    bool refresh_prices();
};

#endif // RENDER_H
