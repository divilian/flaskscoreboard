import pandas as pd
import os
import click
from flask import current_app, g
from flask.cli import with_appcontext


# For a given number of XP, return a tuple with the name, image URL, and grade
# corresponding to the highest level it achieves.
def get_level(xps):
    if 'levels' not in g:
        levels_filename = os.path.join(current_app.instance_path,
            current_app.config['LEVELS_CSV'])
        if os.path.isfile(levels_filename):
            g.levels = pd.read_csv(levels_filename,
                encoding="utf-8").sort_values('minxp', ascending=False)
        else:
            print("No levels file!")
            g.levels = pd.DataFrame({"level":["Novice"], "minxp":[0],
                "image":[""], "grade":["F"]}).sort_values('minxp',
                ascending=False)

    the_row = g.levels[xps >= g.levels.minxp].iloc[0]
    return (the_row['level'], the_row['image'], the_row['grade'])
