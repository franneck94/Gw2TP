from __future__ import annotations

import os
from typing import Any, Dict, Tuple

import httpx
import uvicorn
from fastapi import FastAPI
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from flask import Flask, render_template_string
from starlette.applications import Starlette
from starlette.middleware.wsgi import WSGIMiddleware
from starlette.routing import Mount

from html_template import HTML_PAGE
from items import (
    ANCIENT_WOOD_ID,
    CHARM_OF_BRILLIANCE_ID,
    CHARM_OF_POTENCE_ID,
    CHARM_OF_SKILL_ID,
    COMMON_GEAR_ID,
    ECTO_ITEM_ID,
    ELABORATE_TOTEM_ID,
    ELDER_WOOD_ID,
    ELDER_WOOD_LOG_ID,
    ELDER_WOOD_PLANK_ID,
    GOSSAMER_SCRAP_ID,
    HARDENED_LEATHER_ID,
    INTRICATE_TOTEM_ID,
    LARGE_BONE_ID,
    LARGE_CLAW_ID,
    LARGE_FANG_ID,
    LUCENT_MOTE_ID,
    MIRTHIL_ID,
    MITHRIL_INGOT_ID,
    MITHRIL_ORE_ID,
    ORICHALCUM_ID,
    PILE_OF_LUCENT_CRYSTAL_ID,
    POTENT_BLOOD_ID,
    RARE_UNID_ITEM_ID,
    RELIC_OF_FIREWORKS_ID,
    SCHOLAR_RUNE_ID,
    SILK_SCRAP_ID,
    SYMBOL_OF_CONTROL_ID,
    SYMBOL_OF_ENH_ID,
    SYMBOL_OF_PAIN_ID,
    THICK_LEATHER_ID,
    UNID_ITEM_ID,
)

GW2_COMMERCE_URL: str = "https://api.guildwars2.com/v2/commerce/prices"

fastapi_app = FastAPI()
flask_app = Flask(__name__)
port = int(os.environ.get("PORT", 8000))


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


def get_sub_dict(item_name: str, copper_price: int) -> Dict[str, Any]:
    g, s, c = copper_to_gsc(copper_price)
    return {
        f"{item_name}_g": g,
        f"{item_name}_s": s,
        f"{item_name}_c": c,
    }


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

    fetched_data: dict[int, dict[str, any]] = {}
    for item in data:
        item_id = int(item["id"])
        buy_price = int(item["buys"]["unit_price"])
        sell_price = int(item["sells"]["unit_price"])
        flip_profit = round(sell_price * 0.85, 6) - buy_price
        buy_g, buy_s, buy_c = copper_to_gsc(buy_price)
        sell_g, sell_s, sell_c = copper_to_gsc(sell_price)
        flip_g, flip_s, flip_c = copper_to_gsc(flip_profit)

        fetched_data[item_id] = {
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
    return fetched_data


@flask_app.route("/")
def index() -> str:
    return render_template_string(HTML_PAGE)


@fastapi_app.get("/price")
async def get_price(item_id: int):
    try:
        with flask_app.app_context():
            data = fetch_tp_prices([item_id])
            return JSONResponse(content=jsonable_encoder(data[item_id]))
    except Exception as e:
        return JSONResponse(content=jsonable_encoder({"error": str(e)}))


@fastapi_app.get("/gear_to_ecto")
def get_gear_to_ecto() -> Any:
    try:
        fetched_data = fetch_tp_prices([ECTO_ITEM_ID, RARE_UNID_ITEM_ID])
        ecto_data = fetched_data[ECTO_ITEM_ID]
        rare_gear_data = fetched_data[RARE_UNID_ITEM_ID]
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
            "buy_g": rare_gear_data["buy_g"],
            "buy_s": rare_gear_data["buy_s"],
            "buy_c": rare_gear_data["buy_c"],
            "gear_to_ecto_profit_g": profit_g,
            "gear_to_ecto_profit_s": profit_s,
            "gear_to_ecto_profit_c": profit_c,
        }

        return JSONResponse(content=jsonable_encoder(data))
    except Exception as e:
        return JSONResponse(content=jsonable_encoder({"error": str(e)}))


