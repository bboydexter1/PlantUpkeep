#!/usr/bin/env python
from flask import Flask, render_template, redirect, url_for, request, flash, session
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import models as Models
import loop as Loop
import time
import GPIOFuntions as Raspi

@Models.app.route('/')
def index():
    pumpState = Raspi.checkPin(Raspi.RaspiPin.OPump.value)
    lampState = Raspi.checkPin(Raspi.RaspiPin.ORightLamp.value)
    currentPreset = Models.CurrentPlant.query.first()
    presetDetails = Models.PlantPreset.query.filter_by(id=currentPreset.plantPreset).first()
    return render_template('index.html' , pumpStatus = pumpState , lastWatering=currentPreset.LastWatering , lampStatus=lampState , lastIrradiation = currentPreset.LastIrradiation, presetName = presetDetails.name)

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
    return render_template('chosePreset.html' , options = plantSettings )

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
    time.sleep(2)
    return redirect(url_for('index'))

@Models.app.route('/on')
def turnOnSystem():
    Loop.setup()
    return redirect(url_for('index'))

if __name__ == '__main__':
    Loop.setup()
    Models.app.secret_key = 'super secret key'
    Models.app.run(host='0.0.0.0', port= 8080 , debug = True)
