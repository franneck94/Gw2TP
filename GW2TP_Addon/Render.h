#ifndef RENDER_H
#define RENDER_H

#include <string>

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
    const std::string api_url = "https://gw2tp-production.up.railway.app/api/";

    Price fetchPrice(int item_id);

public:
    GW2TPHelper() {};
    ~GW2TPHelper() {};

    void renderPriceTable(const char *label, int item_id);
    void render();
    void render_options();
    bool refresh_prices();
};

#endif // RENDER_H