@fastapi_app.get("/rare_weapon_craft")
def get_rare_weapon_craft() -> Any:
    try:
        fetched_data = fetch_tp_prices(
            [
                ECTO_ITEM_ID,
                MITHRIL_INGOT_ID,
                MITHRIL_ORE_ID,
                ELDER_WOOD_PLANK_ID,
                ELDER_WOOD_LOG_ID,
                LARGE_CLAW_ID,
                POTENT_BLOOD_ID,
                LARGE_BONE_ID,
                INTRICATE_TOTEM_ID,
                LARGE_FANG_ID,
            ]
        )
        ecto_sell_after_taxes_copper = fetched_data[ECTO_ITEM_ID]["sell_copper"] * 0.85
        mithril_ore_buy_copper = fetched_data[MITHRIL_ORE_ID]["buy_copper"]
        mithril_ingot_buy_copper = fetched_data[MITHRIL_INGOT_ID]["buy_copper"]
        elder_wood_log_buy_copper = fetched_data[ELDER_WOOD_LOG_ID]["buy_copper"]
        elder_wood_plank_buy_copper = fetched_data[ELDER_WOOD_PLANK_ID]["buy_copper"]
        large_claw_buy_copper = fetched_data[LARGE_CLAW_ID]["buy_copper"]
        potent_blood_buy_copper = fetched_data[POTENT_BLOOD_ID]["buy_copper"]
        large_bone_buy_copper = fetched_data[LARGE_BONE_ID]["buy_copper"]
        intricate_totem_buy_copper = fetched_data[INTRICATE_TOTEM_ID]["buy_copper"]
        large_fang_buy_copper = fetched_data[LARGE_FANG_ID]["buy_copper"]

        lowest_t5_mat = min(
            large_claw_buy_copper,
            potent_blood_buy_copper,
            large_bone_buy_copper,
            intricate_totem_buy_copper,
            large_fang_buy_copper,
        )

        crafting_cost_ingot = (
            mithril_ingot_buy_copper
            if mithril_ingot_buy_copper < 2.0 * mithril_ore_buy_copper
            else mithril_ore_buy_copper * 2.0
        )
        crafting_cost_plank = (
            elder_wood_plank_buy_copper
            if elder_wood_plank_buy_copper < 3.0 * elder_wood_log_buy_copper
            else elder_wood_log_buy_copper * 3.0
        )

        crafting_cost_backing = 2.0 * crafting_cost_ingot
        crafting_cost_boss = 2.0 * crafting_cost_ingot
        crafting_cost_dowwl = 2.0 * crafting_cost_plank + 3.0 * crafting_cost_ingot
        crafting_cost_inscr = 15.0 * lowest_t5_mat + 2.0 * crafting_cost_dowwl

        crafting_cost_with_cheap_materials = (
            crafting_cost_inscr + crafting_cost_backing + crafting_cost_boss
        )
        rare_gear_craft_profit_copper = (
            ecto_sell_after_taxes_copper * 0.9
        ) - crafting_cost_with_cheap_materials

        data = {
            **get_sub_dict("crafting_cost", crafting_cost_with_cheap_materials),
            **get_sub_dict("ecto_sell_after_taxes", ecto_sell_after_taxes_copper),
            **get_sub_dict("profit", rare_gear_craft_profit_copper),
        }

        return JSONResponse(content=jsonable_encoder(data))
    except Exception as e:
        return JSONResponse(content=jsonable_encoder({"error": str(e)}))


