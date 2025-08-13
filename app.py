from __future__ import annotations

import os
from typing import Any
from typing import Dict
from typing import Tuple

import httpx
import uvicorn
from fastapi import FastAPI
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from flask import Flask
from flask import render_template_string
from starlette.applications import Starlette
from starlette.middleware.wsgi import WSGIMiddleware
from starlette.routing import Mount

from html_template import HTML_PAGE
from items import ANCIENT_WOOD_ID
from items import BARBED_THORN_ID
from items import CHARGED_LOADSTONE_ID
from items import CHARM_OF_BRILLIANCE_ID
from items import CHARM_OF_POTENCE_ID
from items import CHARM_OF_SKILL_ID
from items import COMMON_GEAR_ID
from items import DRAGONHUNTER_RUNE_ID
from items import ECTOPLASM_ID
from items import ELABORATE_TOTEM_ID
from items import ELDER_WOOD_ID
from items import ELDER_WOOD_LOG_ID
from items import ELDER_WOOD_PLANK_ID
from items import EVERGREEN_LOADSTONE_ID
from items import GOSSAMER_SCRAP_ID
from items import GUARD_RUNE
from items import HARDENED_LEATHER_ID
from items import INTRICATE_TOTEM_ID
from items import LARGE_BONE_ID
from items import LARGE_CLAW_ID
from items import LARGE_FANG_ID
from items import LUCENT_MOTE_ID
from items import MIRTHIL_ID
from items import MITHRIL_INGOT_ID
from items import MITHRIL_ORE_ID
from items import ORICHALCUM_ID
from items import PILE_OF_LUCENT_CRYSTAL_ID
from items import POTENT_BLOOD_ID
from items import RARE_UNID_GEAR_ID
from items import RELIC_OF_FIREWORKS_ID
from items import SCHOLAR_RUNE_ID
from items import SILK_SCRAP_ID
from items import SYMBOL_OF_CONTROL_ID
from items import SYMBOL_OF_ENH_ID
from items import SYMBOL_OF_PAIN_ID
from items import THICK_LEATHER_ID
from items import UNID_GEAR_ID


GW2_COMMERCE_URL: str = "https://api.guildwars2.com/v2/commerce/prices"
GW2BLTC_API_URL: str = "https://www.gw2bltc.com/api/v2/tp/history"
GW2_SELL_TAX_RATE: float = 0.85

fastapi_app = FastAPI()
flask_app = Flask(__name__)
port = int(os.environ.get("PORT", "8000"))


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
) -> dict[int, dict[str, Any]]:
    params = {"ids": ",".join(str(i) for i in item_ids)}
    with httpx.Client() as client:
        response = client.get(GW2_COMMERCE_URL, params=params, timeout=10.0)
    response.raise_for_status()
    data = response.json()
    if not isinstance(data, list) or len(data) == 0:
        raise RuntimeError("No items found")  # noqa: EM101

    fetched_data: dict[int, dict[str, Any]] = {}
    for item in data:
        item_id = int(item["id"])
        buy_price = int(item["buys"]["unit_price"])
        sell_price = int(item["sells"]["unit_price"])
        flip_profit = round(sell_price * GW2_SELL_TAX_RATE, 6) - buy_price
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
            "sell_after_taxes_g": int(sell_price * GW2_SELL_TAX_RATE // 10000),
            "sell_after_taxes_s": int(
                (sell_price * GW2_SELL_TAX_RATE % 10000) // 100
            ),
            "sell_after_taxes_c": int(sell_price * GW2_SELL_TAX_RATE % 100),
        }
    return fetched_data


