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
from items import ItemIDs


GW2_COMMERCE_URL: str = "https://api.guildwars2.com/v2/commerce/prices"
GW2BLTC_API_URL: str = "https://www.gw2bltc.com/api/v2/tp/history"
TAX_RATE: float = 0.85


def is_running_on_railway():  # noqa: ANN201
    return "RAILWAY_STATIC_URL" in os.environ or "PORT" in os.environ


uses_server = is_running_on_railway()
port = int(os.environ.get("PORT", "8000"))
if uses_server:
    api_base = "https://gw2tp-production.up.railway.app/api/"
else:
    api_base = "http://127.0.0.1:8000/api/"

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

    gold = int(copper // 10_000)
    silver = int((copper % 10_000) // 100)
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
    return gold * 10_000 + silver * 100 + copper


def gsc_dict_to_copper(
    dct: int,
) -> int:
    return dct["profit_g"] * 10_000 + dct["profit_s"] * 100 + dct["profit_c"]


def get_sub_dct(item_name: str, copper_price: int) -> Dict[str, Any]:
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
        flip_profit = round(sell_price * TAX_RATE, 6) - buy_price
        buy_g, buy_s, buy_c = copper_to_gsc(buy_price)
        sell_g, sell_s, sell_c = copper_to_gsc(sell_price)
        flip_g, flip_s, flip_c = copper_to_gsc(flip_profit)

        fetched_data[item_id] = {
            "buy": buy_price,
            "sell": sell_price,
            "buy_g": buy_g,
            "buy_s": buy_s,
            "buy_c": buy_c,
            "sell_g": sell_g,
            "sell_s": sell_s,
            "sell_c": sell_c,
            "flip_g": flip_g,
            "flip_s": flip_s,
            "flip_c": flip_c,
            "sell_after_tax_g": int(sell_price * TAX_RATE // 10_000),
            "sell_after_tax_s": int((sell_price * TAX_RATE % 10_000) // 100),
            "sell_after_tax_c": int(sell_price * TAX_RATE % 100),
        }
    return fetched_data


def get_unid_gear_data(gear_id: int) -> tuple[dict, ...] | None:
    try:
        fetched_data = fetch_tp_prices(
            [
                gear_id,
                ItemIDs.ECTOPLASM,
                ItemIDs.LUCENT_MOTE,
                ItemIDs.MIRTHIL,
                ItemIDs.ELDER_WOOD,
                ItemIDs.THICK_LEATHER,
                ItemIDs.GOSSAMER_SCRAP,
                ItemIDs.SILK_SCRAP,
                ItemIDs.HARDENED_LEATHER,
                ItemIDs.ANCIENT_WOOD,
                ItemIDs.SYMBOL_OF_ENH,
                ItemIDs.SYMBOL_OF_PAIN,
                ItemIDs.ORICHALCUM,
                ItemIDs.SYMBOL_OF_CONTROL,
                ItemIDs.CHARM_OF_BRILLIANCE,
                ItemIDs.CHARM_OF_POTENCE,
                ItemIDs.CHARM_OF_SKILL,
                ItemIDs.COMMON_GEAR,
            ],
        )
    except Exception:
        return None

    gear_data = fetched_data[gear_id]

    ecto_data = fetched_data[ItemIDs.ECTOPLASM]
    lucent_mote_data = fetched_data[ItemIDs.LUCENT_MOTE]
    mithril_data = fetched_data[ItemIDs.MIRTHIL]
    elder_wood_data = fetched_data[ItemIDs.ELDER_WOOD]
    thick_leather_ = fetched_data[ItemIDs.THICK_LEATHER]
    gossamer_scrap_data = fetched_data[ItemIDs.GOSSAMER_SCRAP]
    silk_scrap_data = fetched_data[ItemIDs.SILK_SCRAP]
    hardened_data = fetched_data[ItemIDs.HARDENED_LEATHER]
    ancient_wood_data = fetched_data[ItemIDs.ANCIENT_WOOD]
    symbol_of_enh_data = fetched_data[ItemIDs.SYMBOL_OF_ENH]
    symbol_of_pain_data = fetched_data[ItemIDs.SYMBOL_OF_PAIN]
    orichalcum_data = fetched_data[ItemIDs.ORICHALCUM]
    symbol_of_control_data = fetched_data[ItemIDs.SYMBOL_OF_CONTROL]
    charm_of_brilliance_data = fetched_data[ItemIDs.CHARM_OF_BRILLIANCE]
    charm_of_potence_data = fetched_data[ItemIDs.CHARM_OF_POTENCE]
    charm_of_skill_data = fetched_data[ItemIDs.CHARM_OF_SKILL]

    return (
        ecto_data,
        gear_data,
        lucent_mote_data,
        mithril_data,
        elder_wood_data,
        thick_leather_,
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
    data_tpl = get_unid_gear_data(gear_id=ItemIDs.RARE_UNID_GEAR)
    if data_tpl is None:
        return JSONResponse(content=jsonable_encoder({"error"}))

    (
        ecto_data,
        gear_data,
        lucent_mote_data,
        mithril_data,
        elder_wood_data,
        thick_leather_,
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

    stack_buy = gear_data["buy"] * 250.0

    lucent_mote_sell = lucent_mote_data["sell"]
    mithril_sell = mithril_data["sell"]
    elder_wood_sell = elder_wood_data["sell"]
    ecto_sell = ecto_data["sell"]
    thick_leather_sell = thick_leather_["sell"]
    gossamer_scrap_sell = gossamer_scrap_data["sell"]
    silk_scrap_sell = silk_scrap_data["sell"]
    hardened_sell = hardened_data["sell"]
    ancient_wood_sell = ancient_wood_data["sell"]
    symbol_of_enh_sell = symbol_of_enh_data["sell"]
    symbol_of_pain_sell = symbol_of_pain_data["sell"]
    orichalcum_sell = orichalcum_data["sell"]
    symbol_of_control_sell = symbol_of_control_data["sell"]
    charm_of_brilliance_sell = charm_of_brilliance_data["sell"]
    charm_of_potence_sell = charm_of_potence_data["sell"]
    charm_of_skilldata_sell = charm_of_skill_data["sell"]

    mats_value_after_tax = (
        mithril_sell * (250.0 * 0.4879) * TAX_RATE
        + elder_wood_sell * (250.0 * 0.3175) * TAX_RATE
        + silk_scrap_sell * (250.0 * 0.3367) * TAX_RATE
        + thick_leather_sell * (250.0 * 0.3457) * TAX_RATE
        + orichalcum_sell * (250.0 * 0.041) * TAX_RATE
        + ancient_wood_sell * (250.0 * 0.0249) * TAX_RATE
        + gossamer_scrap_sell * (250.0 * 0.018) * TAX_RATE
        + hardened_sell * (250.0 * 0.0162) * TAX_RATE
        + ecto_sell * (250.0 * 0.87) * TAX_RATE  # lowered
        + lucent_mote_sell * (250.0 * 0.2387) * TAX_RATE
        + symbol_of_control_sell * (250.0 * 0.001) * TAX_RATE
        + symbol_of_enh_sell * (250.0 * 0.0003) * TAX_RATE
        + symbol_of_pain_sell * (250.0 * 0.0004) * TAX_RATE
        + charm_of_brilliance_sell * (250.0 * 0.0006) * TAX_RATE
        + charm_of_potence_sell * (250.0 * 0.0009) * TAX_RATE
        + charm_of_skilldata_sell * (250.0 * 0.0009) * TAX_RATE
    )

    salvage_costs = 250 * 60  # Silver Fed

    profit_stack = mats_value_after_tax - stack_buy - salvage_costs

    data = {
        **get_sub_dct("stack_buy", stack_buy),
        **get_sub_dct("salvage_costs", salvage_costs),
        **get_sub_dct("mats_value_after_tax", mats_value_after_tax),
        **get_sub_dct("profit_stack", profit_stack),
    }
    return JSONResponse(content=jsonable_encoder(data))


@fastapi_app.get("/rare_weapon_craft")
def get_rare_weapon_craft() -> JSONResponse:
    try:
        fetched_data = fetch_tp_prices(
            [
                ItemIDs.ECTOPLASM,
                ItemIDs.MITHRIL_INGOT,
                ItemIDs.MITHRIL_ORE,
                ItemIDs.ELDER_WOOD_PLANK,
                ItemIDs.ELDER_WOOD_LOG,
                ItemIDs.LARGE_CLAW,
                ItemIDs.POTENT_BLOOD,
                ItemIDs.LARGE_BONE,
                ItemIDs.INTRICATE_TOTEM,
                ItemIDs.LARGE_FANG,
                ItemIDs.POTENT_VENOM_SAC,
            ],
        )
    except Exception as e:
        return JSONResponse(content=jsonable_encoder({"error": str(e)}))

    ecto_sell_after_tax = fetched_data[ItemIDs.ECTOPLASM]["sell"] * TAX_RATE
    mithril_ore_buy = fetched_data[ItemIDs.MITHRIL_ORE]["buy"]
    mithril_ingot_buy = fetched_data[ItemIDs.MITHRIL_INGOT]["buy"]
    elder_wood_log_buy = fetched_data[ItemIDs.ELDER_WOOD_LOG]["buy"]
    elder_wood_plank_buy = fetched_data[ItemIDs.ELDER_WOOD_PLANK]["buy"]
    large_claw_buy = fetched_data[ItemIDs.LARGE_CLAW]["buy"]
    potent_blood_buy = fetched_data[ItemIDs.POTENT_BLOOD]["buy"]
    large_bone_buy = fetched_data[ItemIDs.LARGE_BONE]["buy"]
    intricate_totem_buy = fetched_data[ItemIDs.INTRICATE_TOTEM]["buy"]
    large_fang_buy = fetched_data[ItemIDs.LARGE_FANG]["buy"]
    potent_sac_buy = fetched_data[ItemIDs.POTENT_VENOM_SAC]["buy"]

    lowest_t5_mat = min(
        large_claw_buy,
        potent_blood_buy,
        large_bone_buy,
        intricate_totem_buy,
        large_fang_buy,
        potent_sac_buy,
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
    rare_gear_craft_profit = (
        ecto_sell_after_tax * 0.9 - crafting_cost_with_cheap_materials
    )

    data = {
        **get_sub_dct("crafting_cost", crafting_cost_with_cheap_materials),
        **get_sub_dct("ecto_sell_after_tax", ecto_sell_after_tax),
        **get_sub_dct("profit", rare_gear_craft_profit),
    }

    return JSONResponse(content=jsonable_encoder(data))


@fastapi_app.get("/t5_mats_buy")
def get_t5_mats_buy() -> JSONResponse:
    try:
        fetched_data = fetch_tp_prices(
            [
                ItemIDs.LARGE_CLAW,
                ItemIDs.POTENT_BLOOD,
                ItemIDs.LARGE_BONE,
                ItemIDs.INTRICATE_TOTEM,
                ItemIDs.LARGE_FANG,
                ItemIDs.POTENT_VENOM_SAC,
            ],
        )
    except Exception as e:
        return JSONResponse(content=jsonable_encoder({"error": str(e)}))

    large_claw_buy = fetched_data[ItemIDs.LARGE_CLAW]["buy"]
    potent_blood_buy = fetched_data[ItemIDs.POTENT_BLOOD]["buy"]
    large_bone_buy = fetched_data[ItemIDs.LARGE_BONE]["buy"]
    intricate_totem_buy = fetched_data[ItemIDs.INTRICATE_TOTEM]["buy"]
    large_fang_buy = fetched_data[ItemIDs.LARGE_FANG]["buy"]
    venom_sac_buy = fetched_data[ItemIDs.POTENT_VENOM_SAC]["buy"]

    data = {
        **get_sub_dct("large_claw", large_claw_buy),
        **get_sub_dct("potent_blood", potent_blood_buy),
        **get_sub_dct("large_bone", large_bone_buy),
        **get_sub_dct("intricate_totem", intricate_totem_buy),
        **get_sub_dct("large_fang", large_fang_buy),
        **get_sub_dct("potent_venom", venom_sac_buy),
    }

    return JSONResponse(content=jsonable_encoder(data))


@fastapi_app.get("/mats_crafting_compare")
def get_mats_crafting_compare() -> JSONResponse:
    try:
        fetched_data = fetch_tp_prices(
            [
                ItemIDs.MITHRIL_INGOT,
                ItemIDs.MITHRIL_ORE,
                ItemIDs.ELDER_WOOD_PLANK,
                ItemIDs.ELDER_WOOD_LOG,
                ItemIDs.LUCENT_MOTE,
                ItemIDs.PILE_OF_LUCENT_CRYSTAL,
            ],
        )
    except Exception as e:
        return JSONResponse(content=jsonable_encoder({"error": str(e)}))

    mithril_ore_buy = fetched_data[ItemIDs.MITHRIL_ORE]["buy"]
    mithril_ingot_buy = fetched_data[ItemIDs.MITHRIL_INGOT]["buy"]
    elder_wood_log_buy = fetched_data[ItemIDs.ELDER_WOOD_LOG]["buy"]
    elder_wood_plank_buy = fetched_data[ItemIDs.ELDER_WOOD_PLANK]["buy"]
    lucent_mote_buy = fetched_data[ItemIDs.LUCENT_MOTE]["buy"]
    lucent_crystal_buy = fetched_data[ItemIDs.PILE_OF_LUCENT_CRYSTAL]["buy"]

    lucent_mote_to_crystal = lucent_mote_buy * 10.0

    data = {
        **get_sub_dct("mithril_ore_to_ingot", mithril_ore_buy * 2.0),
        **get_sub_dct("mithril_ingot_buy", mithril_ingot_buy),
        **get_sub_dct("elder_wood_log_to_plank", elder_wood_log_buy * 3.0),
        **get_sub_dct("elder_wood_plank_buy", elder_wood_plank_buy),
        **get_sub_dct("lucent_mote_to_crystal", lucent_mote_to_crystal),
        **get_sub_dct("lucent_crystal_buy", lucent_crystal_buy),
    }

    return JSONResponse(content=jsonable_encoder(data))


@fastapi_app.get("/scholar_rune")
def get_scholar_rune() -> JSONResponse:
    try:
        fetched_data = fetch_tp_prices(
            [
                ItemIDs.ECTOPLASM,
                ItemIDs.ELABORATE_TOTEM,
                ItemIDs.PILE_OF_LUCENT_CRYSTAL,
                ItemIDs.CHARM_OF_BRILLIANCE,
                ItemIDs.LUCENT_MOTE,
                ItemIDs.SCHOLAR_RUNE,
            ],
        )
    except Exception as e:
        return JSONResponse(content=jsonable_encoder({"error": str(e)}))

    ecto_buy = fetched_data[ItemIDs.ECTOPLASM]["buy"]
    totem_buy = fetched_data[ItemIDs.ELABORATE_TOTEM]["buy"]
    lucent_crystal_buy = fetched_data[ItemIDs.PILE_OF_LUCENT_CRYSTAL]["buy"]
    charm_buy = fetched_data[ItemIDs.CHARM_OF_BRILLIANCE]["buy"]
    lucent_mote_buy = fetched_data[ItemIDs.LUCENT_MOTE]["buy"]

    scholar_rune_sell = fetched_data[ItemIDs.SCHOLAR_RUNE]["sell"]

    crafting_cost = (
        ecto_buy * 5.0
        + totem_buy * 5.0
        + lucent_crystal_buy * 8.0
        + charm_buy * 2.0
    )
    crafting_cost2 = (
        ecto_buy * 5.0
        + totem_buy * 5.0
        + lucent_mote_buy * 80.0
        + charm_buy * 2.0
    )

    profit = scholar_rune_sell * TAX_RATE - crafting_cost
    profit2 = scholar_rune_sell * TAX_RATE - crafting_cost2

    cheap_crafting_cost = min(crafting_cost, crafting_cost2)
    highest_profit = max(profit, profit2)

    data = {
        **get_sub_dct("crafting_cost", cheap_crafting_cost),
        **get_sub_dct("sell", scholar_rune_sell),
        **get_sub_dct("profit", highest_profit),
    }

    return JSONResponse(content=jsonable_encoder(data))


@fastapi_app.get("/guardian_rune")
def get_guardian_rune() -> JSONResponse:
    try:
        fetched_data = fetch_tp_prices(
            [
                ItemIDs.GUARD_RUNE,
                ItemIDs.PILE_OF_LUCENT_CRYSTAL,
                ItemIDs.CHARGED_LOADSTONE,
                ItemIDs.CHARM_OF_POTENCE,
                ItemIDs.ECTOPLASM,
            ],
        )
    except Exception as e:
        return JSONResponse(content=jsonable_encoder({"error": str(e)}))

    rune_sell = fetched_data[ItemIDs.GUARD_RUNE]["sell"]
    charged_loadstone_sell = fetched_data[ItemIDs.CHARGED_LOADSTONE]["sell"]

    charm_buy = fetched_data[ItemIDs.CHARM_OF_POTENCE]["buy"]
    ecto_buy = fetched_data[ItemIDs.ECTOPLASM]["buy"]
    lucent_crystal_buy = fetched_data[ItemIDs.PILE_OF_LUCENT_CRYSTAL]["buy"]

    crafting_cost = (
        charged_loadstone_sell
        + charm_buy
        + ecto_buy * 5.0
        + lucent_crystal_buy * 12.0
    )

    profit = rune_sell * TAX_RATE - crafting_cost

    data = {
        **get_sub_dct("crafting_cost", crafting_cost),
        **get_sub_dct("sell", rune_sell),
        **get_sub_dct("profit", profit),
    }

    return JSONResponse(content=jsonable_encoder(data))


@fastapi_app.get("/dragonhunter_rune")
def get_dragonhunter_rune() -> JSONResponse:
    try:
        fetched_data = fetch_tp_prices(
            [
                ItemIDs.GUARD_RUNE,
                ItemIDs.DRAGONHUNTER_RUNE,
                ItemIDs.EVERGREEN_LOADSTONE,
                ItemIDs.BARBED_THORN,
                ItemIDs.PILE_OF_LUCENT_CRYSTAL,
                ItemIDs.CHARGED_LOADSTONE,
                ItemIDs.CHARM_OF_POTENCE,
                ItemIDs.ECTOPLASM,
            ],
        )
    except Exception as e:
        return JSONResponse(content=jsonable_encoder({"error": str(e)}))

    rune_sell = fetched_data[ItemIDs.DRAGONHUNTER_RUNE]["sell"]
    charged_loadstone_sell = fetched_data[ItemIDs.CHARGED_LOADSTONE]["sell"]

    evergreen_loadstone_buy = fetched_data[ItemIDs.EVERGREEN_LOADSTONE]["buy"]
    thorns_buy = fetched_data[ItemIDs.BARBED_THORN]["buy"]
    charm_buy = fetched_data[ItemIDs.CHARM_OF_POTENCE]["buy"]
    ecto_buy = fetched_data[ItemIDs.ECTOPLASM]["buy"]
    lucent_crystal_buy = fetched_data[ItemIDs.PILE_OF_LUCENT_CRYSTAL]["buy"]

    guardian_rune_cost = (
        charged_loadstone_sell
        + charm_buy
        + ecto_buy * 5.0
        + lucent_crystal_buy * 12.0
    )

    crafting_cost = (
        guardian_rune_cost * 1.0
        + evergreen_loadstone_buy * 1.0
        + thorns_buy * 10.0
    )

    profit = rune_sell * TAX_RATE - crafting_cost

    data = {
        **get_sub_dct("crafting_cost", crafting_cost),
        **get_sub_dct("sell", rune_sell),
        **get_sub_dct("profit", profit),
    }

    return JSONResponse(content=jsonable_encoder(data))


@fastapi_app.get("/relic_of_fireworks")
def get_relic_of_fireworks() -> JSONResponse:
    try:
        fetched_data = fetch_tp_prices(
            [
                ItemIDs.ECTOPLASM,
                ItemIDs.PILE_OF_LUCENT_CRYSTAL,
                ItemIDs.CHARM_OF_SKILL,
                ItemIDs.LUCENT_MOTE,
                ItemIDs.RELIC_OF_FIREWORKS,
            ],
        )
    except Exception as e:
        return JSONResponse(content=jsonable_encoder({"error": str(e)}))

    ecto_buy = fetched_data[ItemIDs.ECTOPLASM]["buy"]
    lucent_crystal_buy = fetched_data[ItemIDs.PILE_OF_LUCENT_CRYSTAL]["buy"]
    charm_buy = fetched_data[ItemIDs.CHARM_OF_SKILL]["buy"]
    lucent_mote_buy = fetched_data[ItemIDs.LUCENT_MOTE]["buy"]
    relic_of_fireworks_sell = fetched_data[ItemIDs.RELIC_OF_FIREWORKS]["sell"]
    relic_of_fireworks_buy = fetched_data[ItemIDs.RELIC_OF_FIREWORKS]["buy"]

    crafting_cost = (
        ecto_buy * 15.0 + lucent_crystal_buy * 48.0 + charm_buy * 3.0
    )
    crafting_cost2 = ecto_buy * 15.0 + lucent_mote_buy * 480.0 + charm_buy * 3.0

    profit = relic_of_fireworks_sell * TAX_RATE - crafting_cost
    profit2 = relic_of_fireworks_sell * TAX_RATE - crafting_cost2

    cheap_crafting_cost = min(
        crafting_cost,
        crafting_cost2,
    )
    highest_profit = max(profit, profit2)
    relic_of_fireworks_flip = (
        relic_of_fireworks_sell * TAX_RATE
    ) - relic_of_fireworks_buy

    data = {
        **get_sub_dct("crafting_cost", cheap_crafting_cost),
        **get_sub_dct("sell", relic_of_fireworks_sell),
        **get_sub_dct("flip", relic_of_fireworks_flip),
        **get_sub_dct("profit", highest_profit),
    }

    return JSONResponse(content=jsonable_encoder(data))


@fastapi_app.get("/common_gear_salvage")
def get_common_gear_salvage() -> JSONResponse:
    data_tpl = get_unid_gear_data(gear_id=ItemIDs.COMMON_GEAR)
    if data_tpl is None:
        return JSONResponse(content=jsonable_encoder({"error"}))

    (
        ecto_data,
        gear_data,
        lucent_mote_data,
        mithril_data,
        elder_wood_data,
        thick_leather_,
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

    stack_buy = gear_data["buy"] * 250.0
    lucent_mote_sell = lucent_mote_data["sell"]
    mithril_sell = mithril_data["sell"]
    elder_wood_sell = elder_wood_data["sell"]
    ecto_sell = ecto_data["sell"]
    thick_leather_sell = thick_leather_["sell"]

    gossamer_scrap_sell = gossamer_scrap_data["sell"]
    silk_scrap_sell = silk_scrap_data["sell"]
    hardened_sell = hardened_data["sell"]
    ancient_wood_sell = ancient_wood_data["sell"]
    symbol_of_enh_sell = symbol_of_enh_data["sell"]
    symbol_of_pain_sell = symbol_of_pain_data["sell"]
    orichalcum_sell = orichalcum_data["sell"]
    symbol_of_control_sell = symbol_of_control_data["sell"]
    charm_of_brilliance_sell = charm_of_brilliance_data["sell"]
    charm_of_potence_sell = charm_of_potence_data["sell"]
    charm_of_skill_sell = charm_of_skill_data["sell"]

    mats_value_after_tax = (
        mithril_sell * (250.0 * 0.4291) * TAX_RATE
        + elder_wood_sell * (250.0 * 0.3884) * TAX_RATE
        + silk_scrap_sell * (250.0 * 0.3059) * TAX_RATE
        + thick_leather_sell * (250.0 * 0.25) * TAX_RATE  # lowered
        + orichalcum_sell * (250.0 * 0.0394) * TAX_RATE
        + ancient_wood_sell * (250.0 * 0.0305) * TAX_RATE
        + gossamer_scrap_sell * (250.0 * 0.0153) * TAX_RATE
        + hardened_sell * (250.0 * 0.0143) * TAX_RATE
        + ecto_sell * (250.0 * 0.007) * TAX_RATE  # lowered
        + lucent_mote_sell * (250.0 * 0.1075) * TAX_RATE  # lowered
        + symbol_of_control_sell * (250.0 * 0.0002) * TAX_RATE
        + symbol_of_enh_sell * (250.0 * 0.0006) * TAX_RATE
        + symbol_of_pain_sell * (250.0 * 0.0005) * TAX_RATE
        + charm_of_brilliance_sell * (250.0 * 0.0004) * TAX_RATE
        + charm_of_potence_sell * (250.0 * 0.0003) * TAX_RATE
        + charm_of_skill_sell * (250.0 * 0.0003) * TAX_RATE
    )

    salvage_costs = (
        3.0 * 223  # Copper Fed
        + 30.0 * 25  # Runecrafter
        + 60 * 2  # Silver Fed
    )

    profit_stack = mats_value_after_tax - stack_buy - salvage_costs

    data = {
        **get_sub_dct("stack_buy", stack_buy),
        **get_sub_dct("salvage_costs", salvage_costs),
        **get_sub_dct("mats_value_after_tax", mats_value_after_tax),
        **get_sub_dct("profit_stack", profit_stack),
    }
    return JSONResponse(content=jsonable_encoder(data))


@fastapi_app.get("/gear_salvage")
def get_gear_salvage() -> JSONResponse:
    data_tpl = get_unid_gear_data(gear_id=ItemIDs.UNID_GEAR)
    if data_tpl is None:
        return JSONResponse(content=jsonable_encoder({"error"}))

    (
        ecto_data,
        gear_data,
        lucent_mote_data,
        mithril_data,
        elder_wood_data,
        thick_leather_,
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

    stack_buy = gear_data["buy"] * 250.0
    lucent_mote_sell = lucent_mote_data["sell"]
    mithril_sell = mithril_data["sell"]
    elder_wood_sell = elder_wood_data["sell"]
    ecto_sell = ecto_data["sell"]
    thick_leather_sell = thick_leather_["sell"]

    gossamer_scrap_sell = gossamer_scrap_data["sell"]
    silk_scrap_sell = silk_scrap_data["sell"]
    hardened_sell = hardened_data["sell"]
    ancient_wood_sell = ancient_wood_data["sell"]
    symbol_of_enh_sell = symbol_of_enh_data["sell"]
    symbol_of_pain_sell = symbol_of_pain_data["sell"]
    orichalcum_sell = orichalcum_data["sell"]
    symbol_of_control_sell = symbol_of_control_data["sell"]
    charm_of_brilliance_sell = charm_of_brilliance_data["sell"]
    charm_of_potence_sell = charm_of_potence_data["sell"]
    charm_of_skilldata_sell = charm_of_skill_data["sell"]

    mats_value_after_tax = (
        mithril_sell * (250.0 * 0.4299) * TAX_RATE
        + elder_wood_sell * (250.0 * 0.3564) * TAX_RATE
        + silk_scrap_sell * (250.0 * 0.3521) * TAX_RATE
        + thick_leather_sell * (250.0 * 0.2673) * TAX_RATE
        + orichalcum_sell * (250.0 * 0.0387) * TAX_RATE
        + ancient_wood_sell * (250.0 * 0.0287) * TAX_RATE
        + gossamer_scrap_sell * (250.0 * 0.018) * TAX_RATE
        + hardened_sell * (250.0 * 0.0169) * TAX_RATE
        + ecto_sell * (250.0 * 0.0291) * TAX_RATE  # lowered
        + lucent_mote_sell * (250.0 * 0.98) * TAX_RATE
        + symbol_of_control_sell * (250.0 * 0.0018) * TAX_RATE
        + symbol_of_enh_sell * (250.0 * 0.001) * TAX_RATE
        + symbol_of_pain_sell * (250.0 * 0.0006) * TAX_RATE
        + charm_of_brilliance_sell * (250.0 * 0.0042) * TAX_RATE
        + charm_of_potence_sell * (250.0 * 0.0029) * TAX_RATE
        + charm_of_skilldata_sell * (250.0 * 0.0028) * TAX_RATE
    )

    salvage_costs = 30.0 * 245 + 60 * 5

    profit_stack = mats_value_after_tax - stack_buy - salvage_costs

    data = {
        **get_sub_dct("stack_buy", stack_buy),
        **get_sub_dct("salvage_costs", salvage_costs),
        **get_sub_dct("mats_value_after_tax", mats_value_after_tax),
        **get_sub_dct("profit_stack", profit_stack),
    }
    return JSONResponse(content=jsonable_encoder(data))


@fastapi_app.get("/profits")
def get_profits() -> JSONResponse:
    try:
        guardian_response = httpx.Client().get(
            f"{api_base}dragonhunter_rune",
        )
        guardian_data = guardian_response.json()
        dragonhunter_response = httpx.Client().get(
            f"{api_base}guardian_rune",
        )
        dragonhunter_data = dragonhunter_response.json()
        scholar_response = httpx.Client().get(
            f"{api_base}scholar_rune",
        )
        scholar_data = scholar_response.json()
        fireworks_response = httpx.Client().get(
            f"{api_base}relic_of_fireworks",
        )
        fireworks_data = fireworks_response.json()
        rare_weapon_response = httpx.Client().get(
            f"{api_base}rare_weapon_craft",
        )
        rare_weapon_data = rare_weapon_response.json()
    except Exception as e:
        return JSONResponse(content=jsonable_encoder({"error": str(e)}))

    guardian_rune_profit = gsc_dict_to_copper(guardian_data)
    dragonhunter_rune_profit = gsc_dict_to_copper(dragonhunter_data)
    scholar_rune_profit = gsc_dict_to_copper(scholar_data)
    fireworks_relic_profit = gsc_dict_to_copper(fireworks_data)
    rare_weapon_craft_profit = gsc_dict_to_copper(rare_weapon_data)

    data = {
        **get_sub_dct("guardian_rune_profit", guardian_rune_profit),
        **get_sub_dct("dragonhunter_rune", dragonhunter_rune_profit),
        **get_sub_dct("scholar_rune", scholar_rune_profit),
        **get_sub_dct("fireworks_relic", fireworks_relic_profit),
        **get_sub_dct("rare_weapon_craft", rare_weapon_craft_profit),
    }
    return JSONResponse(content=jsonable_encoder(data))


@fastapi_app.get("/t5_mats_sell")
def get_t5_mats_sell() -> JSONResponse:
    try:
        fetched_data = fetch_tp_prices(
            [
                ItemIDs.LUCENT_MOTE,
                ItemIDs.MIRTHIL,
                ItemIDs.ELDER_WOOD,
                ItemIDs.THICK_LEATHER,
            ],
        )
    except Exception as e:
        return JSONResponse(content=jsonable_encoder({"error": str(e)}))

    lucent_mote_data = fetched_data[ItemIDs.LUCENT_MOTE]
    mithril_data = fetched_data[ItemIDs.MIRTHIL]
    elder_wood_data = fetched_data[ItemIDs.ELDER_WOOD]
    thick_leather_ = fetched_data[ItemIDs.THICK_LEATHER]

    lucent_mote_sell = lucent_mote_data["sell"]
    mithril_sell = mithril_data["sell"]
    elder_wood_sell = elder_wood_data["sell"]
    thick_leather_sell = thick_leather_["sell"]

    data = {
        **get_sub_dct("lucent_mote", lucent_mote_sell * 250.0),
        **get_sub_dct("mithril_ore", mithril_sell * 250.0),
        **get_sub_dct("elder_wood_log", elder_wood_sell * 250.0),
        **get_sub_dct("thick_leather", thick_leather_sell * 250.0),
    }
    return JSONResponse(content=jsonable_encoder(data))


@fastapi_app.get("/smybol_enh_forge")
def get_smybol_enh_forge() -> JSONResponse:
    try:
        fetched_data = fetch_tp_prices(
            [
                ItemIDs.SYMBOL_OF_ENH,
                ItemIDs.SYMBOL_OF_PAIN,
                ItemIDs.SYMBOL_OF_CONTROL,
            ],
        )
    except Exception as e:
        return JSONResponse(content=jsonable_encoder({"error": str(e)}))

    enh_buy = fetched_data[ItemIDs.SYMBOL_OF_ENH]["buy"]
    enh_sell = fetched_data[ItemIDs.SYMBOL_OF_ENH]["sell"]
    pain_sell = fetched_data[ItemIDs.SYMBOL_OF_PAIN]["sell"]
    control_sell = fetched_data[ItemIDs.SYMBOL_OF_CONTROL]["sell"]

    cost = enh_buy * 3.0
    reward = enh_sell * 0.2 + pain_sell * 0.4 + control_sell * 0.4
    profit = (reward * TAX_RATE) - cost

    data = {
        **get_sub_dct("cost", cost),
        **get_sub_dct("profit_per_try", profit),
        **get_sub_dct("profit_per_shard", profit * 10.0),
    }
    return JSONResponse(content=jsonable_encoder(data))


@fastapi_app.get("/loadstone_forge")
def get_loadstone_forge() -> JSONResponse:
    try:
        fetched_data = fetch_tp_prices(
            [
                ItemIDs.ONYX_LOADSTONE,
                ItemIDs.CHARGED_LOADSTONE,
                ItemIDs.CORRUPTED_LOADSTONE,
                ItemIDs.DESTROYER_LOADSTONE,
                ItemIDs.CRYSTALINE_DUST,
            ],
        )
    except Exception as e:
        return JSONResponse(content=jsonable_encoder({"error": str(e)}))

    onyx_sell = fetched_data[ItemIDs.ONYX_LOADSTONE]["buy"]
    charged_sell = fetched_data[ItemIDs.CHARGED_LOADSTONE]["sell"]
    corrupted_sell = fetched_data[ItemIDs.CORRUPTED_LOADSTONE]["sell"]
    destroyer_sell = fetched_data[ItemIDs.DESTROYER_LOADSTONE]["sell"]
    dust_buy = fetched_data[ItemIDs.CRYSTALINE_DUST]["buy"]
    elonian_cost = 2_500

    onyx_core_cost = 100
    onyx_cost = onyx_core_cost * 2 + dust_buy + elonian_cost
    onyx_profit = (onyx_sell * 0.85) - onyx_cost

    charged_core_cost = 100
    charged_cost = charged_core_cost * 2 + dust_buy + elonian_cost
    charged_profit = (charged_sell * 0.85) - charged_cost

    corrupted_core_cost = 100
    corrupted_cost = corrupted_core_cost * 2 + dust_buy + elonian_cost
    corrupted_profit = (corrupted_sell * 0.85) - corrupted_cost

    destroyer_core_cost = 100
    destroyer_cost = destroyer_core_cost * 2 + dust_buy + elonian_cost
    destroyer_profit = (destroyer_sell * 0.85) - destroyer_cost

    data = {
        **get_sub_dct("onyx", onyx_profit),
        **get_sub_dct("charged", charged_profit),
        **get_sub_dct("corrupted", corrupted_profit),
        **get_sub_dct("destroyer", destroyer_profit),
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
