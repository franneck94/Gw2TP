#include <cstdint>

typedef struct Price
{
    std::int32_t gold = 0;
    std::int32_t silver = 0;
    std::int32_t copper = 0;
} Price;

typedef struct PriceTriplet
{
    Price buy;
    Price sell;
    Price flip;
} PriceTriplet;