@fastapi_app.get("/t5_mats_buy")
def get_t5_mats_buy() -> Any:
    try:
        fetched_data = fetch_tp_prices(
            [
                MITHRIL_INGOT_ID,
                MITHRIL_ORE_ID,
                ELDER_WOOD_PLANK_ID,
                ELDER_WOOD_LOG_ID,
                LARGE_CLAW_ID,
                POTENT_BLOOD_ID,
                LARGE_BONE_ID,
                INTRICATE_TOTEM_ID,
                LARGE_FANG_ID,
            ]
        )
        mithril_ore_buy_copper = fetched_data[MITHRIL_ORE_ID]["buy_copper"]
        mithril_ingot_buy_copper = fetched_data[MITHRIL_INGOT_ID]["buy_copper"]
        elder_wood_log_buy_copper = fetched_data[ELDER_WOOD_LOG_ID]["buy_copper"]
        elder_wood_plank_buy_copper = fetched_data[ELDER_WOOD_PLANK_ID]["buy_copper"]
        large_claw_buy_copper = fetched_data[LARGE_CLAW_ID]["buy_copper"]
        potent_blood_buy_copper = fetched_data[POTENT_BLOOD_ID]["buy_copper"]
        large_bone_buy_copper = fetched_data[LARGE_BONE_ID]["buy_copper"]
        intricate_totem_buy_copper = fetched_data[INTRICATE_TOTEM_ID]["buy_copper"]
        large_fang_buy_copper = fetched_data[LARGE_FANG_ID]["buy_copper"]

        data = {
            **get_sub_dict("mithril_ore_to_ingot", mithril_ore_buy_copper * 2.0),
            **get_sub_dict("mithril_ingot_buy", mithril_ingot_buy_copper),
            **get_sub_dict("elder_wood_log_to_plank", elder_wood_log_buy_copper * 3.0),
            **get_sub_dict("elder_wood_plank_buy", elder_wood_plank_buy_copper),
            **get_sub_dict("large_claw_buy_buy", large_claw_buy_copper),
            **get_sub_dict("potent_blood_buy_buy", potent_blood_buy_copper),
            **get_sub_dict("large_bone_buy_buy", large_bone_buy_copper),
            **get_sub_dict("intricate_totem_buy_buy", intricate_totem_buy_copper),
            **get_sub_dict("large_fang_buy_buy", large_fang_buy_copper),
        }

        return JSONResponse(content=jsonable_encoder(data))
    except Exception as e:
        return JSONResponse(content=jsonable_encoder({"error": str(e)}))


@fastapi_app.get("/scholar_rune")
def get_scholar_rune() -> Any:
    try:
        fetched_data = fetch_tp_prices(
            [
                ECTO_ITEM_ID,
                ELABORATE_TOTEM_ID,
                PILE_OF_LUCENT_CRYSTAL_ID,
                CHARM_OF_BRILLIANCE_ID,
                LUCENT_MOTE_ID,
                SCHOLAR_RUNE_ID,
            ]
        )
        ecto_data = fetched_data[ECTO_ITEM_ID]["buy_copper"]
        totem_data = fetched_data[ELABORATE_TOTEM_ID]["buy_copper"]
        lucent_crystal_data = fetched_data[PILE_OF_LUCENT_CRYSTAL_ID]["buy_copper"]
        charm_data = fetched_data[CHARM_OF_BRILLIANCE_ID]["buy_copper"]
        lucent_mote_data = fetched_data[LUCENT_MOTE_ID]["buy_copper"]
        scholar_rune_sell_copper = fetched_data[SCHOLAR_RUNE_ID]["sell_copper"]

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

        data = {
            **get_sub_dict("crafting_cost", scholar_crafting_cost_copper),
            **get_sub_dict(
                "crafting_cost_with_lucent_motes", scholar_crafting_cost2_copper
            ),
            **get_sub_dict("sell", scholar_rune_sell_copper),
            **get_sub_dict("profit", profit),
            **get_sub_dict("profit_with_lucent_motes", profit2),
        }

        return JSONResponse(content=jsonable_encoder(data))
    except Exception as e:
        return JSONResponse(content=jsonable_encoder({"error": str(e)}))


