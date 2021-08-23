
from flask import current_app, g, render_template, request
from scoreboard.db import get_db
from scoreboard.levels import get_level
import numpy as np
import pandas as pd

@current_app.route('/create')
def create():
    return render_template("create_account.html")

@current_app.route('/')
@current_app.route('/student')
def student_main():
    db = get_db()

    db_results = db.execute(
        """
        select username, sum(xps) as total,
            max(thetime) as latest_time from xp
        group by username
        order by total desc
        """).fetchall()
    students = pd.DataFrame(db_results)
    students.columns = ['username','total','latest_time']

    levels = np.array([], dtype='object')
    images = np.array([], dtype='object')
    grades = np.array([], dtype='object')
    most_recents = np.array([], dtype='object')

    for row in students.itertuples():

        level, image, grade = get_level(row.total)
        levels = np.append(levels, level)
        images = np.append(images, image)
        grades = np.append(grades, grade)

        most_recent_tag = db.execute(
            """
            select tag from xp where username=?
            order by thetime desc
            limit 1
            """, (row.username,)).fetchone()
        most_recents = np.append(most_recents, most_recent_tag['tag'])

    students['level'] = levels
    students['image'] = images
    students['grade'] = grades
    students['most_recent'] = most_recents
    
    return render_template("student_main.html",students=students,
        title=current_app.config['TITLE'])

# URL is .../fac?hash=ajwerjaklerjkaejlrkj
@current_app.route('/fac')
def faculty_scoreboard():

    db = get_db()

    db_secret = db.execute("select secret from secret").fetchone()
    if ('hash' in request.args and request.args['hash'] and
        request.args['hash'] == db_secret['secret']):

        db_results = db.execute(
            """
            select realname, username, sum(xps) as total,
                    max(thetime) as latest_time from
                xp join chars on username=charname
            group by username
            order by total desc
            """).fetchall()
        students = pd.DataFrame(db_results)
        students.columns = ['realname','username','total','latest_time']

        levels = np.array([], dtype='object')
        images = np.array([], dtype='object')
        grades = np.array([], dtype='object')
        most_recents = np.array([], dtype='object')

        for row in students.itertuples():

            level, image, grade = get_level(row.total)
            levels = np.append(levels, level)
            images = np.append(images, image)
            grades = np.append(grades, grade)

            most_recent_tag = db.execute(
                """
                select tag from xp where username=?
                order by thetime desc
                limit 1
                """, (row.username,)).fetchone()
            most_recents = np.append(most_recents, most_recent_tag['tag'])

        students['level'] = levels
        students['image'] = images
        students['grade'] = grades
        students['most_recent'] = most_recents
        
        return render_template("faculty_scoreboard.html",students=students,
            title="Faculty view")
    else:
        return "Nope."
