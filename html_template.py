# ruff: noqa: E501
from items import ECTO_ITEM_ID
from items import RARE_UNID_ITEM_ID


def get_price_row_html(
    item_id: str,
    name: str,
) -> str:
    words = [word.capitalize() for word in item_id.split("_")]
    return f"""
<tr>
    <td>{" ".join(words)}</td>
    <td id="{item_id}_g##{name}">-</td>
    <td id="{item_id}_s##{name}">-</td>
    <td id="{item_id}_c##{name}">-</td>
</tr>"""


def get_flip_table_html(item_id: int) -> str:
    return f"""<table>
        <tr>
            <th>Type</th>
            <th>Gold</th>
            <th>Silver</th>
            <th>Copper</th>
        </tr>
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


ECTO_TABLE = get_flip_table_html(ECTO_ITEM_ID)
RARE_GEAR_TABLE = get_flip_table_html(RARE_UNID_ITEM_ID)

GEAR_TO_ECTO_TABLE = f"""
<table>
    <tr>
        <th></th>
        <th>Gold</th>
        <th>Silver</th>
        <th>copper</th>
    </tr>
    {get_price_row_html("ecto_sell_after_taxes", "gear_to_ecto")}
    {get_price_row_html("buy", "gear_to_ecto")}
    {get_price_row_html("gear_to_ecto_profit", "gear_to_ecto")}
</table>
"""

GEAR_SALVAGE_TABLE = f"""
<table>
    <tr>
        <th></th>
        <th>Gold</th>
        <th>Silver</th>
        <th>copper</th>
    </tr>
    {get_price_row_html("stack_buy", "gear_salvage")}
    {get_price_row_html("profit_stack", "gear_salvage")}
</table>
"""

T5_MATS_SELL_TABLE = f"""
<table>
    <tr>
        <th></th>
        <th>Gold</th>
        <th>Silver</th>
        <th>copper</th>
    </tr>
    {get_price_row_html("lucent_mote_sell", "t5_mats_sell")}
    {get_price_row_html("mithril_sell", "t5_mats_sell")}
    {get_price_row_html("elder_wood_sell", "t5_mats_sell")}
    {get_price_row_html("thick_leather_sell", "t5_mats_sell")}
</table>
"""

T5_MATS_BUY_TABLE = f"""
<table>
    <tr>
        <th></th>
        <th>Gold</th>
        <th>Silver</th>
        <th>copper</th>
    </tr>
    {get_price_row_html("mithril_ore_to_ingot", "t5_mats_buy")}
    {get_price_row_html("mithril_ingot_buy", "t5_mats_buy")}
    {get_price_row_html("elder_wood_log_to_plank", "t5_mats_buy")}
    {get_price_row_html("elder_wood_plank_buy", "t5_mats_buy")}
    {get_price_row_html("large_claw_buy_buy", "t5_mats_buy")}
    {get_price_row_html("potent_blood_buy_buy", "t5_mats_buy")}
    {get_price_row_html("large_bone_buy_buy", "t5_mats_buy")}
    {get_price_row_html("intricate_totem_buy_buy", "t5_mats_buy")}
    {get_price_row_html("large_fang_buy_buy", "t5_mats_buy")}
</table>
"""

COMMON_GEAR_SALVAGE_TABLE = f"""
<table>
    <tr>
        <th></th>
        <th>Gold</th>
        <th>Silver</th>
        <th>copper</th>
    </tr>
    {get_price_row_html("stack_buy", "common_gear_salvage")}
    {get_price_row_html("profit_stack", "common_gear_salvage")}
</table>
"""

SCHOLAR_RUNE_TABLE = f"""
<table>
    <tr>
        <th></th>
        <th>Gold</th>
        <th>Silver</th>
        <th>copper</th>
    </tr>
    {get_price_row_html("crafting_cost", "scholar_rune")}
    {get_price_row_html("crafting_cost_with_lucent_motes", "scholar_rune")}
    {get_price_row_html("sell", "scholar_rune")}
    {get_price_row_html("profit", "scholar_rune")}
    {get_price_row_html("profit_with_lucent_motes", "scholar_rune")}
