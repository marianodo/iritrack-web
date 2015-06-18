from bottle import template, request,redirect
from server import app
from server.models import Data
from server.models import Driver
from server.models import Stage
from server.models import StartTime
from server.models import LastUpdate
from server.models import DateUpdate
from server.models import DateDriverUpdate
from time import mktime
from datetime import *
from server.services import dataFetch
@app.route('/resultado/<stage_id>')
def index(db,stage_id):
    
    drivers=db.query(StartTime.driver_group,StartTime.start_time).filter(StartTime.stage_id==stage_id).all() #Busco todos los driver_id que se generaron por el excel largadas.xls
    zones = db.query(Stage.zone).filter(Stage.stage_id==stage_id).all() #cambiar el stage_id cuando cambie de etapa
    start_times = drivers

    try:
        last_update = db.query(LastUpdate.time).filter(LastUpdate.id =="1").one() #Me trae la ultima fecha de actualizacion
    except:
        last_update= " "

    vector_driver = []
    vector_zone = []
    vector_time = []
    
    tiemporsultado = []
    zonaresultado = []
    tiempolastresultado = []
    zonalastresultado = []
    vector_start_time = []
    myArray = []
    starttimedr = []
    for start_time in start_times:
        vector_start_time.append(start_time.start_time)
    
    for zone in zones:    
        vector_zone.append(zone.zone)
        timename = "time" + zone.zone

    #con esto logre tener en vectores los alpha,drivers y las zonas dependiendo de la etapa    
    for i,driver in enumerate(drivers):
        
        vector_driver.append(driver.driver_group)
        #Agarra un alpha y pregunta por todas las zonas, sig alpha y pregunta de vuelta por todas las zonas
        vehicle_num = driver.driver_group

        start_time_tmp = datetime.strptime(vector_start_time[i], '%H:%M:%S') #Convierto en datetime para poder restar dsp
        vector_time.append(vector_start_time[i])

        for zone in zones:
            
                date_per_zones = db.query(Data.date).filter(Data.vehicle==vehicle_num, Data.zone==zone.zone).first() #Busco la hora por la que paso en la zona, si no esta, salta un except
                if date_per_zones == None: #Si me da none es porque no paso por esa zona
                    tiemporsultado.append(' ')
                    zonaresultado.append(' ')
                else:
                    date_per_zone=str(date_per_zones[0]).split("'")
                    date_per_zone = datetime.strptime(date_per_zone[0], '%Y-%m-%d %H:%M:%S')
                    hora_zona = str(date_per_zone.hour)
                    minuto_zona = str(date_per_zone.minute)
                    segundo_zona = str(date_per_zone.second)
                    if len(hora_zona) == 1:
                        hora_zona= "0" + hora_zona
                    if len(minuto_zona) == 1:
                        minuto_zona= "0" + minuto_zona
                    if len(segundo_zona) == 1:
                        segundo_zona= "0" + segundo_zona
                    date_zone = hora_zona + ":" + minuto_zona + ":" + segundo_zona    
                    result = date_per_zone - start_time_tmp
                    result =  str(result).split(",")
                    tiemporsultado.append(date_zone)
                    zonaresultado.append(result[1])
            
    count = db.query(Stage.stage_id).distinct().count()    
    return template('result.html', vehiculo=vector_driver, fecha=last_update[0],zonename = vector_zone,  zoneresult=zonaresultado,timeresult=tiemporsultado,startime=vector_time, stage_id=stage_id,count=count)

@app.route('/resultado/show', method='POST')
def refresh(db):
    stage_id = request.forms.get('stage')
    redirect('/resultado/%s'% stage_id)
    
@app.post('/resultado')
def searchData(db):
    dateFrom = request.forms.get('from')
    dateTo = request.forms.get('to')
    stage_id = request.forms.get('stage_id')

    fecha_desde = dateFrom + ' 00:00'
    t = datetime.strptime(fecha_desde, '%Y-%m-%d %H:%M')
    t = t - timedelta(hours=3) #Convierto a UTC - 3
    fecha_desde = mktime(t.timetuple())

    fecha_hasta = dateTo + " " + ' 23:59'
    t = datetime.strptime(fecha_hasta, '%Y-%m-%d %H:%M')
    t = t - timedelta(hours=3) #Convierto a UTC - 3
    fecha_hasta = mktime(t.timetuple())
    
    if fecha_desde == fecha_hasta:
        time_now = datetime.now().strftime("%H:%M")
        fecha_hasta = dateTo + " " + time_now
        t = datetime.strptime(fecha_hasta, '%Y-%m-%d %H:%M')
        t = t - timedelta(hours=3) #Convierto a UTC - 3
        fecha_hasta = mktime(t.timetuple())    
    
    #dataFetch(fecha_desde,fecha_hasta).firstFetch()
    firstdriver = db.query(StartTime.driver_group,StartTime.gid).filter(StartTime.stage_id==1,StartTime.gid==1).first()
    db.query(DateUpdate).delete()
    date = DateUpdate(id=1,firstDate= fecha_desde, secondDate=fecha_hasta,lastId=firstdriver.gid)
    db.add(date)
    db.commit()

    dataFetch(fecha_desde,fecha_hasta).firstnewFetch(firstdriver.driver_group)
    redirect('/resultado/%s'% stage_id)
    
@app.route('/result/deletall')
def deleteall(db):
    db.query(Data).delete()
    redirect('/resultado/1')

@app.post('/resultado/update/<stage_id>')
@app.route('/resultado/update/<stage_id>')
def updateData(db,stage_id):   
    dataFetch("a","b").updateAll()  
    redirect('/resultado/%s'% stage_id)
