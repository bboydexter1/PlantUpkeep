#!/usr/bin/env python
from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)
GPIO.setup(8, GPIO.OUT)
GPIO.output(8, False)

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'

db = SQLAlchemy(app)

temp = False

class CurrentPlant(db.Model):
    __tablename__ = 'currentPlant'
    id = db.Column(db.Integer, primary_key=True)
    LastWatering = db.Column(db.DateTime, nullable=True)
    LastIrradiation = db.Column(db.DateTime, nullable=True)
    plantPreset = db.Column(db.Integer, db.ForeignKey('plantPreset.id'), nullable=False)
    
class PlantPreset(db.Model):
    __tablename__ = 'plantPreset'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), unique=True, nullable=False)
    lampFrom = db.Column(db.Time, nullable=True)
    lampTo = db.Column(db.Time, nullable=True)
    brightnessID = db.Column(db.Integer, db.ForeignKey('brightness.id'), nullable=True)
    humidityID = db.Column(db.Integer, db.ForeignKey('humidity.id'), nullable=True)
    
        
class Brightness(db.Model):
    __tablename__ = 'brightness'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), unique=True, nullable=False)
    brightness = db.Column(db.Integer, nullable=False)
    #preset = db.relationship("PlantPreset")
    
    
class Humidity(db.Model):
    __tablename__ = 'humidity'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), unique=True, nullable=False)
    soilHumidity = db.Column(db.Integer, nullable=False)
    #preset = db.relationship("PlantPreset")
    

@app.route('/')
def index():
    state = GPIO.input(8)
    CP = CurrentPlant.query.first()
    return render_template('index.html' , pumpStatus = state , lastWatering=CP.LastWatering , lampStatus=False , lastIrradiation = CP.LastIrradiation)

@app.route('/lamp')
def lamp():
    GPIO.output(8, True)
    brightnessOptions = Brightness.query.all()
    return render_template('lamp.html' ,  options = brightnessOptions)

@app.route('/pump')
def pump():
    GPIO.output(8, False)
    humidityOptions = Humidity.query.all()
    return render_template('pump.html' , options = humidityOptions )

if __name__ == '__main__':
    app.run(host='0.0.0.0', port= 8080 , debug = True)