</table>
"""

FIREWORKS_TABLE = f"""
<table>
    <tr>
        <th></th>
        <th>Gold</th>
        <th>Silver</th>
        <th>copper</th>
    </tr>
    {get_price_row_html("fireworks_crafting_cost", "relic_of_fireworks")}
    {get_price_row_html("fireworks_crafting_cost_with_lucent_motes", "relic_of_fireworks")}
    {get_price_row_html("fireworks_sell", "relic_of_fireworks")}
    {get_price_row_html("fireworks_profit", "relic_of_fireworks")}
    {get_price_row_html("fireworks_profit_with_lucent_motes", "relic_of_fireworks")}
</table>
"""

RARE_WEAPON_CRAFT_TABLE = f"""
<table>
    <tr>
        <th></th>
        <th>Gold</th>
        <th>Silver</th>
        <th>copper</th>
    </tr>
    {get_price_row_html("crafting_cost", "rare_weapon_craft")}
    {get_price_row_html("ecto_sell_after_taxes", "rare_weapon_craft")}
    {get_price_row_html("profit", "rare_weapon_craft")}
</table>
"""

STYLE = """
<style>
    body { background-color: #121212; color: #e0e0e0; font-family: Arial, sans-serif; margin: 20px; }
    table { border-collapse: collapse; width: 400px; margin-top: 20px; }
    th, td { border: 1px solid #444; padding: 8px; text-align: center; }
    th { background-color: #1f1f1f; color: #fff; }
    button { padding: 8px 12px; font-size: 14px; cursor: pointer; background-color: #333; color: #fff; border: 1px solid #555; }
    button:hover { background-color: #444; }
    #fetch-popup {
        display: none;
        position: absolute;
        left: 50%;
        transform: translateX(-50%);
        top: 80px;
        background: #222;
        color: #fff;
        padding: 8px 16px;
        border-radius: 6px;
        text-align: center;
        width: fit-content;
        box-shadow: 0 2px 8px rgba(0,0,0,0.3);
        z-index: 100;
    }
    #fetch-popup.show {
        display: block;
        opacity: 1;
    }
</style>
"""


PROFIT_CALCULATION_HTML = """
<h2 style="text-align: center;">Profit Calculator</h2>
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


def get_rare_gear_to_ecto_html() -> str:
    return get_all_fetch_price_html("gear_to_ecto")


def get_rare_salvage_html() -> str:
    return get_all_fetch_price_html("gear_salvage")


def get_scholar_rune_html() -> str:
    return get_all_fetch_price_html("scholar_rune")


def get_fireworks_html() -> str:
    return get_all_fetch_price_html("relic_of_fireworks")


def get_rare_weapon_craft_html() -> str:
    return get_all_fetch_price_html("rare_weapon_craft")


def get_common_gear_salvage_html() -> str:
    return get_all_fetch_price_html("common_gear_salvage")


def get_t5_mats_sell() -> str:
    return get_all_fetch_price_html("t5_mats_sell")


def get_t5_mats_buy() -> str:
    return get_all_fetch_price_html("t5_mats_buy")


SCRIPT = f"""
<script>
async function _fetchPrices() {{
    await Promise.all([
        (async () => {{ {get_fetch_price_html(RARE_UNID_ITEM_ID)} }})(),
        (async () => {{ {get_fetch_price_html(ECTO_ITEM_ID)} }})(),
        (async () => {{ {get_rare_gear_to_ecto_html()} }})(),
        (async () => {{ {get_rare_salvage_html()} }})(),
        (async () => {{ {get_scholar_rune_html()} }})(),
        (async () => {{ {get_fireworks_html()} }})(),
        (async () => {{ {get_rare_weapon_craft_html()} }})(),
        (async () => {{ {get_t5_mats_sell()} }})(),
        (async () => {{ {get_t5_mats_buy()} }})(),
        (async () => {{ {get_common_gear_salvage_html()} }})(),
    ]);
}}

function showFetchPopup() {{
    const popup = document.getElementById('fetch-popup');
    popup.classList.add('show');
    setTimeout(() => {{
        popup.classList.remove('show');
    }}, 1000);
    console.log("Prices fetched and updated.");
}}

async function fetchPrices() {{
    await _fetchPrices();
    showFetchPopup();
}}

window.addEventListener('DOMContentLoaded', fetchPrices);

function calculateManualProfit() {{
    const buyG = parseInt(document.getElementById('manual-buy-g').value) || 0;
    const buyS = parseInt(document.getElementById('manual-buy-s').value) || 0;
    const buyC = parseInt(document.getElementById('manual-buy-c').value) || 0;
    const sellG = parseInt(document.getElementById('manual-sell-g').value) || 0;
    const sellS = parseInt(document.getElementById('manual-sell-s').value) || 0;
    const sellC = parseInt(document.getElementById('manual-sell-c').value) || 0;

    console.log(`Calculating profit: Buy - ${{buyG}}g ${{buyS}}s ${{buyC}}c, Sell - ${{sellG}}g ${{sellS}}s ${{sellC}}c`);

    // Convert to copper
    const buyTotal = buyG * 10000 + buyS * 100 + buyC;
    const sellTotal = sellG * 10000 + sellS * 100 + sellC;

    // GW2 TP takes 15% fee from sell price
    const sellAfterTax = Math.floor(sellTotal * 0.85);

    const profit = sellAfterTax - buyTotal;
    console.log(`Profit calculated: ${{profit}} copper`);

    let profitG, profitS, profitC;
    if (profit < 0) {{
        profitG = Math.floor((-1 * profit) / 10000);
        profitS = Math.floor(((-1 * profit) % 10000) / 100);
        profitC = (-1 * profit) % 100;
    }} else {{
        profitG = Math.floor(profit / 10000);
        profitS = Math.floor((profit % 10000) / 100);
        profitC = profit % 100;
    }}

    let resultText;
    let color;
    if (profit >= 0) {{
        resultText = `Profit: ${{profitG}}g ${{profitS}}s ${{profitC}}c`;
        color = "#FFD700"; // gold-ish
    }} else {{
        resultText = `Loss: ${{Math.abs(profitG)}}g ${{Math.abs(profitS)}}s ${{Math.abs(profitC)}}c`;
        color = "#f44336"; // red
    }}
    const resultElem = document.getElementById('manual-profit-result');
    resultElem.innerText = resultText;
    resultElem.style.color = color;
}}
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

            <h2 style="text-align: center;">Rare Unid. Gear</h2>
            {RARE_GEAR_TABLE}

            <h2 style="text-align: center;">Rare Gear to Ecto</h2>
            {GEAR_TO_ECTO_TABLE}

            <h2 style="text-align: center;">
                <a href="https://wiki.guildwars2.com/wiki/Piece_of_Unidentified_Gear/Salvage_Rate" target="_blank" style="color: inherit; text-decoration: none;">
                    Green Gear Ident & Salvaging
                </a>
            </h2>
            {GEAR_SALVAGE_TABLE}

            <h2 style="text-align: center;">
                <a href="https://wiki.guildwars2.com/wiki/Piece_of_Common_Unidentified_Gear/Salvage_Rate" target="_blank" style="color: inherit; text-decoration: none;">
                    Common Gear Ident & Salvaging
                </a>
            </h2>
            {COMMON_GEAR_SALVAGE_TABLE}
        </div>
        <div style="flex: 1;">
            <h2 style="text-align: center;">Ectoplasm</h2>
            {ECTO_TABLE}

            <h2 style="text-align: center;">T5 Mats Sell Order</h2>
            {T5_MATS_SELL_TABLE}

            <h2 style="text-align: center;">T5 Mats Buy Order</h2>
            {T5_MATS_BUY_TABLE}
        </div>
        <div style="flex: 1;">
            <h2 style="text-align: center;">
                <a href="https://wiki.guildwars2.com/wiki/Krait_Shell" target="_blank" style="color: inherit; text-decoration: none;">
                    Rare Weapon Craft
                </a>
            </h2>
            {RARE_WEAPON_CRAFT_TABLE}

            <h2 style="text-align: center;">
                <a href="https://wiki.guildwars2.com/wiki/Superior_Rune_of_the_Scholar" target="_blank" style="color: inherit; text-decoration: none;">
                    Scholar Runes
                </a>
            </h2>
            {SCHOLAR_RUNE_TABLE}

            <h2 style="text-align: center;">
                <a href="https://wiki.guildwars2.com/wiki/Relic_of_Fireworks" target="_blank" style="color: inherit; text-decoration: none;">
                    Relic of Fireworks
                </a>
            </h2>
            {FIREWORKS_TABLE}
        </div>
    </div>
</body>
</html>
"""
