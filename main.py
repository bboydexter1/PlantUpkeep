#!/usr/bin/env python
from flask import Flask, render_template, redirect, url_for, request, flash, session
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, time
import models as Models
import loop as Loop
import GPIOFuntions as Raspi
import signal
import sys
import json

def signal_handler(sig, frame):
        Loop.turnOffSystem()
        sys.exit(0)

@Models.app.route('/')
def index():
    brightnessOptions = Models.Brightness.query.all()
    humidityOptions = Models.Humidity.query.all()
    pumpStatus = Raspi.checkPin(Raspi.RaspiPin.OPump.value)
    if (pumpStatus == 1):
        pumpStatus = "Off"
    else:
        pumpStatus = "On"
    lampStatus = Raspi.checkPin(Raspi.RaspiPin.ORightLamp.value)
    if (lampStatus == 1):
        lampStatus = "Off"
    else:
        lampStatus = "On"
    currentPreset = Models.CurrentPlant.query.first()
    presetDetails = Models.PlantPreset.query.filter_by(id=currentPreset.plantPreset).first()
    return render_template('index.html' , pumpStatus = pumpStatus , lastWatering=currentPreset.LastWatering , lampStatus=lampStatus , lastIrradiation = currentPreset.LastIrradiation, presetName = presetDetails.name , currentHumidty = Raspi.getCurrentHumidityText() , currentIlumination = Raspi.getCurrentIluminationText())

@Models.app.route('/addPreset') 
def addPreset():
    humidityOptions = Models.Humidity.query.all()
    brightnessOptions = Models.Brightness.query.all()
    return render_template('addPreset.html' , wateringOptions = humidityOptions , lightOptions = brightnessOptions )

@Models.app.route('/iluminationtypes') 
def getIlumitationTypes():
    brightnessOptions = Models.Brightness.query.all()
    jsonFormat = []
    for type in brightnessOptions :
        jsonFormat.append([type.name , type.brightness])
    return json.dumps(jsonFormat)

@Models.app.route('/wateringtypes') 
def getWateringTypes():
    humidityOptions = Models.Humidity.query.all()
    jsonFormat = []
    for type in humidityOptions :
        jsonFormat.append([type.name , type.soilHumidity])
    return json.dumps(jsonFormat)

@Models.app.route('/addPresetDataHandle', methods=['POST'])
def addPresetDataHandle():
    if request.method == 'POST':
        name = request.form['name']
        lampFrom = request.form['from'].split(":")
        lampTo = request.form['to'].split(":")
        lampFrom = time(hour=int(lampFrom[0]), minute = int(lampFrom[1]))
        lampTo = time(hour=int(lampTo[0]), minute = int(lampTo[1]))
        wateringDays = request.form['daysCount']
        brightnessID = request.form['iluminationType']
        humidityID = request.form['wateringType']
        newPlant = Models.PlantPreset(name = name,lampFrom = lampFrom , lampTo = lampTo , wateringDays = wateringDays , brightnessID = brightnessID , humidityID = humidityID)
        Models.db.session.add(newPlant)
        Models.db.session.commit()
        return redirect(url_for('index'))
    else:
        return redirect(url_for('addPreset'))

@Models.app.route('/changePlantSettings')
def changePlantSettings():
    plantSettings = Models.PlantPreset.query.all()
    brightnessOptions = Models.Brightness.query.all()
    humidityOptions = Models.Humidity.query.all()
    return render_template('chosePreset.html' , options = plantSettings, brightnessOptions = brightnessOptions, humidityOptions = humidityOptions )

@Models.app.route('/getplantsettings')
def getplantsettings():
    plantSettings = Models.PlantPreset.query.all()
    brightnessOptions = Models.Brightness.query.all()
    humidityOptions = Models.Humidity.query.all()
    jsonFormat = ["name" , "lampFrom" , "lampTo" , "wateringDays" , "brightnessName" , "brightnessPower" , "humidityName" , "humidityPower"]
    for type in plantSettings :
        brightness = brightnessOptions[type.brightnessID]
        humidity = humidityOptions[type.humidityID]
        jsonFormat.append([type.name , type.lampFrom , type.lampTo , type.wateringDays , brightness.name , brightness.brightness , humidity.name , humidity.soilHumidity])
    return json.dumps(jsonFormat)

@Models.app.route('/changePlantSettingsHandler', methods=['POST'])
def changePlantSettingsHandler():
    if request.method == 'POST':
        Loop.turnOffSystem()
        plant = Models.CurrentPlant.query.first()
        plant.plantPreset = request.form['preset']
        Models.db.session.commit()
        Loop.setup()
        return redirect(url_for('index'))
    else:
        return redirect(url_for('changePlantSettings'))

@Models.app.route('/off', methods=['GET', 'PUT'])
def turnOffSystem():
    Loop.turnOffSystem()
    if request.method == 'GET':
        return redirect(url_for('index'))
    else : 
        return "system is off"

@Models.app.route('/on', methods=['GET' , 'PUT'])
def turnOnSystem():
    Loop.setup()
    if request.method == 'GET':
        return redirect(url_for('index'))
    else : 
        return "system is on"

@Models.app.route('/lamp/<state>' , methods=['GET' , 'PUT'])
def changeLampState(state):
    if (state == "on"):
        Raspi.turnOnLamps()
    elif  (state == "off") :
        Raspi.turnOffLamps()
    if request.method == 'GET':
        return redirect(url_for('index'))
    else : 
        return "lamp is "+state

@Models.app.route('/pump/<state>' , methods=['GET' , 'PUT'])
def changePumpState(state):
    if (state == "on"):
        Raspi.turnOnPump()
    elif  (state == "off") :
        Raspi.turnOffPump()
    if request.method == 'GET':
        return redirect(url_for('index'))
    else : 
        return "pump is "+state

if __name__ == '__main__':
    Loop.setup()
    signal.signal(signal.SIGINT, signal_handler)
    Models.app.secret_key = 'super secret key'
    Models.app.run(host='0.0.0.0', port= 8080 , debug = False)