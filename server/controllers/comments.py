import os
from bottle import template, request, redirect
from server import app
from server.models import StartTime
from server.models import Comments

@app.route('/comments/<driver_id>')
def comment(db,driver_id):
    try:
        tabla = db.query(Comments).filter(Comments.driver_group==driver_id).all()
        if len(tabla) == 0:
        	session=db
        	ins = Comments(driver_group=driver_id, comment="")
        	session.add(ins)
        	session.commit()
        	tabla = db.query(Comments).filter(Comments.driver_group==driver_id).all()
    except:
    	pass
    	
    return template('comments.html', tabla=tabla)


@app.post('/comments/add/<driver_id>')
def addComment(db,driver_id):
	comentario = request.forms.get('comment')
	db.query(Comments).filter(Comments.driver_group == driver_id).update({'driver_group':driver_id,'comment':comentario})
	db.commit()
	tabla = db.query(Comments).filter(Comments.driver_group==driver_id).all()
	return template('comments.html', tabla=tabla,flagFile=flagFile)

@app.route('/comments/delete/<driver_id>')
def deleteComment(db,driver_id):
	db.query(Comments).filter(Comments.driver_group==driver_id).delete()
	tabla = db.query(Comments).filter(Comments.driver_group==driver_id).all()
	if len(tabla) == 0:
        	session=db
        	ins = Comments(driver_group=driver_id, comment="")
        	session.add(ins)
        	session.commit()
        	tabla = db.query(Comments).filter(Comments.driver_group==driver_id).all()
	return template('comments.html', tabla=tabla)
	