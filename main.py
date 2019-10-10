#!/usr/bin/env python
from flask import Flask, render_template, redirect, url_for, request, flash, session
from flask_sqlalchemy import SQLAlchemy
import RPi.GPIO as GPIO
from datetime import datetime , time
import models as Models

#GPIO 8 = lampka testowa
#GPIO 11 = sensor wilgoci
#GPIO 13 = lampa lewa
#GPIO 15 = lampa prawa
#GPIO 16 = wlacznik pompy

GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)
GPIO.setup(8, GPIO.OUT)
GPIO.output(8, False)
GPIO.setup(11, GPIO.IN)
GPIO.setup(13, GPIO.OUT)
GPIO.output(13, False)
GPIO.setup(15, GPIO.OUT)
GPIO.output(15, False)
GPIO.setup(16, GPIO.OUT)
GPIO.output(16, False)

@Models.app.route('/')
def index():
    state = GPIO.input(8)
    currentPreset = Models.CurrentPlant.query.first()
    presetDetails = Models.PlantPreset.query.filter_by(id=currentPreset.plantPreset).first()
    return render_template('index.html' , pumpStatus = state , lastWatering=currentPreset.LastWatering , lampStatus=0 , lastIrradiation = currentPreset.LastIrradiation, presetName = presetDetails.name)

@Models.app.route('/addPreset', methods=['GET', 'POST'])
def addPreset():
    GPIO.output(8, False)
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

@Models.app.route('/test',methods = ["POST"])
def test():
    flash("flash test")
    return render_template('test.html')

if __name__ == '__main__':
    Models.app.secret_key = 'super secret key'
    Models.app.run(host='0.0.0.0', port= 8080 , debug = True)
