# ruff: noqa: E501
from pathlib import Path

from items import ItemIDs


CWD = Path.cwd()

TABLE_HEADER = """
<tr>
    <th></th>
    <th>Gold</th>
    <th>Silver</th>
    <th>Copper</th>
</tr>
"""


def get_table_header_html(hidden_name: str = "") -> str:
    if hidden_name:
        style = 'style="cursor: pointer; color: transparent; text-shadow: 0 0 8px rgba(0,0,0,0.5);"'
        onclick = f'onclick="navigator.clipboard.writeText(\'{hidden_name}\')" title="Click to copy"'
        first_row = f"<th {style} {onclick}>{hidden_name}</th>"
    else:
        first_row = "<th></th>"
    return f"""
<tr>
    {first_row}
    <th>Gold</th>
    <th>Silver</th>
    <th>Copper</th>
</tr>
"""


def get_price_row_html(
    item_id: str,
    name: str,
    /,
    clipboard_copy: bool = False,  # noqa: FBT001, FBT002
) -> str:
    words = [word.capitalize() for word in item_id.split("_")]
    row_content = " ".join(words)
    if clipboard_copy:
        first_col = f"""
    <td onclick="navigator.clipboard.writeText('{row_content}')" style="cursor: pointer;" title="Click to copy">{row_content}</td>
"""
    else:
        first_col = f"<td>{row_content}</td>"
    return f"""
<tr>
    {first_col}
    <td id="{item_id}_g##{name}">-</td>
    <td id="{item_id}_s##{name}">-</td>
    <td id="{item_id}_c##{name}">-</td>
</tr>"""


def get_price_rows_html(
    price_names: list[str],
    category_name: str,
    /,
    clipboard_copy: bool = False,  # noqa: FBT001, FBT002
) -> str:
    rows_str = ""
    for price_name in price_names:
        rows_str += get_price_row_html(
            price_name,
            category_name,
            clipboard_copy=clipboard_copy,
        )
    return rows_str


def get_flip_table_html(item_id: int) -> str:
    return f"""<table>
        {get_table_header_html()}
        <tr>
            <td>Buy Order</td>
            <td id="{item_id}_buy_g">-</td>
            <td id="{item_id}_buy_s">-</td>
            <td id="{item_id}_buy_c">-</td>
        </tr>
        <tr>
            <td>Sell Order</td>
            <td id="{item_id}_sell_g">-</td>
            <td id="{item_id}_sell_s">-</td>
            <td id="{item_id}_sell_c">-</td>
        </tr>
        <tr>
            <td>Flip Profit</td>
            <td id="{item_id}_flip_g">-</td>
            <td id="{item_id}_flip_s">-</td>
            <td id="{item_id}_flip_c">-</td>
        </tr>
    </table>"""


ECTO_TABLE = get_flip_table_html(ItemIDs.ECTOPLASM)
RARE_GEAR_TABLE = get_flip_table_html(ItemIDs.RARE_UNID_GEAR)

RARE_GEAR_NAMES = [
    "stack_buy",
    "salvage_costs",
    "mats_value_after_tax",
    "profit_stack",
]
RARE_GEAR_SALVAGE = f"""
<table>
    {get_table_header_html(hidden_name="Rare Gear")}
    {get_price_rows_html(RARE_GEAR_NAMES, "rare_gear_salvage")}
</table>
"""

GEAR_SALVAGE_NAMES = [
    "stack_buy",
    "salvage_costs",
    "mats_value_after_tax",
    "profit_stack",
]
GEAR_SALVAGE_TABLE = f"""
<table>
    {get_table_header_html(hidden_name="Unidentified Gear")}
    {get_price_rows_html(GEAR_SALVAGE_NAMES, "gear_salvage")}
</table>
"""

T5_MATS_SELL_NAMES = [
    "lucent_mote",
    "mithril_ore",
    "elder_wood_log",
    "thick_leather",
]
T5_MATS_SELL_TABLE = f"""
<table>
    {get_table_header_html()}
    {get_price_rows_html(T5_MATS_SELL_NAMES, "t5_mats_sell", clipboard_copy=True)}
</table>
"""

T5_MATS_BUY_NAMES = [
    "large_claw",
    "potent_blood",
    "large_bone",
    "intricate_totem",
    "large_fang",
    "potent_venom",
]
T5_MATS_BUY_TABLE = f"""
<table>
    {TABLE_HEADER}
    {get_price_rows_html(T5_MATS_BUY_NAMES, "t5_mats_buy", clipboard_copy=True)}
</table>
"""

