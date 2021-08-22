
from flask import current_app, g, render_template, request, redirect, url_for
from scoreboard.db import get_db
from scoreboard.levels import get_level
import numpy as np
import pandas as pd

@current_app.route('/createAcctController', methods=['GET','POST'])
def createAcctController():
    db = get_db()
    username = request.form['username']
    charname = request.form['charname']
    existing = db.execute("select * from chars").fetchall()
    existing_usernames = [ u for u,_ in existing ]
    existing_charnames = [ c for _,c in existing ]
    if username in existing_usernames:
        return f"Sorry! {username} already has a scoreboard account."
    if charname in existing_charnames:
        return f"Sorry! {charname} is already taken."
    db.execute("insert into chars (realname, charname) values (?, ?)",
        (username,charname))
    db.execute("insert into xp (username, xps, tag) values (?, ?, ?)",
        (charname,1,"Scoreboard"))
    db.commit()
    return redirect(url_for('student_scoreboard'))
