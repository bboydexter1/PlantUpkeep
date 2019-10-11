#!/usr/bin/env python
from flask import Flask, render_template, redirect, url_for, request
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime , time
import time

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'

db = SQLAlchemy(app)

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
    wateringDays = db.Column(db.Integer, nullable=True)
    brightnessID = db.Column(db.Integer, db.ForeignKey('brightness.id'), nullable=True)
    humidityID = db.Column(db.Integer, db.ForeignKey('humidity.id'), nullable=True)
    
        
class Brightness(db.Model):
    __tablename__ = 'brightness'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), unique=True, nullable=False)
    brightness = db.Column(db.Integer, nullable=False)
    
class Humidity(db.Model):
    __tablename__ = 'humidity'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), unique=True, nullable=False)
    soilHumidity = db.Column(db.Integer, nullable=False)
