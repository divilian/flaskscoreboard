
import os

from flask import Flask

def create_app():
    xpapp = Flask(__name__, instance_relative_config=True)
    xpapp.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(xpapp.instance_path,"xp.sqlite")
    )

    try:
        os.makedirs(xpapp.instance_path, exist_ok=True)
    except OSError as e:
        print(f"Can't create inst path! {xpapp.instance_path}")

    from . import db
    db.init_app(xpapp)
    
    with xpapp.app_context():
        from . import routes

    return xpapp