def get_unid_gear_data(gear_id: int) -> tuple[dict, ...] | None:
    try:
        fetched_data = fetch_tp_prices(
            [
                gear_id,
                ECTOPLASM_ID,
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
            ],
        )
    except Exception:
        return None

    gear_data = fetched_data[gear_id]

    ecto_data = fetched_data[ECTOPLASM_ID]
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

    return (
        ecto_data,
        gear_data,
        lucent_mote_data,
        mithril_data,
        elder_wood_data,
        thick_leather_data,
        gossamer_scrap_data,
        silk_scrap_data,
        hardened_data,
        ancient_wood_data,
        symbol_of_enh_data,
        symbol_of_pain_data,
        orichalcum_data,
        symbol_of_control_data,
        charm_of_brilliance_data,
        charm_of_potence_data,
        charm_of_skill_data,
    )


@flask_app.route("/")
def index() -> str:
    return render_template_string(HTML_PAGE)


@fastapi_app.get("/price")
async def get_price(item_id: int) -> JSONResponse:
    try:
        with flask_app.app_context():
            data = fetch_tp_prices([item_id])
            return JSONResponse(content=jsonable_encoder(data[item_id]))
    except Exception as e:
        return JSONResponse(content=jsonable_encoder({"error": str(e)}))


@fastapi_app.get("/rare_gear_salvage")
def get_rare_gear_salvage() -> JSONResponse:
    data_tpl = get_unid_gear_data(gear_id=RARE_UNID_GEAR_ID)
    if data_tpl is None:
        return JSONResponse(content=jsonable_encoder({"error"}))

    (
        ecto_data,
        gear_data,
        lucent_mote_data,
        mithril_data,
        elder_wood_data,
        thick_leather_data,
        gossamer_scrap_data,
        silk_scrap_data,
        hardened_data,
        ancient_wood_data,
        symbol_of_enh_data,
        symbol_of_pain_data,
        orichalcum_data,
        symbol_of_control_data,
        charm_of_brilliance_data,
        charm_of_potence_data,
        charm_of_skill_data,
    ) = data_tpl

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

    mats_value_after_taxes = (
        mithril_copper * (250.0 * 0.4879) * GW2_SELL_TAX_RATE
        + elder_wood_copper * (250.0 * 0.3175) * GW2_SELL_TAX_RATE
        + silk_scrap_data_sell_copper * (250.0 * 0.3367) * GW2_SELL_TAX_RATE
        + thick_leather_data_sell_copper * (250.0 * 0.3457) * GW2_SELL_TAX_RATE
        + orichalcum_data_sell_copper * (250.0 * 0.041) * GW2_SELL_TAX_RATE
        + ancient_wood_data_sell_copper * (250.0 * 0.0249) * GW2_SELL_TAX_RATE
        + gossamer_scrap_data_sell_copper * (250.0 * 0.018) * GW2_SELL_TAX_RATE
        + hardened_data_sell_copper * (250.0 * 0.0162) * GW2_SELL_TAX_RATE
        + ecto_sellcopper * (250.0 * 0.8761) * GW2_SELL_TAX_RATE
        + lucent_mote_copper * (250.0 * 0.2387) * GW2_SELL_TAX_RATE
        + symbol_of_control_sell_copper * (250.0 * 0.001) * GW2_SELL_TAX_RATE
        + symbol_of_enh_data_sell_copper * (250.0 * 0.0003) * GW2_SELL_TAX_RATE
        + symbol_of_pain_data_sell_copper * (250.0 * 0.0004) * GW2_SELL_TAX_RATE
        + charm_of_brilliance_sell_copper * (250.0 * 0.0006) * GW2_SELL_TAX_RATE
        + charm_of_potence_sell_copper * (250.0 * 0.0009) * GW2_SELL_TAX_RATE
        + charm_of_skilldata_sell_copper * (250.0 * 0.0009) * GW2_SELL_TAX_RATE
    )

    salvage_costs = 250 * 60  # Silver Fed

    profit_stack_copper = (
        mats_value_after_taxes - buy_stack_copper - salvage_costs
    )

    data = {
        **get_sub_dict("stack_buy", buy_stack_copper),
        **get_sub_dict("salvage_costs", salvage_costs),
        **get_sub_dict("mats_value_after_taxes", mats_value_after_taxes),
        **get_sub_dict("profit_stack", profit_stack_copper),
    }
    return JSONResponse(content=jsonable_encoder(data))


