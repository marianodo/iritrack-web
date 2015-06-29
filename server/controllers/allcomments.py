import os
from bottle import template, request, redirect
from server import app
from server.models import StartTime
from server.models import Comments
from datetime import *

@app.route('/allcomments')
def allComments(db):
	try:
		tabla = db.query(Comments).all()

	except:
		pass

	return template('allcomments.html', tabla=tabla)

@app.route('/allcomments/delete/<ident>')
def deleteAllComments(db,ident):
	db.query(Comments).filter(Comments.id==ident).delete()
	tabla = db.query(Comments).all()
	return template('allcomments.html', tabla=tabla)