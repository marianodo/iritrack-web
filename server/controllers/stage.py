import os
from bottle import template, request, redirect
from server import app
from server.models import Stage
from server.services import xlsParser
from sqlalchemy import func

@app.route('/stage/<stage_id>')
@app.post('/stage/<stage_id>')
def index(db,stage_id):
	try:
		zones = db.query(Stage).filter(Stage.stage_id==stage_id).all()
		count = db.query(Stage.stage_id).distinct().count()
	except:
		stage = 0
		count = 0
	
	return template('stage.html', zones=zones,stage_id=stage_id,count=count,flagFile=True)
	

@app.route('/stage/deletall')
def deleteall(db):
	db.query(Stage).delete()
	return template('stage.html', zones="",stage_id=0,count=0, flagFile=True)

@app.route('/stage/upload', method='POST')
def do_upload(db):
	upload = request.files.get('stage')
	
	try:
		doc = xlsParser(upload.file.read(), headers="").toStartTime()
		sheet = doc.sheet_by_index(0) #Selecciono la hoja uno
		ncols = sheet.ncols
		nrows = sheet.nrows
		i = 1
		for col in range(ncols):
			for row in range(1,nrows):
				if sheet.cell(row,col).value <> "":
					insertStage = Stage(stage_id = i ,zone=sheet.cell(row,col).value)
					db.add(insertStage)
			i += 1
		db.commit()
		try:
			zones = db.query(Stage).filter(Stage.stage_id==1).all()
		except:
			pass
		count = db.query(Stage.stage_id).distinct().count()
		flagFile=True
	except:
		flagFile=False
		zones = ""
		count = ""
	return template('stage.html', zones=zones,stage_id=1,count=count, flagFile=flagFile)
