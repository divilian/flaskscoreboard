import sqlite3

import click
from flask import current_app, g
from flask.cli import with_appcontext
import os

def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect(
            os.path.join(current_app.instance_path,
                current_app.config['DATABASE']),
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        # Not strictly necessary since we're converting to DataFrame anyway.
        g.db.row_factory = sqlite3.Row
    return g.db

def close_db(exception):
    db = g.pop('db',None)
    if db is not None:
        db.close()

def init_db():
    db = get_db()

    with current_app.open_resource("create_schema.sql") as f:
        db.executescript(f.read().decode('utf-8'))

@click.command('init-db')
@with_appcontext
def init_db_command():
    init_db()
    click.echo("Initialized the database.")

def init_app(app):
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)