@fastapi_app.get("/relic_of_fireworks")
def get_relic_of_fireworks() -> Any:
    try:
        fetched_data = fetch_tp_prices(
            [
                ECTO_ITEM_ID,
                PILE_OF_LUCENT_CRYSTAL_ID,
                CHARM_OF_SKILL_ID,
                LUCENT_MOTE_ID,
                RELIC_OF_FIREWORKS_ID,
            ]
        )
        ecto_price_copper = fetched_data[ECTO_ITEM_ID]["buy_copper"]
        lucent_crystal_price_copper = fetched_data[PILE_OF_LUCENT_CRYSTAL_ID][
            "buy_copper"
        ]
        charm_price_copper = fetched_data[CHARM_OF_SKILL_ID]["buy_copper"]
        lucent_mote_price_copper = fetched_data[LUCENT_MOTE_ID]["buy_copper"]
        relic_of_fireworks_sell_copper = fetched_data[RELIC_OF_FIREWORKS_ID][
            "sell_copper"
        ]

        fireworks_crafting_cost_copper = (
            ecto_price_copper * 15.0
            + lucent_crystal_price_copper * 48.0
            + charm_price_copper * 3.0
        )
        fireworks_crafting_cost2_copper = (
            ecto_price_copper * 15.0
            + lucent_mote_price_copper * 480.0
            + charm_price_copper * 3.0
        )

        profit = relic_of_fireworks_sell_copper * 0.85 - fireworks_crafting_cost_copper
        profit2 = (
            relic_of_fireworks_sell_copper * 0.85 - fireworks_crafting_cost2_copper
        )

        data = {
            **get_sub_dict("fireworks_crafting_cost", fireworks_crafting_cost_copper),
            **get_sub_dict(
                "fireworks_crafting_cost_with_lucent_motes",
                fireworks_crafting_cost2_copper,
            ),
            **get_sub_dict("fireworks_sell", relic_of_fireworks_sell_copper),
            **get_sub_dict("fireworks_profit", profit),
            **get_sub_dict("fireworks_profit_with_lucent_motes", profit2),
        }

        return JSONResponse(content=jsonable_encoder(data))
    except Exception as e:
        return JSONResponse(content=jsonable_encoder({"error": str(e)}))


