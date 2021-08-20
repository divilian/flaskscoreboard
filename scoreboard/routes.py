
from flask import current_app, g, render_template
from scoreboard.db import get_db
from scoreboard.levels import get_level
import numpy as np
import pandas as pd

@current_app.route('/sup')
def sup():
    return "Sup dude!"

@current_app.route('/')
def student_scoreboard():
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
    
    return render_template("student_scoreboard.html",students=students,
        title="Student view")