@fastapi_app.get("/rare_weapon_craft")
def get_rare_weapon_craft() -> JSONResponse:
    try:
        fetched_data = fetch_tp_prices(
            [
                ECTOPLASM_ID,
                MITHRIL_INGOT_ID,
                MITHRIL_ORE_ID,
                ELDER_WOOD_PLANK_ID,
                ELDER_WOOD_LOG_ID,
                LARGE_CLAW_ID,
                POTENT_BLOOD_ID,
                LARGE_BONE_ID,
                INTRICATE_TOTEM_ID,
                LARGE_FANG_ID,
            ],
        )
    except Exception as e:
        return JSONResponse(content=jsonable_encoder({"error": str(e)}))

    ecto_sell_after_taxes_copper = (
        fetched_data[ECTOPLASM_ID]["sell_copper"] * GW2_SELL_TAX_RATE
    )
    mithril_ore_buy = fetched_data[MITHRIL_ORE_ID]["buy_copper"]
    mithril_ingot_buy = fetched_data[MITHRIL_INGOT_ID]["buy_copper"]
    elder_wood_log_buy = fetched_data[ELDER_WOOD_LOG_ID]["buy_copper"]
    elder_wood_plank_buy = fetched_data[ELDER_WOOD_PLANK_ID]["buy_copper"]
    large_claw_buy = fetched_data[LARGE_CLAW_ID]["buy_copper"]
    potent_blood_buy = fetched_data[POTENT_BLOOD_ID]["buy_copper"]
    large_bone_buy = fetched_data[LARGE_BONE_ID]["buy_copper"]
    intricate_totem_buy = fetched_data[INTRICATE_TOTEM_ID]["buy_copper"]
    large_fang_buy = fetched_data[LARGE_FANG_ID]["buy_copper"]

    lowest_t5_mat = min(
        large_claw_buy,
        potent_blood_buy,
        large_bone_buy,
        intricate_totem_buy,
        large_fang_buy,
    )

    crafting_cost_ingot = (
        mithril_ingot_buy
        if mithril_ingot_buy < 2.0 * mithril_ore_buy
        else mithril_ore_buy * 2.0
    )
    crafting_cost_plank = (
        elder_wood_plank_buy
        if elder_wood_plank_buy < 3.0 * elder_wood_log_buy
        else elder_wood_log_buy * 3.0
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
        **get_sub_dict(
            "ecto_sell_after_taxes",
            ecto_sell_after_taxes_copper,
        ),
        **get_sub_dict("profit", rare_gear_craft_profit_copper),
    }

    return JSONResponse(content=jsonable_encoder(data))


@fastapi_app.get("/t5_mats_buy")
def get_t5_mats_buy() -> JSONResponse:
    try:
        fetched_data = fetch_tp_prices(
            [
                LARGE_CLAW_ID,
                POTENT_BLOOD_ID,
                LARGE_BONE_ID,
                INTRICATE_TOTEM_ID,
                LARGE_FANG_ID,
            ],
        )
    except Exception as e:
        return JSONResponse(content=jsonable_encoder({"error": str(e)}))

    large_claw_buy = fetched_data[LARGE_CLAW_ID]["buy_copper"]
    potent_blood_buy = fetched_data[POTENT_BLOOD_ID]["buy_copper"]
    large_bone_buy = fetched_data[LARGE_BONE_ID]["buy_copper"]
    intricate_totem_buy = fetched_data[INTRICATE_TOTEM_ID]["buy_copper"]
    large_fang_buy = fetched_data[LARGE_FANG_ID]["buy_copper"]

    data = {
        **get_sub_dict("large_claw_buy", large_claw_buy),
        **get_sub_dict("potent_blood_buy", potent_blood_buy),
        **get_sub_dict("large_bone_buy", large_bone_buy),
        **get_sub_dict(
            "intricate_totem_buy",
            intricate_totem_buy,
        ),
        **get_sub_dict("large_fang_buy", large_fang_buy),
    }

    return JSONResponse(content=jsonable_encoder(data))


