#!/usr/bin/env python
from flask import Flask, render_template, redirect, url_for, request
from flask_sqlalchemy import SQLAlchemy
import RPi.GPIO as GPIO
from datetime import datetime , time
from enum import Enum
# Import SPI library (for hardware SPI) and MCP3008 library.
import Adafruit_GPIO.SPI as SPI
import Adafruit_MCP3008

# Hardware SPI configuration:
SPI_PORT   = 0
SPI_DEVICE = 0
mcp = Adafruit_MCP3008.MCP3008(spi=SPI.SpiDev(SPI_PORT, SPI_DEVICE))

#GPIO 8 = lampka testowa
#GPIO 13 = lampa lewa
#GPIO 15 = lampa prawa
#GPIO 16 = wlacznik pompy
#mcp.read_adc(0) = fotodioda 1
#mcp.read_adc(1) = fotodioda 2
#mcp.read_adc(2) = miernik wilgoci

class RaspiPin(Enum):
    OTestLamp = 8
    OLeftLamp = 13
    ORightLamp = 15
    OPump = 16

def setupPins():
    GPIO.setmode(GPIO.BOARD)
    GPIO.setwarnings(False)
    GPIO.setup(RaspiPin.OTestLamp, GPIO.OUT)
    GPIO.output(RaspiPin.OTestLamp, False)
    #GPIO.setup(11, GPIO.IN)
    GPIO.setup(RaspiPin.OLeftLamp, GPIO.OUT)
    GPIO.output(RaspiPin.OLeftLamp, False)
    GPIO.setup(RaspiPin.ORightLamp, GPIO.OUT)
    GPIO.output(RaspiPin.ORightLamp, False)
    GPIO.setup(RaspiPin.OPump, GPIO.OUT)
    GPIO.output(RaspiPin.OPump, False)

def checkPin(pin):
    return GPIO.input(pin)

def turnOnPin(pin):
    GPIO.output(pin, False)

def turnOffPin(pin):
    GPIO.output(pin, False)

def getHumidityLevel():
    return mcp.read_adc(2)

def getLightLevel():
    return ((mcp.read_adc(0)+mcp.read_adc(1))/2)

def watering():
    targetHumidity = 512 # change to get this from models
    if (getHumidityLevel() < targetHumidity):
        GPIO.output(RaspiPin.OPump, True)
        return True
    else :
        GPIO.output(RaspiPin.OPump, False)
        return False

def ilumantion(pin):
    targetLightLevel = 256 # change to get this from models
    if (getLightLevel() < targetLightLevel):
        GPIO.output(RaspiPin.OLeftLamp, True)
        GPIO.output(RaspiPin.ORightLamp, True)
        return True
    else :
        GPIO.output(RaspiPin.OLeftLamp, False)
        GPIO.output(RaspiPin.ORightLamp, False)
        return False



