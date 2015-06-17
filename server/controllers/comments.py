import os
from bottle import template, request, redirect
from server import app
from server.models import StartTime
from server.models import Comments

@app.route('/comments/<driver_id>')
def comentario(db,driver_id):
    try:
        tabla = db.query(Comments).filter(Comments.driver_group==driver_id).all()

    except:

        pass
    return template('comments.html', tabla=tabla)