@fastapi_app.get("/mats_crafting_compare")
def get_mats_crafting_compare() -> JSONResponse:
    try:
        fetched_data = fetch_tp_prices(
            [
                MITHRIL_INGOT_ID,
                MITHRIL_ORE_ID,
                ELDER_WOOD_PLANK_ID,
                ELDER_WOOD_LOG_ID,
                LUCENT_MOTE_ID,
                PILE_OF_LUCENT_CRYSTAL_ID,
            ],
        )
    except Exception as e:
        return JSONResponse(content=jsonable_encoder({"error": str(e)}))

    mithril_ore_buy = fetched_data[MITHRIL_ORE_ID]["buy_copper"]
    mithril_ingot_buy = fetched_data[MITHRIL_INGOT_ID]["buy_copper"]
    elder_wood_log_buy = fetched_data[ELDER_WOOD_LOG_ID]["buy_copper"]
    elder_wood_plank_buy = fetched_data[ELDER_WOOD_PLANK_ID]["buy_copper"]
    lucent_mote_buy = fetched_data[LUCENT_MOTE_ID]["buy_copper"]
    lucent_crystal_buy = fetched_data[PILE_OF_LUCENT_CRYSTAL_ID]["buy_copper"]

    lucent_mote_to_crystal = lucent_mote_buy * 10.0

    data = {
        **get_sub_dict(
            "mithril_ore_to_ingot",
            mithril_ore_buy * 2.0,
        ),
        **get_sub_dict("mithril_ingot_buy", mithril_ingot_buy),
        **get_sub_dict(
            "elder_wood_log_to_plank",
            elder_wood_log_buy * 3.0,
        ),
        **get_sub_dict("elder_wood_plank_buy", elder_wood_plank_buy),
        **get_sub_dict("lucent_mote_to_crystal", lucent_mote_to_crystal),
        **get_sub_dict("lucent_crystal_buy", lucent_crystal_buy),
    }

    return JSONResponse(content=jsonable_encoder(data))


@fastapi_app.get("/scholar_rune")
def get_scholar_rune() -> JSONResponse:
    try:
        fetched_data = fetch_tp_prices(
            [
                ECTOPLASM_ID,
                ELABORATE_TOTEM_ID,
                PILE_OF_LUCENT_CRYSTAL_ID,
                CHARM_OF_BRILLIANCE_ID,
                LUCENT_MOTE_ID,
                SCHOLAR_RUNE_ID,
            ],
        )
    except Exception as e:
        return JSONResponse(content=jsonable_encoder({"error": str(e)}))

    ecto_data = fetched_data[ECTOPLASM_ID]["buy_copper"]
    totem_data = fetched_data[ELABORATE_TOTEM_ID]["buy_copper"]
    lucent_crystal_data = fetched_data[PILE_OF_LUCENT_CRYSTAL_ID]["buy_copper"]
    charm_data = fetched_data[CHARM_OF_BRILLIANCE_ID]["buy_copper"]
    lucent_mote_data = fetched_data[LUCENT_MOTE_ID]["buy_copper"]
    scholar_rune_sell_copper = fetched_data[SCHOLAR_RUNE_ID]["sell_copper"]

    crafting_cost_copper = (
        ecto_data * 5.0
        + totem_data * 5.0
        + lucent_crystal_data * 8.0
        + charm_data * 2.0
    )
    crafting_cost2_copper = (
        ecto_data * 5.0
        + totem_data * 5.0
        + lucent_mote_data * 80.0
        + charm_data * 2.0
    )

    profit = scholar_rune_sell_copper * GW2_SELL_TAX_RATE - crafting_cost_copper
    profit2 = (
        scholar_rune_sell_copper * GW2_SELL_TAX_RATE - crafting_cost2_copper
    )

    cheapest_crafting_cost = min(crafting_cost_copper, crafting_cost2_copper)
    highest_profit = max(profit, profit2)

    data = {
        **get_sub_dict("crafting_cost", cheapest_crafting_cost),
        **get_sub_dict("sell", scholar_rune_sell_copper),
        **get_sub_dict("profit", highest_profit),
    }

    return JSONResponse(content=jsonable_encoder(data))


