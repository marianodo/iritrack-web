import os
from bottle import template, request, redirect
from server import app
from server.models import StartTime
from server.models import Comments
from datetime import *

@app.route('/comments/<driver_id>')
def comment(db,driver_id):
    try:
        tabla = db.query(Comments).filter(Comments.driver_group==driver_id).all()
        driver = driver_id
    except:
        pass

    return template('comments.html', tabla=tabla, driver=driver)


@app.post('/comments/add/<driver_id>')
def addComment(db,driver_id):
    comentario = request.forms.get('comment')
    date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    ins = Comments(driver_group=driver_id, datetime=date, comment=comentario)
    db.add(ins)
    db.commit()
    tabla = db.query(Comments).filter(Comments.driver_group==driver_id).all()
    driver = driver_id
    return template('comments.html', tabla=tabla,  driver=driver)

@app.route('/comments/delete/<ident>/<driver_id>')
def deleteComment(db,ident,driver_id):
    db.query(Comments).filter(Comments.id==ident).delete()
    tabla = db.query(Comments).filter(Comments.driver_group==driver_id).all()
    driver = driver_id
    return template('comments.html', tabla=tabla,  driver=driver)
	