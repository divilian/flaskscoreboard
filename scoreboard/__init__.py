
import os

from flask import Flask

xpapp = Flask(__name__, instance_relative_config=True)
xpapp.config.from_envvar("SCOREBOARD_SETTINGS_FILE")

try:
    os.makedirs(xpapp.instance_path, exist_ok=True)
except OSError as e:
    print(f"Can't create inst path! {xpapp.instance_path}")

from . import db
db.init_app(xpapp)

with xpapp.app_context():
    from . import routes
    from . import controllers

