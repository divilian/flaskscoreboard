import pandas as pd
import os
import click
from flask import current_app, g
from flask.cli import with_appcontext

# levels.csv should be in the instance directory, and should look like this:
#
#level,image,grade,minxp
#Bottom Feeder,novice.html,F,0
#Dork,dork.html,F,3
#Stud,stud.html,C,6
#Dragon,dragon.html,B,9
#Destroyer,destroyer.html,A,29


# For a given number of XP, return a tuple with the name, image URL, and grade
# corresponding to the highest level it achieves.
def get_level(xps):
    if 'levels' not in g:
        if os.path.isfile(current_app.config['LEVELS_CSV']):
            g.levels = pd.read_csv(current_app.config['LEVELS_CSV'],
                encoding="utf-8").sort_values('minxp', ascending=False)
        else:
            print("No levels file!")
            g.levels = pd.DataFrame({"level":["Novice"], "minxp":[0],
                "image":[""], "grade":["F"]}).sort_values('minxp',
                ascending=False)

    the_row = g.levels[xps >= g.levels.minxp].iloc[0]
    return (the_row['level'], the_row['image'], the_row['grade'])
