#pragma once

#include <string>

#include "Data.h"

class Render
{
public:
    constexpr static auto NAME_COLUMN_WIDTH_PX = 140.0F;
    constexpr static auto NUMBER_COLUMN_WIDTH_PX = 25.0F;

    Data data;

    void render();

private:
    void render_table(std::string request_id);
};
