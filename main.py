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

class PlantPreset(db.Model):
    __tablename__ = 'plantPreset'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), unique=True, nullable=False)
    lampFrom = db.Column(db.Time, nullable=True)
    lampTo = db.Column(db.Time, nullable=True)
    brightnessID = db.Column(db.Integer, db.ForeignKey('brightness.id'), nullable=True)
    humidityID = db.Column(db.Integer, db.ForeignKey('humidity.id'), nullable=True)
    
    def __repr__(self):
        return "PlantPreset('{self.name}')"
        
class Brightness(db.Model):
    __tablename__ = 'brightness'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), unique=True, nullable=False)
    brightness = db.Column(db.Integer, nullable=False)
    preset = db.relationship("PlantPreset")
    
    def __repr__(self):
        return "Brightness('{self.name}')"
    
class Humidity(db.Model):
    __tablename__ = 'humidity'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), unique=True, nullable=False)
    soilHumidity = db.Column(db.Integer, nullable=False)
    preset = db.relationship("PlantPreset")
    
    def __repr__(self):
        return "Humidity('{self.name}')"

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/lamp')
def lamp():
    GPIO.output(8, True)
    return render_template('lamp.html')

@app.route('/pump')
def pump():
    GPIO.output(8, False)
    return render_template('pump.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port= 8080 , debug = True)
