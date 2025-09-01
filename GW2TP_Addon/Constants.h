#ifndef CONSTANTS_HPP
#define CONSTANTS_HPP

#include <set>
#include <string>

class ItemIDs
{
public:
    // Gear
    static constexpr std::int32_t RARE_UNID_GEAR = 83008;
    static constexpr std::int32_t COMMON_UNID_GEAR = 85016;
    static constexpr std::int32_t UNID_GEAR = 84731;
    static constexpr std::int32_t COMMON_GEAR = 85016;
    // T6 Mats
    static constexpr std::int32_t THICK_LEATHER = 19729;
    static constexpr std::int32_t GOSSAMER_SCRAP = 19745;
    static constexpr std::int32_t SILK_SCRAP = 19748;
    static constexpr std::int32_t HARDENED_LEATHER = 19732;
    static constexpr std::int32_t ANCIENT_WOOD = 19725;
    static constexpr std::int32_t CURED_HARDENED_LEATHER_SQUARE = 19737;
    static constexpr std::int32_t ORICHALCUM = 19701;
    static constexpr std::int32_t ECTOPLASM = 19721;
    static constexpr std::int32_t ELABORATE_TOTEM = 24300;
    static constexpr std::int32_t CRYSTALINE_DUST = 24277;
    // T5 Mats
    static constexpr std::int32_t MITHRIL_INGOT = 19684;
    static constexpr std::int32_t MITHRIL_ORE = 19700;
    static constexpr std::int32_t ELDER_WOOD_PLANK = 19709;
    static constexpr std::int32_t ELDER_WOOD_LOG = 19722;
    static constexpr std::int32_t MIRTHIL = 19700;
    static constexpr std::int32_t ELDER_WOOD = 19722;
    static constexpr std::int32_t LARGE_CLAW = 24350;
    static constexpr std::int32_t POTENT_BLOOD = 24294;
    static constexpr std::int32_t LARGE_BONE = 24341;
    static constexpr std::int32_t INTRICATE_TOTEM = 24299;
    static constexpr std::int32_t LARGE_FANG = 24356;
    static constexpr std::int32_t POTENT_VENOM_SAC = 24282;
    // Other
    static constexpr std::int32_t PILE_OF_LUCENT_CRYSTAL = 89271;
    static constexpr std::int32_t BARBED_THORN = 74202;
    static constexpr std::int32_t LUCENT_MOTE = 89140;
    // Runes
    static constexpr std::int32_t SCHOLAR_RUNE = 24836;
    static constexpr std::int32_t GUARD_RUNE = 24824;
    static constexpr std::int32_t DRAGONHUNTER_RUNE = 74978;
    // Relics
    static constexpr std::int32_t RELIC_OF_FIREWORKS = 100947;
    static constexpr std::int32_t RELIC_OF_ARISTOCRACY = 100849;
    static constexpr std::int32_t RELIC_OF_THIEF = 100916;
    // Charms
    static constexpr std::int32_t SYMBOL_OF_ENH = 89141;
    static constexpr std::int32_t SYMBOL_OF_PAIN = 89182;
    static constexpr std::int32_t SYMBOL_OF_CONTROL = 89098;
    static constexpr std::int32_t CHARM_OF_BRILLIANCE = 89103;
    static constexpr std::int32_t CHARM_OF_POTENCE = 89258;
    static constexpr std::int32_t CHARM_OF_SKILL = 89216;
    // Loadstones
    static constexpr std::int32_t EVERGREEN_LOADSTONE = 68942;
    static constexpr std::int32_t CHARGED_LOADSTONE = 24305;
    static constexpr std::int32_t CORRUPTED_LOADSTONE = 24340;
    static constexpr std::int32_t DESTROYER_LOADSTONE = 24325;
    static constexpr std::int32_t ONYX_LOADSTONE = 24310;
    // Cores
    static constexpr std::int32_t ONYX_CORE = 24309;
    static constexpr std::int32_t DESTROYER_CORE = 24324;
    static constexpr std::int32_t CORRUPTED_CORE = 24339;
    static constexpr std::int32_t CHARGED_CORE = 24304;
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
    static const inline std::string GW2_COMMERCE_API_URL = "https://api.guildwars2.com/v2/commerce/prices";
    static const inline std::string PRODUCTION_API_URL = "https://gw2tp-production.up.railway.app/api";
    static const inline std::string DEV_API_URL = "http://127.0.0.1:8000/api";
    static const inline std::string COMMAND_PREFIX = "/gw2tp";

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
        "t5_mats_sel",
        // forge
        "smybol_enh_forge",
        "loadstone_forge"};
};

#endif // CONSTANTS_HPP