MATS_CRAFT_COMPARE_NAMES = [
    "mithril_ore_to_ingot",
    "mithril_ingot_buy",
    "elder_wood_log_to_plank",
    "elder_wood_plank_buy",
    "lucent_mote_to_crystal",
    "lucent_crystal_buy",
]
MATS_CRAFT_COMPARE_TABLE = f"""
<table>
    {TABLE_HEADER}
    {get_price_rows_html(MATS_CRAFT_COMPARE_NAMES, "mats_crafting_compare")}
</table>
"""

COMMON_GEAR_NAMES = [
    "stack_buy",
    "salvage_costs",
    "mats_value_after_tax",
    "profit_stack",
]
COMMON_GEAR_SALVAGE_TABLE = f"""
<table>
    {get_table_header_html(hidden_name="Common Gear")}
    {get_price_rows_html(COMMON_GEAR_NAMES, "common_gear_salvage")}
</table>
"""

LOADSTONE_NAMES = [
    "onyx",
    "charged",
    "corrupted",
    "destroyer",
]
LOADSTONE_TABLE = f"""
<table>
    {TABLE_HEADER}
    {get_price_rows_html(LOADSTONE_NAMES, "loadstone_forge", clipboard_copy=True)}
</table>
"""

SCHOLAR_RUNE_NAMES = [
    "crafting_cost",
    "sell",
    "profit",
]
SCHOLAR_RUNE_TABLE = f"""
<table>
    {get_table_header_html(hidden_name="Scholar Rune")}
    {get_price_rows_html(SCHOLAR_RUNE_NAMES, "scholar_rune")}
</table>
"""

GUARDIAN_RUNE_NAMES = [
    "crafting_cost",
    "sell",
    "profit",
]
GUARDIAN_RUNE_TABLE = f"""
<table>
    {get_table_header_html(hidden_name="Guardian Rune")}
    {get_price_rows_html(GUARDIAN_RUNE_NAMES, "guardian_rune")}
</table>
"""

DRAGONHUNTER_RUNE_NAMES = [
    "crafting_cost",
    "sell",
    "profit",
]
DRAGONHUNTER_RUNE_TABLE = f"""
<table>
    {get_table_header_html(hidden_name="Dragonhunter Rune")}
    {get_price_rows_html(DRAGONHUNTER_RUNE_NAMES, "dragonhunter_rune")}
</table>
"""

FIREWORKS_NAMES = [
    "crafting_cost",
    "sell",
    "flip",
    "profit",
]
FIREWORKS_TABLE = f"""
<table>
    {get_table_header_html(hidden_name="Relic of Fireworks")}
    {get_price_rows_html(FIREWORKS_NAMES, "relic_of_fireworks")}
</table>
"""

RARE_WEAPON_CRAFT_NAMES = [
    "crafting_cost",
    "ecto_sell_after_tax",
    "profit",
]
RARE_WEAPON_CRAFT_TABLE = f"""
<table>
    {get_table_header_html()}
    {get_price_rows_html(RARE_WEAPON_CRAFT_NAMES, "rare_weapon_craft")}
</table>
"""

FORGE_ENH_NAMES = [
    "cost",
    "profit_per_try",
    "profit_per_shard",
]
FORGE_ENH_TABLE = f"""
<table>
    {get_table_header_html(hidden_name="Symbol of Enhancement")}
    {get_price_rows_html(FORGE_ENH_NAMES, "smybol_enh_forge")}
</table>
"""

with (CWD / "style.css").open() as f:
    CSS_CONTENT = f.read()
STYLE = f"<style>{CSS_CONTENT}</style>"


PROFIT_CALCULATION_HTML = """
<h3 style="text-align: center;">Profit Calculator</h3>
<div style="display: flex; justify-content: center; align-items: flex-end; gap: 16px; margin-bottom: 24px;">
    <div style="display: flex; flex-direction: column; align-items: center;">
        <label for="manual-buy-g">Buy Price:</label>
        <div style="display: flex; gap: 4px;">
            <input id="manual-buy-g" type="text" inputmode="numeric" pattern="[0-9]*" placeholder="G" style="width: 40px;">
            <input id="manual-buy-s" type="text" inputmode="numeric" pattern="[0-9]*" placeholder="S" style="width: 40px;">
            <input id="manual-buy-c" type="text" inputmode="numeric" pattern="[0-9]*" placeholder="C" style="width: 40px;">
        </div>
    </div>
    <div style="display: flex; flex-direction: column; align-items: center;">
        <label for="manual-sell-g">Sell Price:</label>
        <div style="display: flex; gap: 4px;">
            <input id="manual-sell-g" type="text" inputmode="numeric" pattern="[0-9]*" placeholder="G" style="width: 40px;">
            <input id="manual-sell-s" type="text" inputmode="numeric" pattern="[0-9]*" placeholder="S" style="width: 40px;">
            <input id="manual-sell-c" type="text" inputmode="numeric" pattern="[0-9]*" placeholder="C" style="width: 40px;">
        </div>
    </div>
    <div style="align-self: flex-end;">
        <button onclick="calculateManualProfit()">Calculate</button>
    </div>
</div>
<div style="text-align: center; margin-bottom: 24px;">
    <span id="manual-profit-result" style="font-size: 18px;">Profit: 0g 0s 0c</span>
</div>
"""