@fastapi_app.get("/common_gear_salvage")
def get_common_gear_salvage() -> Any:
    try:
        fetched_data = fetch_tp_prices(
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
                COMMON_GEAR_ID,
            ]
        )

        ecto_data = fetched_data[ECTO_ITEM_ID]
        gear_data = fetched_data[COMMON_GEAR_ID]
        lucent_mote_data = fetched_data[LUCENT_MOTE_ID]
        mithril_data = fetched_data[MIRTHIL_ID]
        elder_wood_data = fetched_data[ELDER_WOOD_ID]
        thick_leather_data = fetched_data[THICK_LEATHER_ID]
        gossamer_scrap_data = fetched_data[GOSSAMER_SCRAP_ID]
        silk_scrap_data = fetched_data[SILK_SCRAP_ID]
        hardened_data = fetched_data[HARDENED_LEATHER_ID]
        ancient_wood_data = fetched_data[ANCIENT_WOOD_ID]
        symbol_of_enh_data = fetched_data[SYMBOL_OF_ENH_ID]
        symbol_of_pain_data = fetched_data[SYMBOL_OF_PAIN_ID]
        orichalcum_data = fetched_data[ORICHALCUM_ID]
        symbol_of_control_data = fetched_data[SYMBOL_OF_CONTROL_ID]
        charm_of_brilliance_data = fetched_data[CHARM_OF_BRILLIANCE_ID]
        charm_of_potence_data = fetched_data[CHARM_OF_POTENCE_ID]
        charm_of_skill_data = fetched_data[CHARM_OF_SKILL_ID]

        buy_stack_copper = gear_data["buy_copper"] * 250.0
        lucent_mote_copper = lucent_mote_data["sell_copper"]
        mithril_copper = mithril_data["sell_copper"]
        elder_wood_copper = elder_wood_data["sell_copper"]
        ecto_sellcopper = ecto_data["sell_copper"]
        thick_leather_data_sell_copper = thick_leather_data["sell_copper"]

        gossamer_scrap_data_sell_copper = gossamer_scrap_data["sell_copper"]
        silk_scrap_data_sell_copper = silk_scrap_data["sell_copper"]
        hardened_data_sell_copper = hardened_data["sell_copper"]
        ancient_wood_data_sell_copper = ancient_wood_data["sell_copper"]
        symbol_of_enh_data_sell_copper = symbol_of_enh_data["sell_copper"]
        symbol_of_pain_data_sell_copper = symbol_of_pain_data["sell_copper"]
        orichalcum_data_sell_copper = orichalcum_data["sell_copper"]
        symbol_of_control_sell_copper = symbol_of_control_data["sell_copper"]
        charm_of_brilliance_sell_copper = charm_of_brilliance_data["sell_copper"]
        charm_of_potence_sell_copper = charm_of_potence_data["sell_copper"]
        charm_of_skilldata_sell_copper = charm_of_skill_data["sell_copper"]

        profit_stack_copper = (
            mithril_copper * (250.0 * 0.4291) * 0.85
            + elder_wood_copper * (250.0 * 0.3884) * 0.85
            + silk_scrap_data_sell_copper * (250.0 * 0.3059) * 0.85
            + thick_leather_data_sell_copper * (250.0 * 0.2509) * 0.85
            + orichalcum_data_sell_copper * (250.0 * 0.0394) * 0.85
            + ancient_wood_data_sell_copper * (250.0 * 0.0305) * 0.85
            + gossamer_scrap_data_sell_copper * (250.0 * 0.0153) * 0.85
            + hardened_data_sell_copper * (250.0 * 0.0143) * 0.85
            + ecto_sellcopper * (250.0 * 0.0095) * 0.85
            + lucent_mote_copper * (250.0 * 0.1083) * 0.85
            + symbol_of_control_sell_copper * (250.0 * 0.0002) * 0.85
            + symbol_of_enh_data_sell_copper * (250.0 * 0.0006) * 0.85
            + symbol_of_pain_data_sell_copper * (250.0 * 0.0005) * 0.85
            + charm_of_brilliance_sell_copper * (250.0 * 0.0004) * 0.85
            + charm_of_potence_sell_copper * (250.0 * 0.0003) * 0.85
            + charm_of_skilldata_sell_copper * (250.0 * 0.0003) * 0.85
            - buy_stack_copper
            - 3.0 * 223  # Copper Fed
            - 30.0 * 25  # Runecrafter
            - 60 * 2  # Silver Fed
        )

        data = {
            **get_sub_dict("stack_buy", buy_stack_copper),
            **get_sub_dict("profit_stack", profit_stack_copper),
        }
        return JSONResponse(content=jsonable_encoder(data))
    except Exception as e:
        return JSONResponse(content=jsonable_encoder({"error": str(e)}))


