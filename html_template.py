from items import ECTO_ITEM_ID, RARE_UNID_ITEM_ID


def get_price_row_html(item_id: str) -> str:
    return f"""
<tr>
    <td>{" ".join(word.capitalize() for word in item_id.split("_"))}</td>
    <td id="{item_id}_g">-</td>
    <td id="{item_id}_s">-</td>
    <td id="{item_id}_c">-</td>
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
            <td>Buy</td>
            <td id="{item_id}_buy_g">-</td>
            <td id="{item_id}_buy_s">-</td>
            <td id="{item_id}_buy_c">-</td>
        </tr>
        <tr>
            <td>Sell</td>
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
    {get_price_row_html("ecto_sell_after_taxes")}
    {get_price_row_html("rare_gear_buy")}
    {get_price_row_html("gear_to_ecto_profit")}
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
    {get_price_row_html("gear_stack_buy")}
    {get_price_row_html("lucent_mote_sell")}
    {get_price_row_html("mithril_sell")}
    {get_price_row_html("elder_wood_sell")}
    {get_price_row_html("thick_leather_sell")}
    {get_price_row_html("profit_stack")}
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
    {get_price_row_html("scholar_crafting_cost")}
    {get_price_row_html("scholar_crafting_cost_with_lucent_motes")}
    {get_price_row_html("scholar_rune_sell")}
    {get_price_row_html("scholar_profit")}
    {get_price_row_html("scholar_profit_with_lucent_motes")}
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
    {get_price_row_html("fireworks_crafting_cost")}
    {get_price_row_html("fireworks_crafting_cost_with_lucent_motes")}
    {get_price_row_html("fireworks_sell")}
    {get_price_row_html("fireworks_profit")}
    {get_price_row_html("fireworks_profit_with_lucent_motes")}
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
    {get_price_row_html("mithril_ore__to_ingot_cost")}
    {get_price_row_html("mithril_ingot_cost")}
    {get_price_row_html("elder_wood_log_to_plank_cost")}
    {get_price_row_html("elder_wood_plank_cost")}
    {get_price_row_html("large_claw_buy_cost")}
    {get_price_row_html("potent_blood_buy_cost")}
    {get_price_row_html("large_bone_buy_cost")}
    {get_price_row_html("intricate_totem_buy_cost")}
    {get_price_row_html("large_fang_buy_cost")}
    {get_price_row_html("crafting_cost_with_cheap_materials")}
    {get_price_row_html("ecto_sell_after_taxes2")}
    {get_price_row_html("rare_gear_craft_profit")}
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
</style>
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


def get_rare_gear_to_ecto_html() -> str:
    return """
const response = await fetch(`/api/gear_to_ecto`);
const data = await response.json();

for (const [key, value] of Object.entries(data)) {
    document.getElementById(key).innerText = value;
}
"""


def get_rare_salvage_html() -> str:
    return """
const response = await fetch(`/api/gear_salvage`);
const data = await response.json();

for (const [key, value] of Object.entries(data)) {
    document.getElementById(key).innerText = value;
}
"""


def get_scholar_rune_html() -> str:
    return """
const response = await fetch(`/api/scholar_rune`);
const data = await response.json();

for (const [key, value] of Object.entries(data)) {
    document.getElementById(key).innerText = value;
}
"""


def get_fireworks_html() -> str:
    return """
const response = await fetch(`/api/relic_of_fireworks`);
const data = await response.json();

for (const [key, value] of Object.entries(data)) {
    document.getElementById(key).innerText = value;
}
"""

def get_rare_gear_craft_html() -> str:
    return """
const response = await fetch(`/api/rare_gear_craft`);
const data = await response.json();
console.log("Called");

for (const [key, value] of Object.entries(data)) {
    document.getElementById(key).innerText = value;
}
"""


SCRIPT = f"""
<script>
    async function fetchPrices() {{
        await Promise.all([
            (async () => {{ {get_fetch_price_html(RARE_UNID_ITEM_ID)} }})(),
            (async () => {{ {get_fetch_price_html(ECTO_ITEM_ID)} }})(),
            (async () => {{ {get_rare_gear_to_ecto_html()} }})(),
            (async () => {{ {get_rare_salvage_html()} }})(),
            (async () => {{ {get_scholar_rune_html()} }})(),
            (async () => {{ {get_fireworks_html()} }})(),
            (async () => {{ {get_rare_gear_craft_html()} }})(),
        ]);
    }}

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
    <h1 style="text-align: center;">Guild Wars 2 TP King</h1>
    <div style="display: flex; justify-content: center;">
        <button onclick="fetchPrices()" style="margin-bottom: 20px;">Refresh Prices</button>
    </div>
    <div style="display: flex; justify-content: center; align-items: flex-start; gap: 40px; margin: 0 auto; max-width: 1000px;">
        <div style="flex: 1;">
            <h2 style="text-align: center;">Ectoplasm</h2>
            {ECTO_TABLE}

            <h2 style="text-align: center;">Rare Unid Gear</h2>
            {RARE_GEAR_TABLE}

            <h2 style="text-align: center;">Rare Gear to Ecto</h2>
            {GEAR_TO_ECTO_TABLE}

            <h2 style="text-align: center;">Rare Weapon Craft</h2>
            {RARE_WEAPON_CRAFT_TABLE}
        </div>
        <div style="flex: 1;">
            <h2 style="text-align: center;">Gear Ident & Salvaging</h2>
            {GEAR_SALVAGE_TABLE}

            <h2 style="text-align: center;">Scholar Runes</h2>
            {SCHOLAR_RUNE_TABLE}

            <h2 style="text-align: center;">Relic of Fireworks</h2>
            {FIREWORKS_TABLE}
        </div>
    </div>
</body>
</html>
"""
