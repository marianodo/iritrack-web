#!/usr/bin/python
# -*- coding: utf-8 -*-
# -*- coding: latin-1-*-
# coding: utf-8
import os
import xlrd
from bottle import template, request, redirect
from server import app
from server.models import StartTime
from server.services import xlsParser
from time import mktime
from datetime import *

import unicodedata
import urllib2
from cookielib import CookieJar
from urllib2 import urlopen
from bs4 import BeautifulSoup as bs

cj = CookieJar()
opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))



@app.post('/starttimes/<stage_id>')
@app.route('/starttimes/<stage_id>')
def index(db,stage_id):
	try:
		rows = db.query(StartTime).filter(StartTime.stage_id==stage_id).all()
		count = db.query(StartTime.stage_id).distinct().count()
	except:
		pass
	return template('starttimes.html', rows=rows, stage=stage_id, count=count,flagFile=True)

@app.route('/starttimes', method='POST')
def set_start_time(db):
	name = request.forms.get('name')
	driver_id = request.forms.get('driver_id')
	db.add(Driver(driver_id=driver_id, name=name))
	redirect('/starttimes/1')

@app.route('/starttimes/upload', method='POST')
def do_upload(db):
	addtime = request.forms.get('addtime')
	stage_id = request.forms.get('stageId')
	session=db
	upload = request.files.get('starttimes')
	try:

		headers = ['orden', 'driver_id', 'name', 'country', 'starttime']
		doc = xlsParser(upload.file.read(), headers=headers).toStartTime()
		try:
			db.query(StartTime).filter(StartTime.stage_id==stage_id).delete()
		except:
			flag = 0
		sheet= doc.sheet_by_index(0)
		nrows = sheet.nrows
		book_datemode = doc.datemode
		timetmp = time(0,0,0) #Tiempo temporal, es para hacer la comparacion
		for i in range(nrows):
			id_driver = sheet.cell(i,0)
			id_group = sheet.cell(i,1)
			name_driver = sheet.cell(i,2)
			county_driver =  sheet.cell(i,3)
			time_driver = sheet.cell(i,4)
			year, month, day, hour, minute, second = xlrd.xldate_as_tuple(time_driver.value, book_datemode) #separo la fecha de la celda del excel
			minute = minute + int(addtime)
			timedr = timedelta(hours=hour,minutes=minute ,seconds=second)
			#timedr = timedr + timedelta(minutes=int(addtime))
			if timedr == timetmp:
				timedr=timedelta(hours=hour,minutes=minute,seconds=30)
			timerun = StartTime(id = i,driver_group=int(id_group.value), name=name_driver.value,start_time= str(timedr),stage_id=str(stage_id))
			timetmp = timedr
			session.add(timerun)
			
		session.commit()
	except:
		return template('starttimes.html', rows="", stage=1, count="",flagFile=False)
	redirect('/starttimes/1')
	

@app.route('/starttimes/editar/<stage>/<driver_id>')
def edit_driver(db,stage,driver_id):
	start_times = db.query(StartTime).filter(StartTime.driver_group==driver_id,StartTime.stage_id==stage).first() #busco el start time del alpha indicado
	return template('editar.html', drivers = start_times)

@app.route('/starttimes/update', method='POST')
def update_edit_driver(db):
	driver_id = request.forms.get('driverid')
	name = request.forms.get('name').replace('&nbsp',' ')
	startime = request.forms.get('startime')
	stage = request.forms.get('stage')

	#update(StartTime).where(StartTime.driver_id == driver_id).values(driver_id=driver_id,start_time=startime,name=name)
	db.query(StartTime).filter(StartTime.driver_group == driver_id,StartTime.stage_id == stage).update({'driver_group':driver_id,'start_time':startime,'name':name.decode("utf-8"),'stage_id':stage})
	db.commit()
	redirect('/starttimes/1')
	

@app.route('/starttimes/deletall/<stage_id>')
def deleteall(db,stage_id):
	db.query(StartTime).filter(StartTime.stage_id == stage_id).delete()

	redirect('/starttimes/1')

@app.post('/starttimes/web')
def uploadWeb(db):
	stageId = request.forms.get('stageId')
	addtime = request.forms.get('addtime')
	url = request.forms.get('url')
	codigoHTML = opener.open (url).read()
	soap = bs(urllib2.urlopen(url))       # Paso el código HTML a BeautifulSoap
	tabla = soap.find('table')
	trs = tabla.findAll('tr')
	for tr in trs:
		tds = tr.findAll('td')
		tmp = []
		for j,td in enumerate(tds): # Imprime cada TD por separado

			tmpData = td.string
			if j == 6: 
				try:
					time = td.string.replace('.',':')
					time = time.replace(' ','')
					time = "0" + time + ":00"
					t = datetime.strptime(time, '%H:%M:%S')
					timedr = timedelta(hours=t.hour,minutes=t.minute ,seconds=t.second)
					timedr =timedelta(hours=t.hour,minutes=t.minute + int(addtime) ,seconds=t.second)
					tmpData = str(timedr)
				except:
					pass
			tmp.append(tmpData)
		try:
			if len(tmpData) > 6: #esto es porque los primeros tiempo los toma como 8.26 en vez de 08:26:00
				name = ''.join((c for c in unicodedata.normalize('NFD', tmp[2].replace('&nbsp',' ')) if unicodedata.category(c) != 'Mn'))
				timerun = StartTime(id = int(tmp[0]),driver_group=int(tmp[1]), name=name,start_time= str(tmpData),stage_id=stageId)
				db.add(timerun)
		except:
			pass
	redirect('/starttimes/1')
	
