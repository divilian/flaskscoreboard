
from flask import current_app, g, render_template
from scoreboard.db import get_db
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
    import ipdb; ipdb.set_trace()
    students = pd.DataFrame(db_results)
    students.columns = ['username','total','latest_time']
    return render_template("student_scoreboard.html",students=students,
        title="Student view")