def get_fetch_price_html(item_id: int) -> str:
    return f"""
const response = await fetch(`/api/price?item_id={item_id}`);
const data = await response.json();
if (data.error) {{
    alert(data.error);
    return;
}}

document.getElementById('{item_id}_buy_g').innerText = data.buy_g;
document.getElementById('{item_id}_buy_s').innerText = data.buy_s;
document.getElementById('{item_id}_buy_c').innerText = data.buy_c;

document.getElementById('{item_id}_sell_g').innerText = data.sell_g;
document.getElementById('{item_id}_sell_s').innerText = data.sell_s;
document.getElementById('{item_id}_sell_c').innerText = data.sell_c;

document.getElementById('{item_id}_flip_g').innerText = data.flip_g;
document.getElementById('{item_id}_flip_s').innerText = data.flip_s;
document.getElementById('{item_id}_flip_c').innerText = data.flip_c;
"""


def get_all_fetch_price_html(
    api_endpoint: str,
) -> str:
    return f"""
const response = await fetch(`/api/{api_endpoint}`);
const data = await response.json();

for (const [key, value] of Object.entries(data)) {{
    document.getElementById(key + '##' + `{api_endpoint}`).innerText = value;
}}
"""


def get_rare_gear_salvage_html() -> str:
    return get_all_fetch_price_html("rare_gear_salvage")


def get_rare_salvage_html() -> str:
    return get_all_fetch_price_html("gear_salvage")


def get_scholar_rune_html() -> str:
    return get_all_fetch_price_html("scholar_rune")


def get_guardian_rune_html() -> str:
    return get_all_fetch_price_html("guardian_rune")


def get_dragonhunter_rune_html() -> str:
    return get_all_fetch_price_html("dragonhunter_rune")


def get_fireworks_html() -> str:
    return get_all_fetch_price_html("relic_of_fireworks")


def get_rare_weapon_craft_html() -> str:
    return get_all_fetch_price_html("rare_weapon_craft")


def get_common_gear_salvage_html() -> str:
    return get_all_fetch_price_html("common_gear_salvage")


def get_forge_enh_html() -> str:
    return get_all_fetch_price_html("smybol_enh_forge")


def get_t5_mats_sell() -> str:
    return get_all_fetch_price_html("t5_mats_sell")


def get_t5_mats_buy() -> str:
    return get_all_fetch_price_html("t5_mats_buy")


def get_mats_crafting_compare() -> str:
    return get_all_fetch_price_html("mats_crafting_compare")


def get_loadstone_forge() -> str:
    return get_all_fetch_price_html("loadstone_forge")


with (CWD / "scripts.js").open() as f:
    SCRIPT_FUNCTIONS = f.read()

FETCH_PRICES = f"""
async function _fetchPrices() {{
    await Promise.all([
        (async () => {{ {get_fetch_price_html(ItemIDs.RARE_UNID_GEAR)} }})(),
        (async () => {{ {get_fetch_price_html(ItemIDs.ECTOPLASM)} }})(),
        (async () => {{ {get_rare_gear_salvage_html()} }})(),
        (async () => {{ {get_rare_salvage_html()} }})(),
        (async () => {{ {get_guardian_rune_html()} }})(),
        (async () => {{ {get_scholar_rune_html()} }})(),
        (async () => {{ {get_dragonhunter_rune_html()} }})(),
        (async () => {{ {get_fireworks_html()} }})(),
        (async () => {{ {get_rare_weapon_craft_html()} }})(),
        (async () => {{ {get_t5_mats_sell()} }})(),
        (async () => {{ {get_t5_mats_buy()} }})(),
        (async () => {{ {get_mats_crafting_compare()} }})(),
        (async () => {{ {get_common_gear_salvage_html()} }})(),
        (async () => {{ {get_forge_enh_html()} }})(),
        (async () => {{ {get_loadstone_forge()} }})(),
    ]);
}}
"""