@fastapi_app.get("/dragonhunter_rune")
def get_dragonhunter_rune() -> JSONResponse:
    try:
        fetched_data = fetch_tp_prices(
            [
                GUARD_RUNE,
                DRAGONHUNTER_RUNE_ID,
                EVERGREEN_LOADSTONE_ID,
                BARBED_THORN_ID,
                PILE_OF_LUCENT_CRYSTAL_ID,
                CHARGED_LOADSTONE_ID,
                CHARM_OF_POTENCE_ID,
                ECTOPLASM_ID,
            ],
        )
    except Exception as e:
        return JSONResponse(content=jsonable_encoder({"error": str(e)}))

    rune_sell_copper = fetched_data[DRAGONHUNTER_RUNE_ID]["sell_copper"]
    evergreen_loadstone_buy = fetched_data[EVERGREEN_LOADSTONE_ID]["buy_copper"]
    charged_loadstone_sell = fetched_data[CHARGED_LOADSTONE_ID]["sell_copper"]
    thorns_buy = fetched_data[BARBED_THORN_ID]["buy_copper"]
    charm_buy = fetched_data[CHARM_OF_POTENCE_ID]["buy_copper"]
    ecto_buy = fetched_data[ECTOPLASM_ID]["buy_copper"]
    lucent_crystal_buy = fetched_data[PILE_OF_LUCENT_CRYSTAL_ID]["buy_copper"]

    guardian_rune_cost = (
        charged_loadstone_sell
        + charm_buy
        + ecto_buy * 5.0
        + lucent_crystal_buy * 12.0
    )

    crafting_cost_copper = (
        guardian_rune_cost * 1.0
        + evergreen_loadstone_buy * 1.0
        + thorns_buy * 10.0
    )

    profit = rune_sell_copper * GW2_SELL_TAX_RATE - crafting_cost_copper

    data = {
        **get_sub_dict("guardian_crafting_cost", guardian_rune_cost),
        **get_sub_dict("crafting_cost", crafting_cost_copper),
        **get_sub_dict("sell", rune_sell_copper),
        **get_sub_dict("profit", profit),
    }

    return JSONResponse(content=jsonable_encoder(data))


@fastapi_app.get("/relic_of_fireworks")
def get_relic_of_fireworks() -> JSONResponse:
    try:
        fetched_data = fetch_tp_prices(
            [
                ECTOPLASM_ID,
                PILE_OF_LUCENT_CRYSTAL_ID,
                CHARM_OF_SKILL_ID,
                LUCENT_MOTE_ID,
                RELIC_OF_FIREWORKS_ID,
            ],
        )
    except Exception as e:
        return JSONResponse(content=jsonable_encoder({"error": str(e)}))

    ecto_price_copper = fetched_data[ECTOPLASM_ID]["buy_copper"]
    lucent_crystal_price_copper = fetched_data[PILE_OF_LUCENT_CRYSTAL_ID][
        "buy_copper"
    ]
    charm_price_copper = fetched_data[CHARM_OF_SKILL_ID]["buy_copper"]
    lucent_mote_price_copper = fetched_data[LUCENT_MOTE_ID]["buy_copper"]
    relic_of_fireworks_sell_copper = fetched_data[RELIC_OF_FIREWORKS_ID][
        "sell_copper"
    ]

    crafting_cost_copper = (
        ecto_price_copper * 15.0
        + lucent_crystal_price_copper * 48.0
        + charm_price_copper * 3.0
    )
    crafting_cost2_copper = (
        ecto_price_copper * 15.0
        + lucent_mote_price_copper * 480.0
        + charm_price_copper * 3.0
    )

    profit = (
        relic_of_fireworks_sell_copper * GW2_SELL_TAX_RATE
        - crafting_cost_copper
    )
    profit2 = (
        relic_of_fireworks_sell_copper * GW2_SELL_TAX_RATE
        - crafting_cost2_copper
    )

    cheapest_crafting_cost_copper = min(
        crafting_cost_copper, crafting_cost2_copper
    )
    highest_profit = max(profit, profit2)

    data = {
        **get_sub_dict(
            "crafting_cost",
            cheapest_crafting_cost_copper,
        ),
        **get_sub_dict("sell", relic_of_fireworks_sell_copper),
        **get_sub_dict("profit", highest_profit),
    }

    return JSONResponse(content=jsonable_encoder(data))


