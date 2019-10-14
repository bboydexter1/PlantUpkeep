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
    GPIO.output(RaspiPin.OLeftLamp.value, False)
    GPIO.setup(RaspiPin.ORightLamp.value, GPIO.OUT)
    GPIO.output(RaspiPin.ORightLamp.value, False)
    GPIO.setup(RaspiPin.OPump.value, GPIO.OUT)
    GPIO.output(RaspiPin.OPump.value, False)

def checkPin(pin):
    return GPIO.input(pin)

def turnOnPin(pin):
    GPIO.output(pin, False)

def turnOffPin(pin):
    GPIO.output(pin, False)

def getHumidityLevel():
    return mcp.read_adc(2)

def getLightLevel():
    return (mcp.read_adc(0) + mcp.read_adc(1))/2

def watering():
    currentPreset = Models.CurrentPlant.query.first()
    presetDetails = Models.PlantPreset.query.filter_by(id=currentPreset.plantPreset).first()
    humidityDetails = Models.Humidity.query.filter_by(id=presetDetails.humidityID).first()
    targetHumidity = humidityDetails.soilHumidity
    print("H lvl : " + str(getHumidityLevel()) + "/" + str(targetHumidity))
    if (getHumidityLevel() < targetHumidity):
        GPIO.output(RaspiPin.OPump.value, True)
        print("watering")
        return True
    else :
        GPIO.output(RaspiPin.OPump.value, False)
        return False

def ilumantion():
    currentPreset = Models.CurrentPlant.query.first()
    presetDetails = Models.PlantPreset.query.filter_by(id=currentPreset.plantPreset).first()
    iluminationDetails = Models.Brightness.query.filter_by(id=presetDetails.brightnessID).first()
    targetLightLevel = iluminationDetails.brightness
    print("L lvl : " + str(getLightLevel()) + "/" + str(targetLightLevel))
    if (getLightLevel() < targetLightLevel):
        GPIO.output(RaspiPin.OLeftLamp.value, True)
        GPIO.output(RaspiPin.ORightLamp.value, True)
        print("iluminating")
        return True
    else :
        GPIO.output(RaspiPin.OLeftLamp.value, False)
        GPIO.output(RaspiPin.ORightLamp.value, False)
        return False

def test():
    setupPins()
    while 1 : 
        watering()
        ilumantion()
        time.sleep(4)