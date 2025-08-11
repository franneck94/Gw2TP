from __future__ import annotations

from typing import Any, Dict, Tuple

import httpx
from flask import Flask, jsonify, render_template_string, request

from html_template import HTML_PAGE
from items import (ANCIENT_WOOD_ID, CHARM_OF_BRILLIANCE_ID,
                   CHARM_OF_POTENCE_ID, CHARM_OF_SKILL_ID, ECTO_ITEM_ID,
                   ELABORATE_TOTEM_ID, ELDER_WOOD_ID, GOSSAMER_SCRAP_ID,
                   HARDENED_LEATHER_ID, LUCENT_MOTE_ID, MIRTHIL_ID,
                   ORICHALCUM_ID, PILE_OF_LUCENT_CRYSTAL_ID, RARE_UNID_ITEM_ID,
                   RELIC_OF_FIREWORKS_ID, SCHOLAR_RUNE_ID, SILK_SCRAP_ID,
                   SYMBOL_OF_CONTROL_ID, SYMBOL_OF_ENH_ID, SYMBOL_OF_PAIN_ID,
                   THICK_LEATHER_ID, UNID_ITEM_ID)

GW2_COMMERCE_URL: str = "https://api.guildwars2.com/v2/commerce/prices"

app = Flask(__name__)


