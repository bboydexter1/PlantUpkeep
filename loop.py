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

def turnOffSystem():
    schedule.clear()
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
    currentTime = datetime.now().time()
    if (currentTime > startTime and currentTime < stopTime) :
        sheduleLamp()
    schedule.every().days.at(str(startTime)).do(sheduleLamp)
    schedule.every().days.at(str(stopTime)).do(cancelSheduleLamp)

def sheduleLamp():
    schedule.every(5).minutes.do(Raspi.ilumantion).tag('lamp')

def cancelSheduleLamp():
    Raspi.turnOffLamps()
    schedule.clear('lamp')

def setupPump():
    currentPreset = Models.CurrentPlant.query.first()
    presetDetails = Models.PlantPreset.query.filter_by(id=currentPreset.plantPreset).first()
    lastWatering = datetime.now() - currentPreset.LastWatering
    daysSinceLastWatering = lastWatering.days
    if (daysSinceLastWatering >= presetDetails.wateringDays) :
        schedule.every().days.at("20:00").do(firstWatering)
        schedule.every().days.at("20:15").do(cancelShedulePump)
    else : 
        waterAfter = presetDetails.wateringDays - daysSinceLastWatering
        schedule.every(waterAfter).days.at("15:00").do(firstWatering)
        schedule.every(waterAfter).days.at("15:15").do(cancelShedulePump)

def firstWatering():
    shedulePump()
    currentPreset = Models.CurrentPlant.query.first()
    presetDetails = Models.PlantPreset.query.filter_by(id=currentPreset.plantPreset).first()
    schedule.every(presetDetails.wateringDays).days.at("15:00").do(shedulePump)
    schedule.every(presetDetails.wateringDays).days.at("15:15").do(cancelShedulePump)
    return schedule.CancelJob

def shedulePump():
    schedule.every(1).seconds.do(Raspi.watering).tag('pump')

def cancelShedulePump():
    Raspi.turnOffPump()
    schedule.clear('pump')

def mainLoop():
    global loopEndFlag
    while loopEndFlag == False:
        schedule.run_pending()
        time.sleep(1)