@fastapi_app.get("/common_gear_salvage")
def get_common_gear_salvage() -> JSONResponse:
    data_tpl = get_unid_gear_data(gear_id=COMMON_GEAR_ID)
    if data_tpl is None:
        return JSONResponse(content=jsonable_encoder({"error"}))

    (
        ecto_data,
        gear_data,
        lucent_mote_data,
        mithril_data,
        elder_wood_data,
        thick_leather_data,
        gossamer_scrap_data,
        silk_scrap_data,
        hardened_data,
        ancient_wood_data,
        symbol_of_enh_data,
        symbol_of_pain_data,
        orichalcum_data,
        symbol_of_control_data,
        charm_of_brilliance_data,
        charm_of_potence_data,
        charm_of_skill_data,
    ) = data_tpl

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

    mats_value_after_taxes = (
        mithril_copper * (250.0 * 0.4291) * GW2_SELL_TAX_RATE
        + elder_wood_copper * (250.0 * 0.3884) * GW2_SELL_TAX_RATE
        + silk_scrap_data_sell_copper * (250.0 * 0.3059) * GW2_SELL_TAX_RATE
        + thick_leather_data_sell_copper * (250.0 * 0.2509) * GW2_SELL_TAX_RATE
        + orichalcum_data_sell_copper * (250.0 * 0.0394) * GW2_SELL_TAX_RATE
        + ancient_wood_data_sell_copper * (250.0 * 0.0305) * GW2_SELL_TAX_RATE
        + gossamer_scrap_data_sell_copper * (250.0 * 0.0153) * GW2_SELL_TAX_RATE
        + hardened_data_sell_copper * (250.0 * 0.0143) * GW2_SELL_TAX_RATE
        + ecto_sellcopper * (250.0 * 0.0095) * GW2_SELL_TAX_RATE
        + lucent_mote_copper * (250.0 * 0.1083) * GW2_SELL_TAX_RATE
        + symbol_of_control_sell_copper * (250.0 * 0.0002) * GW2_SELL_TAX_RATE
        + symbol_of_enh_data_sell_copper * (250.0 * 0.0006) * GW2_SELL_TAX_RATE
        + symbol_of_pain_data_sell_copper * (250.0 * 0.0005) * GW2_SELL_TAX_RATE
        + charm_of_brilliance_sell_copper * (250.0 * 0.0004) * GW2_SELL_TAX_RATE
        + charm_of_potence_sell_copper * (250.0 * 0.0003) * GW2_SELL_TAX_RATE
        + charm_of_skilldata_sell_copper * (250.0 * 0.0003) * GW2_SELL_TAX_RATE
    )

    salvage_costs = (
        3.0 * 223  # Copper Fed
        + 30.0 * 25  # Runecrafter
        + 60 * 2  # Silver Fed
    )

    profit_stack_copper = (
        mats_value_after_taxes - buy_stack_copper - salvage_costs
    )

    data = {
        **get_sub_dict("stack_buy", buy_stack_copper),
        **get_sub_dict("salvage_costs", salvage_costs),
        **get_sub_dict("mats_value_after_taxes", mats_value_after_taxes),
        **get_sub_dict("profit_stack", profit_stack_copper),
    }
    return JSONResponse(content=jsonable_encoder(data))


