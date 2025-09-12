from __future__ import annotations

import datetime
from pathlib import Path

from flask import Flask
from flask import render_template_string
from starlette.applications import Starlette
from starlette.middleware.wsgi import WSGIMiddleware
from starlette.routing import Mount

from backend.db import SessionLocal
from frontend.html_template import HTML_PAGE
from frontend.plotting import get_date_plot
from gw2tp.db_schema import get_db_data
from gw2tp.helper import host_url


api_base = host_url()
flask_app = Flask(__name__)


@flask_app.route("/")
def index() -> str:
    return render_template_string(HTML_PAGE)


def history_base(
    key_name: str,
    full_name: str,
) -> str:
    db = SessionLocal()
    end_datetime = datetime.datetime.now(
        tz=datetime.timezone(datetime.timedelta(hours=2), "UTC")
    )
    start_datetime = end_datetime - datetime.timedelta(hours=24)
    data = get_db_data(
        db,
        key_name,
        start_datetime=start_datetime,
        end_datetime=end_datetime,
    )
    plot = get_date_plot(data=data)
    content = Path("./templates/plot.html").read_text(encoding="utf-8")
    style = Path("./static/style.css").read_text(encoding="utf-8")
    return render_template_string(
        content,
        item_name=full_name,
        history=data,
        plot=plot,
        style=style,
    )


@flask_app.route("/scholar_rune_history")
def history_scholar() -> str:
    return history_base("scholar_rune", "Scholar Rune")


@flask_app.route("/guardian_rune_history")
def history_guardian() -> str:
    return history_base("guardian_rune", "Guardian Rune")


@flask_app.route("/dragonhunter_rune_history")
def history_dragonhunter() -> str:
    return history_base("dragonhunter_rune", "Dragonhunter Rune")


@flask_app.route("/relic_of_fireworks_history")
def history_fireworks() -> str:
    return history_base("relic_of_fireworks", "Relic of Fireworks")


@flask_app.route("/relic_of_thief_history")
def history_thief() -> str:
    return history_base("relic_of_thief", "Relic of Thief")


@flask_app.route("/relic_of_aristocracy_history")
def history_aristocracy() -> str:
    return history_base("relic_of_aristocracy", "Relic of Aristocracy")


app = Starlette(
    routes=[
        Mount("/", app=WSGIMiddleware(flask_app)),
    ],
)
