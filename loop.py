#!/usr/bin/env python
from flask import Flask, render_template, redirect, url_for, request
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import time
import schedule as Sched
import models as Models
import GPIOFuntions as Raspi

def setup():
    setupLamp()
    setupPump()

def setupLamp():
    currentPreset = Models.CurrentPlant.query.first()
    presetDetails = Models.PlantPreset.query.filter_by(id=currentPreset.plantPreset).first()
    startTime = presetDetails.lampFrom
    stopTime = presetDetails.lampTo
    schedule.every().day.at(startTime).do(sheduleLamp)
    schedule.every().day.at(stopTime).do(cancelSheduleLamp)

def sheduleLamp():
    schedule.every(5).minutes.do(Raspi.ilumantion).tag('lamp')

def cancelSheduleLamp():
    Raspi.turnOffPin(Raspi.RaspiPin.ORightLamp)
    Raspi.turnOffPin(Raspi.RaspiPin.OLeftLamp)
    schedule.clear('lamp')

def setupPump():
    currentPreset = Models.CurrentPlant.query.first()
    presetDetails = Models.PlantPreset.query.filter_by(id=currentPreset.plantPreset).first()
    startTime = presetDetails.lampFrom
    stopTime = presetDetails.lampTo
    schedule.every(presetDetails.wateringDays).day.at("15:00").do(shedulePump)
    schedule.every(presetDetails.wateringDays).day.at("15:15").do(cancelShedulePump)

def shedulePump():
    schedule.every(10).secounds.do(Raspi.watering).tag('pump')

def cancelShedulePump():
    Raspi.turnOffPin(Raspi.RaspiPin.OPump)
    schedule.clear('pump')

while 1:
    Sched.run_pending()
    time.sleep(1)