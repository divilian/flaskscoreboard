
from flask import current_app, g, render_template, request
from scoreboard.db import get_db
from scoreboard.levels import get_level
import numpy as np
import pandas as pd

@current_app.route('/')
def main():

    db = get_db()

    # If the URL had a "hash" URL parameter on it that matched the database,
    # show the faculty (full names) version of the scoreboard.
    db_secret = db.execute("select secret from secret").fetchone()
    if ('hash' in request.args and request.args['hash'] and
        request.args['hash'] == db_secret['secret']):
        role = "faculty"
    else:
        role = "student"

    return render_template("main.html",students=getStudentList(),
        title=current_app.config['TITLE'],
        stylefilename=current_app.config['STYLE_FILENAME'],
        url_base=current_app.config['URL_BASE'],
        role=role)


def getStudentList():
    db = get_db()
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
    return students


@current_app.route('/myxp', methods=['GET','POST'])
def myxp():

    print(f"it's {request.method}")
    if request.method == 'GET':
        return render_template("my_xp_challenge.html")
    else:
        db = get_db()
        db_results = db.execute(
            """
            select realname, charname from chars
            where realname=? and charname=?
            """,
            (request.form['username'], request.form['charname'])).fetchone()
        if db_results:
            return render_template("my_xp.html")
        else:
            return render_template("main.html",students=getStudentList(),
                opentab='myxp',
                error=f"No such student {request.form['username']} with " +
                    f"screen name {request.form['charname']}",
                title=current_app.config['TITLE'],
                stylefilename=current_app.config['STYLE_FILENAME'],
                url_base=current_app.config['URL_BASE'],
                role="student")
