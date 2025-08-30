#ifndef CONSTANTS_HPP
#define CONSTANTS_HPP

#include <set>
#include <string>

class ItemIDs
{
public:
    // Gear
    static constexpr int RARE_UNID_GEAR = 83008;
    static constexpr int COMMON_UNID_GEAR = 85016;
    static constexpr int UNID_GEAR = 84731;
    static constexpr int COMMON_GEAR = 85016;
    // T6 Mats
    static constexpr int THICK_LEATHER = 19729;
    static constexpr int GOSSAMER_SCRAP = 19745;
    static constexpr int SILK_SCRAP = 19748;
    static constexpr int HARDENED_LEATHER = 19732;
    static constexpr int ANCIENT_WOOD = 19725;
    static constexpr int CURED_HARDENED_LEATHER_SQUARE = 19737;
    static constexpr int ORICHALCUM = 19701;
    static constexpr int ECTOPLASM = 19721;
    static constexpr int ELABORATE_TOTEM = 24300;
    static constexpr int CRYSTALINE_DUST = 24277;
    // T5 Mats
    static constexpr int MITHRIL_INGOT = 19684;
    static constexpr int MITHRIL_ORE = 19700;
    static constexpr int ELDER_WOOD_PLANK = 19709;
    static constexpr int ELDER_WOOD_LOG = 19722;
    static constexpr int MIRTHIL = 19700;
    static constexpr int ELDER_WOOD = 19722;
    static constexpr int LARGE_CLAW = 24350;
    static constexpr int POTENT_BLOOD = 24294;
    static constexpr int LARGE_BONE = 24341;
    static constexpr int INTRICATE_TOTEM = 24299;
    static constexpr int LARGE_FANG = 24356;
    static constexpr int POTENT_VENOM_SAC = 24282;
    // Other
    static constexpr int PILE_OF_LUCENT_CRYSTAL = 89271;
    static constexpr int BARBED_THORN = 74202;
    static constexpr int LUCENT_MOTE = 89140;
    // Runes
    static constexpr int SCHOLAR_RUNE = 24836;
    static constexpr int GUARD_RUNE = 24824;
    static constexpr int DRAGONHUNTER_RUNE = 74978;
    // Relics
    static constexpr int RELIC_OF_FIREWORKS = 100947;
    static constexpr int RELIC_OF_ARISTOCRACY = 100849;
    static constexpr int RELIC_OF_THIEF = 100916;
    // Charms
    static constexpr int SYMBOL_OF_ENH = 89141;
    static constexpr int SYMBOL_OF_PAIN = 89182;
    static constexpr int SYMBOL_OF_CONTROL = 89098;
    static constexpr int CHARM_OF_BRILLIANCE = 89103;
    static constexpr int CHARM_OF_POTENCE = 89258;
    static constexpr int CHARM_OF_SKILL = 89216;
    // Loadstones
    static constexpr int EVERGREEN_LOADSTONE = 68942;
    static constexpr int CHARGED_LOADSTONE = 24305;
    static constexpr int CORRUPTED_LOADSTONE = 24340;
    static constexpr int DESTROYER_LOADSTONE = 24325;
    static constexpr int ONYX_LOADSTONE = 24310;
    // Cores
    static constexpr int ONYX_CORE = 24309;
    static constexpr int DESTROYER_CORE = 24324;
    static constexpr int CORRUPTED_CORE = 24339;
    static constexpr int CHARGED_CORE = 24304;
};

class Kits
{
public:
    static constexpr float COPPER_FED = 3.0f;
    static constexpr float RUNECRAFTER = 30.0f;
    static constexpr float SILVER_FED = 60.0f;
};

static constexpr float TAX_RATE = 0.85f;

class API
{
public:
    static constexpr const char *GW2_COMMERCE_API_URL = "https://api.guildwars2.com/v2/commerce/prices";
    static constexpr const char *PRODUCTION_API_URL = "https://gw2tp-production.up.railway.app/api/";
    static constexpr const char *DEV_API_URL = "http://127.0.0.1:8000/api/";
    static constexpr const char *COMMAND_PREFIX = "/gw2tp";

    static const inline std::set<std::string> COMMANDS_LIST = {
        // runes
        "scholar_rune",
        "dragonhunter_rune",
        "guardian_rune",
        // relics
        "relic_of_fireworks",
        "relic_of_aristocracy",
        "relic_of_thief",
        // rare / ecto
        "rare_weapon_craft",
        "rare_gear_salvage",
        "ecto",
        // gear
        "gear_salvage",
        "common_gear_salvage",
        // t5
        "t5_mats_buy",
        "t5_mats_sell",
        // general
        "profits",
        "get_price",
        // forge
        "smybol_enh_forge",
        "loadstone_forge"};
};

#endif // CONSTANTS_HPP
