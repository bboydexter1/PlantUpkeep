#!/usr/bin/env python
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import time
import schedule
import models as Models
import GPIOFuntions as Raspi
import threading

loopEndFlag = False

def setup():
    global loopEndFlag
    loopEndFlag = True
    Raspi.setupPins()
    setupLamp()
    setupPump()
    runThreaded(mainLoop)
    schedule.every().minutes.do(turnOffSystem)

def turnOffSystem():
    global loopEndFlag
    loopEndFlag = True

def runThreaded(job_func):
    global loopEndFlag
    loopEndFlag = False
    jobThread = threading.Thread(target=job_func)
    jobThread.start()

def setupLamp():
    currentPreset = Models.CurrentPlant.query.first()
    presetDetails = Models.PlantPreset.query.filter_by(id=currentPreset.plantPreset).first()
    startTime = presetDetails.lampFrom
    stopTime = presetDetails.lampTo
    schedule.every().days.at(str(startTime)).do(sheduleLamp)
    schedule.every().days.at(str(stopTime)).do(cancelSheduleLamp)

def sheduleLamp():
    schedule.every(5).minutes.do(Raspi.ilumantion).tag('lamp')

def cancelSheduleLamp():
    Raspi.turnOffPin(Raspi.RaspiPin.ORightLamp)
    Raspi.turnOffPin(Raspi.RaspiPin.OLeftLamp)
    currentPreset = Models.CurrentPlant.query.first()
    currentPreset.LastIrradiation = datetime.now()
    Models.db.session.commit()
    schedule.clear('lamp')

def setupPump():
    currentPreset = Models.CurrentPlant.query.first()
    presetDetails = Models.PlantPreset.query.filter_by(id=currentPreset.plantPreset).first()
    startTime = presetDetails.lampFrom
    stopTime = presetDetails.lampTo
    schedule.every(presetDetails.wateringDays).days.at("15:00").do(shedulePump)
    schedule.every(presetDetails.wateringDays).days.at("15:10").do(cancelShedulePump)

def shedulePump():
    schedule.every(1).minutes.do(Raspi.watering).tag('pump')

def cancelShedulePump():
    Raspi.turnOffPin(Raspi.RaspiPin.OPump)
    currentPreset = Models.CurrentPlant.query.first()
    currentPreset.LastWatering = datetime.now()
    Models.db.session.commit()
    schedule.clear('pump')

def mainLoop():
    global loopEndFlag
    while loopEndFlag == False:
        schedule.run_pending()
        time.sleep(1)