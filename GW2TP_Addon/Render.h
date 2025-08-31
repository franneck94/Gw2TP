#ifndef RENDER_H
#define RENDER_H

#include <string>
#include <map>

#include "imgui.h"

struct Price
{
    int gold = 0;
    int silver = 0;
    int copper = 0;
};

class GW2TPHelper
{
private:
    const std::wstring api_url = L"http://127.0.0.1:8000/api/";

    Price fetchPrice(int item_id);
    bool loaded_prices = false;
    std::map<std::string, Price> prices;

public:
    GW2TPHelper() {};
    ~GW2TPHelper() {};

    void renderPriceTable(const char *label, int item_id);
    void render();
    void render_options();
    bool refresh_prices();
};

#endif // RENDER_H
