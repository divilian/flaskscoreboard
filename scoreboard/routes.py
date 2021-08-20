
from flask import current_app, g

@current_app.route('/sup')
def sup():
    return "Sup dude!"

@current_app.route('/')
def dawg():
    return "here dawg"