def copper_to_gsc(
    copper: int,
) -> Tuple[int, int, int]:
    negative = False
    if copper < 0:
        negative = True
        copper = abs(copper)

    gold = int(copper // 10000)
    silver = int((copper % 10000) // 100)
    copper_rest = int(copper % 100)

    if negative:
        gold = -gold
        silver = -silver
        copper_rest = -copper_rest

    return gold, silver, copper_rest


def gsc_to_copper(
    gold: int,
    silver: int,
    copper: int,
) -> int:
    return gold * 10000 + silver * 100 + copper


def fetch_tp_prices(
    item_ids: list[int],
) -> dict[int, dict[str, any]]:
    params = {"ids": ",".join(str(i) for i in item_ids)}
    with httpx.Client() as client:
        response = client.get(GW2_COMMERCE_URL, params=params, timeout=10.0)
    response.raise_for_status()
    data = response.json()
    if not isinstance(data, list) or len(data) == 0:
        raise RuntimeError("No items found")

    result: dict[int, dict[str, any]] = {}
    for item in data:
        item_id = int(item["id"])
        buy_price = int(item["buys"]["unit_price"])
        sell_price = int(item["sells"]["unit_price"])
        flip_profit = round(sell_price * 0.85, 6) - buy_price
        buy_g, buy_s, buy_c = copper_to_gsc(buy_price)
        sell_g, sell_s, sell_c = copper_to_gsc(sell_price)
        flip_g, flip_s, flip_c = copper_to_gsc(flip_profit)

        result[item_id] = {
            "buy_copper": buy_price,
            "sell_copper": sell_price,
            "buy_g": buy_g,
            "buy_s": buy_s,
            "buy_c": buy_c,
            "sell_g": sell_g,
            "sell_s": sell_s,
            "sell_c": sell_c,
            "flip_g": flip_g,
            "flip_s": flip_s,
            "flip_c": flip_c,
            "sell_after_taxes_g": int(sell_price * 0.85 // 10000),
            "sell_after_taxes_s": int((sell_price * 0.85 % 10000) // 100),
            "sell_after_taxes_c": int(sell_price * 0.85 % 100),
        }
    return result


@app.route("/")
def index() -> str:
    return render_template_string(HTML_PAGE)


@app.route("/api/price")
def get_price() -> Any:
    try:
        item_id = request.args.get("item_id", type=int)
        data = fetch_tp_prices([item_id])
        return jsonify(data[item_id])
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/api/gear_to_ecto")
def get_gear_to_ecto() -> Any:
    try:
        result = fetch_tp_prices([ECTO_ITEM_ID, RARE_UNID_ITEM_ID])
        ecto_data = result[ECTO_ITEM_ID]
        rare_gear_data = result[RARE_UNID_ITEM_ID]
        ecto_ident_rate = 0.9

        ecto_sell_after_taxes = gsc_to_copper(
            ecto_data["sell_after_taxes_g"],
            ecto_data["sell_after_taxes_s"],
            ecto_data["sell_after_taxes_c"],
        )
        gear_buy = gsc_to_copper(
            rare_gear_data["buy_g"],
            rare_gear_data["buy_s"],
            rare_gear_data["buy_c"],
        )

        profit = gear_buy - ecto_sell_after_taxes * ecto_ident_rate
        profit_g, profit_s, profit_c = copper_to_gsc(profit)

        data = {
            "ecto_sell_after_taxes_g": ecto_data["sell_after_taxes_g"],
            "ecto_sell_after_taxes_s": ecto_data["sell_after_taxes_s"],
            "ecto_sell_after_taxes_c": ecto_data["sell_after_taxes_c"],
            "rare_gear_buy_g": rare_gear_data["buy_g"],
            "rare_gear_buy_s": rare_gear_data["buy_s"],
            "rare_gear_buy_c": rare_gear_data["buy_c"],
            "gear_to_ecto_profit_g": profit_g,
            "gear_to_ecto_profit_s": profit_s,
            "gear_to_ecto_profit_c": profit_c,
        }

        return jsonify(data)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/api/scholar_rune")
def get_scholar_rune() -> Any:
    try:
        result = fetch_tp_prices(
            [
                ECTO_ITEM_ID,
                ELABORATE_TOTEM_ID,
                PILE_OF_LUCENT_CRYSTAL_ID,
                CHARM_OF_BRILLIANCE_ID,
                LUCENT_MOTE_ID,
                SCHOLAR_RUNE_ID,
            ]
        )
        ecto_data = result[ECTO_ITEM_ID]["buy_copper"]
        totem_data = result[ELABORATE_TOTEM_ID]["buy_copper"]
        lucent_crystal_data = result[PILE_OF_LUCENT_CRYSTAL_ID]["buy_copper"]
        charm_data = result[CHARM_OF_BRILLIANCE_ID]["buy_copper"]
        lucent_mote_data = result[LUCENT_MOTE_ID]["buy_copper"]
        scholar_rune_sell_copper = result[SCHOLAR_RUNE_ID]["sell_copper"]
        scholar_rune_sell_g, scholar_rune_sell_s, scholar_rune_sell_c = copper_to_gsc(
            scholar_rune_sell_copper
        )

        scholar_crafting_cost_copper = (
            ecto_data * 5.0
            + totem_data * 5.0
            + lucent_crystal_data * 8.0
            + charm_data * 2.0
        )
        scholar_crafting_cost2_copper = (
            ecto_data * 5.0
            + totem_data * 5.0
            + lucent_mote_data * 80.0
            + charm_data * 2.0
        )

        profit = scholar_rune_sell_copper * 0.85 - scholar_crafting_cost_copper
        profit2 = scholar_rune_sell_copper * 0.85 - scholar_crafting_cost2_copper
        scholar_profit_g, scholar_profit_s, scholar_profit_c = copper_to_gsc(profit)
        scholar_profit2_g, scholar_profit2_s, scholar_profit2_c = copper_to_gsc(profit2)

        scholar_crafting_cost_g, scholar_crafting_cost_s, scholar_crafting_cost_c = (
            copper_to_gsc(scholar_crafting_cost_copper)
        )
        scholar_crafting_cost2_g, scholar_crafting_cost2_s, scholar_crafting_cost2_c = (
            copper_to_gsc(scholar_crafting_cost2_copper)
        )

        data = {
            "scholar_crafting_cost_g": scholar_crafting_cost_g,
            "scholar_crafting_cost_s": scholar_crafting_cost_s,
            "scholar_crafting_cost_c": scholar_crafting_cost_c,
            "scholar_crafting_cost2_g": scholar_crafting_cost2_g,
            "scholar_crafting_cost2_s": scholar_crafting_cost2_s,
            "scholar_crafting_cost2_c": scholar_crafting_cost2_c,
            "scholar_sell_g": scholar_rune_sell_g,
            "scholar_sell_s": scholar_rune_sell_s,
            "scholar_sell_c": scholar_rune_sell_c,
            "scholar_profit_g": scholar_profit_g,
            "scholar_profit_s": scholar_profit_s,
            "scholar_profit_c": scholar_profit_c,
            "scholar_profit2_g": scholar_profit2_g,
            "scholar_profit2_s": scholar_profit2_s,
            "scholar_profit2_c": scholar_profit2_c,
        }

        return jsonify(data)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/api/relic_of_fireworks")
def get_relic_of_fireworks() -> Any:
    try:
        result = fetch_tp_prices(
            [
                ECTO_ITEM_ID,
                PILE_OF_LUCENT_CRYSTAL_ID,
                CHARM_OF_SKILL_ID,
                LUCENT_MOTE_ID,
                RELIC_OF_FIREWORKS_ID,
            ]
        )
        ecto_data = result[ECTO_ITEM_ID]["buy_copper"]
        lucent_crystal_data = result[PILE_OF_LUCENT_CRYSTAL_ID]["buy_copper"]
        charm_data = result[CHARM_OF_SKILL_ID]["buy_copper"]
        lucent_mote_data = result[LUCENT_MOTE_ID]["buy_copper"]
        relic_of_fireworks_sell_copper = result[RELIC_OF_FIREWORKS_ID]["sell_copper"]
        (
            relic_of_fireworks_sell_g,
            relic_of_fireworks_sell_s,
            relic_of_fireworks_sell_c,
        ) = copper_to_gsc(relic_of_fireworks_sell_copper)

        fireworks_crafting_cost_copper = (
            ecto_data * 15.0 + lucent_crystal_data * 48.0 + charm_data * 3.0
        )
        fireworks_crafting_cost2_copper = (
            ecto_data * 15.0 + lucent_mote_data * 480.0 + charm_data * 3.0
        )

        profit = relic_of_fireworks_sell_copper * 0.85 - fireworks_crafting_cost_copper
        profit2 = (
            relic_of_fireworks_sell_copper * 0.85 - fireworks_crafting_cost2_copper
        )
        fireworks_profit_g, fireworks_profit_s, fireworks_profit_c = copper_to_gsc(
            profit
        )
        fireworks_profit2_g, fireworks_profit2_s, fireworks_profit2_c = copper_to_gsc(
            profit2
        )

        (
            fireworks_crafting_cost_g,
            fireworks_crafting_cost_s,
            fireworks_crafting_cost_c,
        ) = copper_to_gsc(fireworks_crafting_cost_copper)
        (
            fireworks_crafting_cost2_g,
            fireworks_crafting_cost2_s,
            fireworks_crafting_cost2_c,
        ) = copper_to_gsc(fireworks_crafting_cost2_copper)

        data = {
            "fireworks_crafting_cost_g": fireworks_crafting_cost_g,
            "fireworks_crafting_cost_s": fireworks_crafting_cost_s,
            "fireworks_crafting_cost_c": fireworks_crafting_cost_c,
            "fireworks_crafting_cost2_g": fireworks_crafting_cost2_g,
            "fireworks_crafting_cost2_s": fireworks_crafting_cost2_s,
            "fireworks_crafting_cost2_c": fireworks_crafting_cost2_c,
            "fireworks_sell_g": relic_of_fireworks_sell_g,
            "fireworks_sell_s": relic_of_fireworks_sell_s,
            "fireworks_sell_c": relic_of_fireworks_sell_c,
            "fireworks_profit_g": fireworks_profit_g,
            "fireworks_profit_s": fireworks_profit_s,
            "fireworks_profit_c": fireworks_profit_c,
            "fireworks_profit2_g": fireworks_profit2_g,
            "fireworks_profit2_s": fireworks_profit2_s,
            "fireworks_profit2_c": fireworks_profit2_c,
        }

        return jsonify(data)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/api/gear_salvage")
def get_gear_salvage() -> Any:
    try:
        result = fetch_tp_prices(
            [
                UNID_ITEM_ID,
                ECTO_ITEM_ID,
                LUCENT_MOTE_ID,
                MIRTHIL_ID,
                ELDER_WOOD_ID,
                THICK_LEATHER_ID,
                GOSSAMER_SCRAP_ID,
                SILK_SCRAP_ID,
                HARDENED_LEATHER_ID,
                ANCIENT_WOOD_ID,
                SYMBOL_OF_ENH_ID,
                SYMBOL_OF_PAIN_ID,
                ORICHALCUM_ID,
                SYMBOL_OF_CONTROL_ID,
                CHARM_OF_BRILLIANCE_ID,
                CHARM_OF_POTENCE_ID,
                CHARM_OF_SKILL_ID,
            ]
        )
        ecto_data = result[ECTO_ITEM_ID]
        gear_data = result[UNID_ITEM_ID]
        lucent_mote_data = result[LUCENT_MOTE_ID]
        mithril_data = result[MIRTHIL_ID]
        elder_wood_data = result[ELDER_WOOD_ID]
        thick_leather_data = result[THICK_LEATHER_ID]
        gossamer_scrap_data = result[GOSSAMER_SCRAP_ID]
        silk_scrap_data = result[SILK_SCRAP_ID]
        hardened_data = result[HARDENED_LEATHER_ID]
        ancient_wood_data = result[ANCIENT_WOOD_ID]
        symbol_of_enh_data = result[SYMBOL_OF_ENH_ID]
        symbol_of_pain_data = result[SYMBOL_OF_PAIN_ID]
        orichalcum_data = result[ORICHALCUM_ID]
        symbol_of_control_data = result[SYMBOL_OF_CONTROL_ID]
        charm_of_brilliance_data = result[CHARM_OF_BRILLIANCE_ID]
        charm_of_potence_data = result[CHARM_OF_POTENCE_ID]
        charm_of_skill_data = result[CHARM_OF_SKILL_ID]

        buy_stack_copper = gear_data["buy_copper"] * 250.0
        buy_stack_g, buy_stack_s, buy_stack_c = copper_to_gsc(buy_stack_copper)

        lucent_mote_copper = lucent_mote_data["sell_copper"]
        lucent_mote_stack_sell_g, lucent_mote_stack_sell_s, lucent_mote_stack_sell_c = (
            copper_to_gsc(lucent_mote_copper * 250.0)
        )

        mithril_copper = mithril_data["sell_copper"]
        mithril_stack_sell_g, mithril_stack_sell_s, mithril_stack_sell_c = (
            copper_to_gsc(mithril_copper * 250.0)
        )

        elder_wood_copper = elder_wood_data["sell_copper"]
        elder_wood_stack_sell_g, elder_wood_stack_sell_s, elder_wood_stack_sell_c = (
            copper_to_gsc(elder_wood_copper * 250.0)
        )

        ecto_sellcopper = ecto_data["sell_copper"]

        thick_leather_data_sell_copper = thick_leather_data["sell_copper"]
        (
            thick_leather_stack_sell_g,
            thick_leather_stack_sell_s,
            thick_leather_stack_sell_c,
        ) = copper_to_gsc(thick_leather_data_sell_copper * 250.0)

        gossamer_scrap_data_sell_copper = gossamer_scrap_data["sell_copper"]
        silk_scrap_data_sell_copper = silk_scrap_data["sell_copper"]
        hardened_data_sell_copper = hardened_data["sell_copper"]
        ancient_wood_data_sell_copper = ancient_wood_data["sell_copper"]
        symbol_of_enh_data_sell_copper = symbol_of_enh_data["sell_copper"]
        symbol_of_pain_data_sell_copper = symbol_of_pain_data["sell_copper"]
        orichalcum_data_sell_copper = orichalcum_data["sell_copper"]
        symbol_of_control__sell_copper = symbol_of_control_data["sell_copper"]
        charm_of_brilliance_sell_copper = charm_of_brilliance_data["sell_copper"]
        charm_of_potence_sell_copper = charm_of_potence_data["sell_copper"]
        charm_of_skilldata_sell_copper = charm_of_skill_data["sell_copper"]

        profit_stack_copper = (
            mithril_copper * (250.0 * 0.4299) * 0.85
            + elder_wood_copper * (250.0 * 0.3564) * 0.85
            + silk_scrap_data_sell_copper * (250.0 * 0.3521) * 0.85
            + thick_leather_data_sell_copper * (250.0 * 0.2673) * 0.85
            + orichalcum_data_sell_copper * (250.0 * 0.0387) * 0.85
            + ancient_wood_data_sell_copper * (250.0 * 0.0287) * 0.85
            + gossamer_scrap_data_sell_copper * (250.0 * 0.018) * 0.85
            + hardened_data_sell_copper * (250.0 * 0.0169) * 0.85
            + ecto_sellcopper * (250.0 * 0.0296) * 0.85
            + lucent_mote_copper * (250.0 * 0.98) * 0.85
            + symbol_of_control__sell_copper * (250.0 * 0.0018) * 0.85
            + symbol_of_enh_data_sell_copper * (250.0 * 0.001) * 0.85
            + symbol_of_pain_data_sell_copper * (250.0 * 0.0006) * 0.85
            + charm_of_brilliance_sell_copper * (250.0 * 0.0042) * 0.85
            + charm_of_potence_sell_copper * (250.0 * 0.0029) * 0.85
            + charm_of_skilldata_sell_copper * (250.0 * 0.0028) * 0.85
            - buy_stack_copper
            - 30.0 * 245  # Runecrafter
            - 60 * 5  # Silver Fed
        )
        profit_stack_g, profit_stack_s, profit_stack_c = copper_to_gsc(
            profit_stack_copper
        )

        data = {
            "gear_stack_buy_g": buy_stack_g,
            "gear_stack_buy_s": buy_stack_s,
            "gear_stack_buy_c": buy_stack_c,
            "lucent_mote_sell_g": lucent_mote_stack_sell_g,
            "lucent_mote_sell_s": lucent_mote_stack_sell_s,
            "lucent_mote_sell_c": lucent_mote_stack_sell_c,
            "mithril_sell_g": mithril_stack_sell_g,
            "mithril_sell_s": mithril_stack_sell_s,
            "mithril_sell_c": mithril_stack_sell_c,
            "elder_wood_sell_g": elder_wood_stack_sell_g,
            "elder_wood_sell_s": elder_wood_stack_sell_s,
            "elder_wood_sell_c": elder_wood_stack_sell_c,
            "thick_leather_sell_g": thick_leather_stack_sell_g,
            "thick_leather_sell_s": thick_leather_stack_sell_s,
            "thick_leather_sell_c": thick_leather_stack_sell_c,
            "profit_stack_g": profit_stack_g,
            "profit_stack_s": profit_stack_s,
            "profit_stack_c": profit_stack_c,
        }
        return jsonify(data)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)
