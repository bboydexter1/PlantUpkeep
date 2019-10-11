#!/usr/bin/env python
from flask import Flask, render_template, redirect, url_for, request
from flask_sqlalchemy import SQLAlchemy
import RPi.GPIO as GPIO
from datetime import datetime , time

#GPIO 8 = lampka testowa
#GPIO 11 = sensor wilgoci
#GPIO 13 = lampa lewa
#GPIO 15 = lampa prawa
#GPIO 16 = wlacznik pompy

def setupPins():
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

def checkPin(pin):
    return GPIO.input(pin)

def turnOnPin(pin):
    GPIO.output(pin, False)

def turnOffPin(pin):
    GPIO.output(pin, False)


