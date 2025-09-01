#pragma once

#include <future>
#include <list>
#include <map>
#include <set>
#include <string>

struct Price
{
    int copper;
    int silver;
    int gold;
};

struct PriceTriplet
{
    Price buy;
    Price sell;
    Price profit;
};

constexpr static auto NAME_COLUMN_WIDTH_PX = 140.0F;
constexpr static auto NUMBER_COLUMN_WIDTH_PX = 25.0F;

struct Request
{
    std::string request_id;
    std::future<std::string> future;

    Request(Request &&other) noexcept
        : request_id(std::move(other.request_id)),
          future(std::move(other.future))
    {
    }

    Request(std::string &&request_id, std::future<std::string> &&future) noexcept
        : request_id(std::move(request_id)),
          future(std::move(future))
    {
    }

    Request(const Request &) = delete;
    Request() = delete;
};

class Render
{
public:
    void requesting();
    void storing();
    void render();
    void render_table(std::string request_id);

    bool requested = false;
    bool loaded = false;

    std::string url = "https://en.wikipedia.org/api/rest_v1/page/summary/Albert_Einstein";
    std::list<Request> futures;
    std::map<std::string, std::map<std::string, int>> api_data;
};
