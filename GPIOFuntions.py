#!/usr/bin/env python
from flask_sqlalchemy import SQLAlchemy
import RPi.GPIO as GPIO
from datetime import datetime
import time
from enum import Enum
import models as Models
# Import SPI library (for hardware SPI) and MCP3008 library.
import Adafruit_GPIO.SPI as SPI
import Adafruit_MCP3008


# Hardware SPI configuration:
SPI_PORT   = 0
SPI_DEVICE = 0
mcp = Adafruit_MCP3008.MCP3008(spi=SPI.SpiDev(SPI_PORT, SPI_DEVICE))

#GPIO 11 = lampa lewa
#GPIO 15 = lampa prawa
#GPIO 16 = wlacznik pompy
#mcp.read_adc(0) = fotodioda 1
#mcp.read_adc(1) = fotodioda 2
#mcp.read_adc(2) = miernik wilgoci

class RaspiPin(Enum):
    OLeftLamp = 13
    ORightLamp = 15
    OPump = 11

def setupPins():
    GPIO.setmode(GPIO.BOARD)
    GPIO.setwarnings(False)
    GPIO.setup(RaspiPin.OLeftLamp.value, GPIO.OUT)
    GPIO.output(RaspiPin.OLeftLamp.value, True)
    GPIO.setup(RaspiPin.ORightLamp.value, GPIO.OUT)
    GPIO.output(RaspiPin.ORightLamp.value, True)
    GPIO.setup(RaspiPin.OPump.value, GPIO.OUT)
    GPIO.output(RaspiPin.OPump.value, True)

def checkPin(pin):
    return GPIO.input(pin)

def turnOnPin(pin):
    GPIO.output(pin, True)

def turnOffPin(pin):
    GPIO.output(pin, False)

def turnOnLamps():
    turnOffPin(RaspiPin.OLeftLamp.value)
    turnOffPin(RaspiPin.ORightLamp.value)
    currentPreset = Models.CurrentPlant.query.first()
    currentPreset.LastIrradiation = datetime.now()
    Models.db.session.commit()

def turnOnPump():
    turnOffPin(RaspiPin.OPump.value)
    currentPreset = Models.CurrentPlant.query.first()
    currentPreset.LastWatering = datetime.now()
    Models.db.session.commit()

def turnOffLamps():
    turnOnPin(RaspiPin.OLeftLamp.value)
    turnOnPin(RaspiPin.ORightLamp.value)

def turnOffPump():
    turnOnPin(RaspiPin.OPump.value)

def getHumidityLevel():
    return mcp.read_adc(2)

def getLightLevel():
    return (mcp.read_adc(0) + mcp.read_adc(1))/2

def watering():
    currentPreset = Models.CurrentPlant.query.first()
    presetDetails = Models.PlantPreset.query.filter_by(id=currentPreset.plantPreset).first()
    humidityDetails = Models.Humidity.query.filter_by(id=presetDetails.humidityID).first()
    targetHumidity = humidityDetails.soilHumidity
    if (getHumidityLevel() < targetHumidity):
        turnOnPump()
        return True
    else :
        turnOffPump()
        return False

def ilumantion():
    currentPreset = Models.CurrentPlant.query.first()
    presetDetails = Models.PlantPreset.query.filter_by(id=currentPreset.plantPreset).first()
    iluminationDetails = Models.Brightness.query.filter_by(id=presetDetails.brightnessID).first()
    targetLightLevel = iluminationDetails.brightness
    if (getLightLevel() < targetLightLevel):
        turnOnLamps()
        return True
    else :
        turnOffLamps()
        return False

def getCurrentHumidityText():
    currentPreset = Models.CurrentPlant.query.first()
    presetDetails = Models.PlantPreset.query.filter_by(id=currentPreset.plantPreset).first()
    humidityDetails = Models.Humidity.query.filter_by(id=presetDetails.humidityID).first()
    targetHumidity = humidityDetails.soilHumidity
    return str(int(getHumidityLevel())) + "/" +str(targetHumidity)

def getCurrentIluminationText():
    currentPreset = Models.CurrentPlant.query.first()
    presetDetails = Models.PlantPreset.query.filter_by(id=currentPreset.plantPreset).first()
    iluminationDetails = Models.Brightness.query.filter_by(id=presetDetails.brightnessID).first()
    targetLightLevel = iluminationDetails.brightness
    return str(int(getLightLevel())) + "/" +str(targetLightLevel)

def test():
    setupPins()
    while 1 : 
        print("soil humidity : " + getCurrentHumidityText())
        watering()
        print("light level : " + getCurrentIluminationText())
        ilumantion()
        time.sleep(4)

setupPins()