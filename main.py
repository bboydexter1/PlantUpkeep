#!/usr/bin/env python
from flask import Flask, render_template, redirect, url_for, request, flash, session
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, time
import models as Models
import loop as Loop
import GPIOFuntions as Raspi
import signal
import sys

def signal_handler(sig, frame):
        Loop.turnOffSystem()
        sys.exit(0)

@Models.app.route('/')
def index():
    pumpStatus = Raspi.checkPin(Raspi.RaspiPin.OPump.value)
    if (pumpStatus == 1):
        pumpStatus = "On"
    else:
        pumpStatus = "Off"
    lampStatus = Raspi.checkPin(Raspi.RaspiPin.ORightLamp.value)
    if (lampStatus == 1):
        lampStatus = "On"
    else:
        lampStatus = "Off"
    currentPreset = Models.CurrentPlant.query.first()
    presetDetails = Models.PlantPreset.query.filter_by(id=currentPreset.plantPreset).first()
    return render_template('index.html' , pumpStatus = pumpStatus , lastWatering=currentPreset.LastWatering , lampStatus=lampStatus , lastIrradiation = currentPreset.LastIrradiation, presetName = presetDetails.name)

@Models.app.route('/addPreset', methods=['GET', 'POST'])
def addPreset():
    humidityOptions = Models.Humidity.query.all()
    brightnessOptions = Models.Brightness.query.all()
    return render_template('addPreset.html' , wateringOptions = humidityOptions , lightOptions = brightnessOptions )

@Models.app.route('/addPresetDataHandle', methods=['GET', 'POST'])
def addPresetDataHandle():
    if request.method == 'POST':
        name = request.form['name']
        lampFrom = request.form['from'].split(":")
        lampTo = request.form['to'].split(":")
        lampFrom = time(hour=int(lampFrom[0]), minute = int(lampFrom[1]))
        lampTo = time(hour=int(lampTo[0]), minute = int(lampTo[1]))
        wateringDays = request.form['daysCount']
        brightnessID = request.form['ilumnatingType']
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

@Models.app.route('/changePlantSettingsHandler', methods=['GET', 'POST'])
def changePlantSettingsHandler():
    if request.method == 'POST':
        plant = Models.CurrentPlant.query.first()
        plant.plantPreset = request.form['preset']
        Models.db.session.commit()
        return redirect(url_for('index'))
    else:
        return redirect(url_for('changePlantSettings'))

@Models.app.route('/off')
def turnOffSystem():
    Loop.turnOffSystem()
    return redirect(url_for('index'))

@Models.app.route('/on')
def turnOnSystem():
    Loop.setup()
    return redirect(url_for('index'))

@Models.app.route('/lamp/<state>')
def changeLampState(state):
    if (state == "on"):
        Raspi.turnOnPin(Raspi.RaspiPin.OLeftLamp.value)
        Raspi.turnOnPin(Raspi.RaspiPin.ORightLamp.value)
    elif  (state == "off") :
        Raspi.turnOffPin(Raspi.RaspiPin.OLeftLamp.value)
        Raspi.turnOffPin(Raspi.RaspiPin.ORightLamp.value)
    return redirect(url_for('index'))

@Models.app.route('/pump/<state>')
def changePumpState(state):
    if (state == "on"):
        Raspi.turnOnPin(Raspi.RaspiPin.OPump.value)
    elif  (state == "off") :
        Raspi.turnOffPin(Raspi.RaspiPin.OPump.value)
    return redirect(url_for('index'))

if __name__ == '__main__':
    Loop.setup()
    signal.signal(signal.SIGINT, signal_handler)
    Models.app.secret_key = 'super secret key'
    Models.app.run(host='0.0.0.0', port= 8080 , debug = False)