@fastapi_app.get("/gear_salvage")
def get_gear_salvage() -> JSONResponse:
    data_tpl = get_unid_gear_data(gear_id=UNID_GEAR_ID)
    if data_tpl is None:
        return JSONResponse(content=jsonable_encoder({"error"}))

    (
        ecto_data,
        gear_data,
        lucent_mote_data,
        mithril_data,
        elder_wood_data,
        thick_leather_data,
        gossamer_scrap_data,
        silk_scrap_data,
        hardened_data,
        ancient_wood_data,
        symbol_of_enh_data,
        symbol_of_pain_data,
        orichalcum_data,
        symbol_of_control_data,
        charm_of_brilliance_data,
        charm_of_potence_data,
        charm_of_skill_data,
    ) = data_tpl

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

    mats_value_after_taxes = (
        mithril_copper * (250.0 * 0.4299) * GW2_SELL_TAX_RATE
        + elder_wood_copper * (250.0 * 0.3564) * GW2_SELL_TAX_RATE
        + silk_scrap_data_sell_copper * (250.0 * 0.3521) * GW2_SELL_TAX_RATE
        + thick_leather_data_sell_copper * (250.0 * 0.2673) * GW2_SELL_TAX_RATE
        + orichalcum_data_sell_copper * (250.0 * 0.0387) * GW2_SELL_TAX_RATE
        + ancient_wood_data_sell_copper * (250.0 * 0.0287) * GW2_SELL_TAX_RATE
        + gossamer_scrap_data_sell_copper * (250.0 * 0.018) * GW2_SELL_TAX_RATE
        + hardened_data_sell_copper * (250.0 * 0.0169) * GW2_SELL_TAX_RATE
        + ecto_sellcopper * (250.0 * 0.0296) * GW2_SELL_TAX_RATE
        + lucent_mote_copper * (250.0 * 0.98) * GW2_SELL_TAX_RATE
        + symbol_of_control_sell_copper * (250.0 * 0.0018) * GW2_SELL_TAX_RATE
        + symbol_of_enh_data_sell_copper * (250.0 * 0.001) * GW2_SELL_TAX_RATE
        + symbol_of_pain_data_sell_copper * (250.0 * 0.0006) * GW2_SELL_TAX_RATE
        + charm_of_brilliance_sell_copper * (250.0 * 0.0042) * GW2_SELL_TAX_RATE
        + charm_of_potence_sell_copper * (250.0 * 0.0029) * GW2_SELL_TAX_RATE
        + charm_of_skilldata_sell_copper * (250.0 * 0.0028) * GW2_SELL_TAX_RATE
    )

    salvage_costs = 30.0 * 245 + 60 * 5

    profit_stack_copper = (
        mats_value_after_taxes - buy_stack_copper - salvage_costs
    )

    data = {
        **get_sub_dict("stack_buy", buy_stack_copper),
        **get_sub_dict("salvage_costs", salvage_costs),
        **get_sub_dict("mats_value_after_taxes", mats_value_after_taxes),
        **get_sub_dict("profit_stack", profit_stack_copper),
    }
    return JSONResponse(content=jsonable_encoder(data))


@fastapi_app.get("/t5_mats_sell")
def get_t5_mats_sell() -> JSONResponse:
    try:
        fetched_data = fetch_tp_prices(
            [
                LUCENT_MOTE_ID,
                MIRTHIL_ID,
                ELDER_WOOD_ID,
                THICK_LEATHER_ID,
            ],
        )
    except Exception as e:
        return JSONResponse(content=jsonable_encoder({"error": str(e)}))

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
            "thick_leather_sell",
            thick_leather_data_sell_copper * 250.0,
        ),
    }
    return JSONResponse(content=jsonable_encoder(data))


app = Starlette(
    routes=[
        Mount("/api", app=fastapi_app),
        Mount("/", app=WSGIMiddleware(flask_app)),
    ],
)

if __name__ == "__main__":
    uvicorn.run(
        "flask_fastapi_shared:app",
        host="0.0.0.0",  # noqa: S104
        port=port,
        reload=True,
    )