@fastapi_app.get("/gear_salvage")
def get_gear_salvage() -> Any:
    try:
        fetched_data = fetch_tp_prices(
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

        ecto_data = fetched_data[ECTO_ITEM_ID]
        gear_data = fetched_data[UNID_ITEM_ID]
        lucent_mote_data = fetched_data[LUCENT_MOTE_ID]
        mithril_data = fetched_data[MIRTHIL_ID]
        elder_wood_data = fetched_data[ELDER_WOOD_ID]
        thick_leather_data = fetched_data[THICK_LEATHER_ID]
        gossamer_scrap_data = fetched_data[GOSSAMER_SCRAP_ID]
        silk_scrap_data = fetched_data[SILK_SCRAP_ID]
        hardened_data = fetched_data[HARDENED_LEATHER_ID]
        ancient_wood_data = fetched_data[ANCIENT_WOOD_ID]
        symbol_of_enh_data = fetched_data[SYMBOL_OF_ENH_ID]
        symbol_of_pain_data = fetched_data[SYMBOL_OF_PAIN_ID]
        orichalcum_data = fetched_data[ORICHALCUM_ID]
        symbol_of_control_data = fetched_data[SYMBOL_OF_CONTROL_ID]
        charm_of_brilliance_data = fetched_data[CHARM_OF_BRILLIANCE_ID]
        charm_of_potence_data = fetched_data[CHARM_OF_POTENCE_ID]
        charm_of_skill_data = fetched_data[CHARM_OF_SKILL_ID]

        buy_stack_copper = gear_data["buy_copper"] * 250.0
        lucent_mote_copper = lucent_mote_data["sell_copper"]
        mithril_copper = mithril_data["sell_copper"]
        elder_wood_copper = elder_wood_data["sell_copper"]
        ecto_sellcopper = ecto_data["sell_copper"]
        thick_leather_data_sell_copper = thick_leather_data["sell_copper"]

        gossamer_scrap_data_sell_copper = gossamer_scrap_data["sell_copper"]
        silk_scrap_data_sell_copper = silk_scrap_data["sell_copper"]
        hardened_data_sell_copper = hardened_data["sell_copper"]
        ancient_wood_data_sell_copper = ancient_wood_data["sell_copper"]
        symbol_of_enh_data_sell_copper = symbol_of_enh_data["sell_copper"]
        symbol_of_pain_data_sell_copper = symbol_of_pain_data["sell_copper"]
        orichalcum_data_sell_copper = orichalcum_data["sell_copper"]
        symbol_of_control_sell_copper = symbol_of_control_data["sell_copper"]
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
            + symbol_of_control_sell_copper * (250.0 * 0.0018) * 0.85
            + symbol_of_enh_data_sell_copper * (250.0 * 0.001) * 0.85
            + symbol_of_pain_data_sell_copper * (250.0 * 0.0006) * 0.85
            + charm_of_brilliance_sell_copper * (250.0 * 0.0042) * 0.85
            + charm_of_potence_sell_copper * (250.0 * 0.0029) * 0.85
            + charm_of_skilldata_sell_copper * (250.0 * 0.0028) * 0.85
            - buy_stack_copper
            - 30.0 * 245  # Runecrafter
            - 60 * 5  # Silver Fed
        )

        data = {
            **get_sub_dict("stack_buy", buy_stack_copper),
            **get_sub_dict("profit_stack", profit_stack_copper),
        }
        return JSONResponse(content=jsonable_encoder(data))
    except Exception as e:
        return JSONResponse(content=jsonable_encoder({"error": str(e)}))


@fastapi_app.get("/t5_mats_sell")
def get_t5_mats_sell() -> Any:
    try:
        fetched_data = fetch_tp_prices(
            [
                LUCENT_MOTE_ID,
                MIRTHIL_ID,
                ELDER_WOOD_ID,
                THICK_LEATHER_ID,
            ]
        )
        lucent_mote_data = fetched_data[LUCENT_MOTE_ID]
        mithril_data = fetched_data[MIRTHIL_ID]
        elder_wood_data = fetched_data[ELDER_WOOD_ID]
        thick_leather_data = fetched_data[THICK_LEATHER_ID]

        lucent_mote_copper = lucent_mote_data["sell_copper"]
        mithril_copper = mithril_data["sell_copper"]
        elder_wood_copper = elder_wood_data["sell_copper"]
        thick_leather_data_sell_copper = thick_leather_data["sell_copper"]

        data = {
            **get_sub_dict("lucent_mote_sell", lucent_mote_copper * 250.0),
            **get_sub_dict("mithril_sell", mithril_copper * 250.0),
            **get_sub_dict("elder_wood_sell", elder_wood_copper * 250.0),
            **get_sub_dict(
                "thick_leather_sell", thick_leather_data_sell_copper * 250.0
            ),
        }
        return JSONResponse(content=jsonable_encoder(data))
    except Exception as e:
        return JSONResponse(content=jsonable_encoder({"error": str(e)}))


app = Starlette(
    routes=[Mount("/api", app=fastapi_app), Mount("/", app=WSGIMiddleware(flask_app))]
)

if __name__ == "__main__":
    uvicorn.run(
        "flask_fastapi_shared:app",
        host="0.0.0.0",
        port=port,
        reload=True,
    )
