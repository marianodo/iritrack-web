import os
from bottle import template, request, redirect
from server import app
from server.models import Stage
from server.services import xlsParser
from sqlalchemy import func
import csv, pyodbc
import simplekml
import zipfile
from bottle import static_file
from polycircles import polycircles
@app.route('/mapkml')
def index(db):
	try:
		os.remove("C:/Users/Nano/Desktop/iritrac-robots-master/tmp/*")
	except:
		pass
	return template('mapkml.html', flagFile="")

@app.post('/mapkml')
def do_upload(db):

	upload = request.files.get('map')
	
	
	file_path = os.getcwd() + "/tmp/{file}".format(file=upload.filename)
	upload.save(file_path)
	
	MDB = file_path 
	DRV = '{Microsoft Access Driver (*.mdb)}'; PWD = 'pw'
	
	name = upload.filename[:-4]

	extension = MDB[:3]
	zipname = "tmp/" + name + ".zip"
	zf = zipfile.ZipFile(zipname, mode='w')
	# connect to db
	con = pyodbc.connect('DRIVER={};DBQ={}'.format(DRV,MDB))
	cur = con.cursor()

	# run a query and get the results 
	countStage = 'select distinct(CodeRoute) from tbWpt'
	stages = cur.execute(countStage).fetchall()

	for stage in stages:
		
		SQL = 'SELECT * FROM tbWpt where CodeRoute = %s;'%(stage.CodeRoute) # your query goes here

		rows = cur.execute(SQL).fetchall()
		
		
		pathNametxt = name +'.txt'

		with open(pathNametxt, 'wb') as fou:
		    csv_writer = csv.writer(fou) # default field-delimiter is ","
		    csv_writer.writerows(rows)


		kml = simplekml.Kml() #Creo el archivo

		archi=open(pathNametxt,'r')
		linea=archi.readline()
		coo = []
		while linea!="":
			valores = []
			valores = linea.split(",")
			nombre = valores[2]
			grados = valores[4]
			minutos = valores[5]
			segundos = float(valores[6])/1000*60
			hef = valores[7]
			gradoslon = valores[8]
			minutoslon = valores[9]
			segundoslon = float(valores[10])/1000*60
			heflon = valores[11]
			radiusWpt = valores[13]
			radiusVis = valores[14]
			a = formatearADecimal(grados,minutos,segundos) #Convierto las coordenadas
			b = formatearADecimal(gradoslon,minutoslon,segundoslon)
			#punto = kml.newpoint(name="K", coords=[(b,a)])
			
			if valores[19] == 'True':
				WPM = "Wpm"
			else:
				WPM = ""
			nameWpt = nombre + "(" + radiusWpt + "," + radiusVis + ")" + WPM
			pnt = kml.newpoint(name=nameWpt)
			pnt.coords = [(b, a)]
			pnt.style.labelstyle.color = simplekml.Color.red  # Make the text red
			pnt.style.labelstyle.scale = 1  # Make the text twice as big
			pnt.style.iconstyle.icon.href = 'http://maps.google.com/mapfiles/kml/shapes/placemark_circle.png'
			pnt.style.iconstyle.icon.scale = int(valores[13])

			polycircle = polycircles.Polycircle(latitude=float(a),longitude=float(b),radius=int(radiusWpt), number_of_vertices=36)
			pol = kml.newpolygon(name="Columbus Circle, Manhattan", outerboundaryis=polycircle.to_kml())
			pol.style.polystyle.color = simplekml.Color.changealphaint(200, simplekml.Color.green)
			try:

				coo += [(b,a)]
			except:
				coo= [(b,a)]
			
			linea=archi.readline()

		ls = kml.newlinestring(name='A LineString')
		ls.coords = coo
		ls.extrude = 1
		ls.altitudemode = simplekml.AltitudeMode.relativetoground
		ls.style.linestyle.width = 5
		ls.style.linestyle.color = simplekml.Color.blue
		

		pathName = name + " -" + str(stage.CodeRoute) + '.kml'
		kml.save(pathName)
		zf.write(pathName)
		os.remove(pathName)

	zf.close()
	cur.close()
	con.close()	
	os.remove(file_path)
	return static_file(zipname, root='')
	return template('mapkml.html', flagFile=True)

def formatearADecimal( grados, minutos, segundos ):
	signo = ''
	grados = float( grados )    
	minutos = float( minutos )
	#segundos = float( segundos.replace(",",".") )
	if grados < 0:
		grados = math.fabs( grados )
		signo = '-'
	return '-' + "" + str( grados + (minutos/60) + (segundos/3600) )