SCRIPT = f"""
<script>
    {FETCH_PRICES}
    {SCRIPT_FUNCTIONS}
    window.addEventListener('DOMContentLoaded', fetchPrices);
</script>
"""

HTML_PAGE = f"""
<!DOCTYPE html>
<html>
<head>
    <title>GW2 TP King</title>
    {STYLE}
    {SCRIPT}
</head>
<body>
    <div id="fetch-popup">Prices updated!</div>
    <h1 style="text-align: center;">
            Guild Wars 2 TP King
    </h1>
    <div style="display: flex; justify-content: center;">
        <button onclick="fetchPrices()" style="margin-bottom: 20px;">Refresh Prices</button>
    </div>
    <div style="display: flex; justify-content: center; align-items: flex-start; gap: 40px; margin: 0 auto; max-width: 1400px;">
        <div style="flex: 1;">
            {PROFIT_CALCULATION_HTML}

            <h3 style="text-align: center;">Rare Unid. Gear</h3>
            {RARE_GEAR_TABLE}

            <h3 style="text-align: center;">
                <a href="https://wiki.guildwars2.com/wiki/Piece_of_Rare_Unidentified_Gear/Salvage_Rate" target="_blank" style="color: inherit; text-decoration: none;">
                    Rare Gear Ident & Salvaging
                </a>
            </h3>
            {RARE_GEAR_SALVAGE}

            <h3 style="text-align: center;">
                <a href="https://wiki.guildwars2.com/wiki/Piece_of_Unidentified_Gear/Salvage_Rate" target="_blank" style="color: inherit; text-decoration: none;">
                    Green Gear Ident & Salvaging
                </a>
            </h3>
            {GEAR_SALVAGE_TABLE}

            <h3 style="text-align: center;">
                <a href="https://wiki.guildwars2.com/wiki/Piece_of_Common_Unidentified_Gear/Salvage_Rate" target="_blank" style="color: inherit; text-decoration: none;">
                    Common Gear Ident & Salvaging
                </a>
            </h3>
            {COMMON_GEAR_SALVAGE_TABLE}

            <h3 style="text-align: center;">Forge Loadstones</h3>
            {LOADSTONE_TABLE}
        </div>
        <div style="flex: 1;">
            <h3 style="text-align: center;">Ectoplasm</h3>
            {ECTO_TABLE}

            <h3 style="text-align: center;">Mats Crafting Compare</h3>
            {MATS_CRAFT_COMPARE_TABLE}

            <h3 style="text-align: center;">T5 Mats Buy Order</h3>
            {T5_MATS_BUY_TABLE}

            <h3 style="text-align: center;">T5 Mats Sell Order</h3>
            {T5_MATS_SELL_TABLE}

            <h3 style="text-align: center;">Forge Symbol of Enhancement</h3>
            {FORGE_ENH_TABLE}
        </div>
        <div style="flex: 1;">
            <h3 style="text-align: center;">
                <a href="https://wiki.guildwars2.com/wiki/Krait_Shell" target="_blank" style="color: inherit; text-decoration: none;">
                    Rare Weapon Craft
                </a>
            </h3>
            {RARE_WEAPON_CRAFT_TABLE}

            <h3 style="text-align: center;">
                <a href="https://wiki.guildwars2.com/wiki/Superior_Rune_of_the_Scholar" target="_blank" style="color: inherit; text-decoration: none;">
                    Scholar Runes
                </a>
            </h3>
            {SCHOLAR_RUNE_TABLE}

            <h3 style="text-align: center;">
                <a href="https://wiki.guildwars2.com/wiki/Superior_Rune_of_the_Guardian" target="_blank" style="color: inherit; text-decoration: none;">
                    Guardian Runes
                </a>
            </h3>
            {GUARDIAN_RUNE_TABLE}

            <h3 style="text-align: center;">
                <a href="https://wiki.guildwars2.com/wiki/Superior_Rune_of_the_Dragonhunter" target="_blank" style="color: inherit; text-decoration: none;">
                    Dragonhunter Runes
                </a>
            </h3>
            {DRAGONHUNTER_RUNE_TABLE}

            <h3 style="text-align: center;">
                <a href="https://wiki.guildwars2.com/wiki/Relic_of_Fireworks" target="_blank" style="color: inherit; text-decoration: none;">
                    Relic of Fireworks
                </a>
            </h3>
            {FIREWORKS_TABLE}
        </div>
    </div>
</body>
</html>
"""
