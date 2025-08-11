from items import ECTO_ITEM_ID, RARE_UNID_ITEM_ID


def get_table_html(item_id: int) -> str:
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


ECTO_TABLE = get_table_html(ECTO_ITEM_ID)
RARE_GEAR_TABLE = get_table_html(RARE_UNID_ITEM_ID)

GEAR_TO_ECTO_TABLE = """
<table>
    <tr>
        <th></th>
        <th>Gold</th>
        <th>Silver</th>
        <th>copper</th>
    </tr>
    <tr>
        <td>Ecto Sell after Taxes</td>
        <td id="ecto_sell_after_taxes_g">-</td>
        <td id="ecto_sell_after_taxes_s">-</td>
        <td id="ecto_sell_after_taxes_c">-</td>
    </tr>
    <tr>
        <td>Rare Gear Buy</td>
        <td id="rare_gear_buy_g">-</td>
        <td id="rare_gear_buy_s">-</td>
        <td id="rare_gear_buy_c">-</td>
    </tr>
    <tr>
        <td>Gear to Ecto Profit</td>
        <td id="gear_to_ecto_profit_g">-</td>
        <td id="gear_to_ecto_profit_s">-</td>
        <td id="gear_to_ecto_profit_c">-</td>
    </tr>
</table>
"""

GEAR_SALVAGE_TABLE = """
<table>
    <tr>
        <th></th>
        <th>Gold</th>
        <th>Silver</th>
        <th>copper</th>
    </tr>
    <tr>
        <td>Gear Stack Price (Buy)</td>
        <td id="gear_stack_buy_g">-</td>
        <td id="gear_stack_buy_s">-</td>
        <td id="gear_stack_buy_c">-</td>
    </tr>
    <tr>
        <td>Lucent Mote Stack</td>
        <td id="lucent_mote_sell_g">-</td>
        <td id="lucent_mote_sell_s">-</td>
        <td id="lucent_mote_sell_c">-</td>
    </tr>
    <tr>
        <td>Mithril Stack</td>
        <td id="mithril_sell_g">-</td>
        <td id="mithril_sell_s">-</td>
        <td id="mithril_sell_c">-</td>
    </tr>
    <tr>
        <td>Elder Wood Stack</td>
        <td id="elder_wood_sell_g">-</td>
        <td id="elder_wood_sell_s">-</td>
        <td id="elder_wood_sell_c">-</td>
    </tr>
    <tr>
        <td>Thick Leather</td>
        <td id="thick_leather_sell_g">-</td>
        <td id="thick_leather_sell_s">-</td>
        <td id="thick_leather_sell_c">-</td>
    </tr>
    <tr>
        <td>Est. Profit Stack</td>
        <td id="profit_stack_g">-</td>
        <td id="profit_stack_s">-</td>
        <td id="profit_stack_c">-</td>
    </tr>
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

document.getElementById('ecto_sell_after_taxes_g').innerText = data.ecto_sell_after_taxes_g;
document.getElementById('ecto_sell_after_taxes_s').innerText = data.ecto_sell_after_taxes_s;
document.getElementById('ecto_sell_after_taxes_c').innerText = data.ecto_sell_after_taxes_c;

document.getElementById('rare_gear_buy_g').innerText = data.rare_gear_buy_g;
document.getElementById('rare_gear_buy_s').innerText = data.rare_gear_buy_s;
document.getElementById('rare_gear_buy_c').innerText = data.rare_gear_buy_c;

document.getElementById('gear_to_ecto_profit_g').innerText = data.gear_to_ecto_profit_g;
document.getElementById('gear_to_ecto_profit_s').innerText = data.gear_to_ecto_profit_s;
document.getElementById('gear_to_ecto_profit_c').innerText = data.gear_to_ecto_profit_c;
"""

def get_rare_salvage_html() -> str:
    return """
const response = await fetch(`/api/gear_salvage`);
const data = await response.json();

document.getElementById('gear_stack_buy_g').innerText = data.gear_stack_buy_g;
document.getElementById('gear_stack_buy_s').innerText = data.gear_stack_buy_s;
document.getElementById('gear_stack_buy_c').innerText = data.gear_stack_buy_c;

document.getElementById('lucent_mote_sell_g').innerText = data.lucent_mote_sell_g;
document.getElementById('lucent_mote_sell_s').innerText = data.lucent_mote_sell_s;
document.getElementById('lucent_mote_sell_c').innerText = data.lucent_mote_sell_c;

document.getElementById('mithril_sell_g').innerText = data.mithril_sell_g;
document.getElementById('mithril_sell_s').innerText = data.mithril_sell_s;
document.getElementById('mithril_sell_c').innerText = data.mithril_sell_c;

document.getElementById('elder_wood_sell_g').innerText = data.elder_wood_sell_g;
document.getElementById('elder_wood_sell_s').innerText = data.elder_wood_sell_s;
document.getElementById('elder_wood_sell_c').innerText = data.elder_wood_sell_c;

document.getElementById('thick_leather_sell_g').innerText = data.thick_leather_sell_g;
document.getElementById('thick_leather_sell_s').innerText = data.thick_leather_sell_s;
document.getElementById('thick_leather_sell_c').innerText = data.thick_leather_sell_c;

document.getElementById('profit_stack_g').innerText = data.profit_stack_g;
document.getElementById('profit_stack_s').innerText = data.profit_stack_s;
document.getElementById('profit_stack_c').innerText = data.profit_stack_c;
"""


SCRIPT = f"""
<script>
    async function fetchPrices() {{
        await Promise.all([
            (async () => {{ {get_fetch_price_html(RARE_UNID_ITEM_ID)} }})(),
            (async () => {{ {get_fetch_price_html(ECTO_ITEM_ID)} }})(),
            (async () => {{ {get_rare_gear_to_ecto_html()} }})(),
            (async () => {{ {get_rare_salvage_html()} }})(),
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
    <h1>Guild Wars 2 TP King</h1>

    <button onclick="fetchPrices()">Refresh Prices</button>

    <div id="19721">
        <h2>Ectoplasm</h2>
        {ECTO_TABLE}
    </div>

    <div id="50016">
        <h2>Rare Unid Gear</h2>

        {RARE_GEAR_TABLE}

        {GEAR_TO_ECTO_TABLE}

        {GEAR_SALVAGE_TABLE}
    </div>
</body>
</html>
"""
