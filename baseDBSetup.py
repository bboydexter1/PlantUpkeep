#!/usr/bin/env python
from datetime import datetime, time
import models as Models

brightness1 = Models.Brightness(name = "low" , brightness = 250)
brightness2 = Models.Brightness(name = "medium" , brightness = 450)
brightness3 = Models.Brightness(name = "high" , brightness = 650)

humidity1 = Models.Humidity(name = "low" , soilHumidity = 200)
humidity2 = Models.Humidity(name = "medium" , soilHumidity = 500)
humidity3 = Models.Humidity(name = "high" , soilHumidity = 1000)

plantPreset = Models.PlantPreset(name = "example plant preset for Basil", lampFrom = time(hour=8, minute = 0) , lampTo = time(hour=19, minute = 0), wateringDays = 3 , brightnessID = 3,  humidityID = 2)

currentplant = Models.CurrentPlant(plantPreset = 1)

Models.db.session.add(brightness1)
Models.db.session.add(brightness2)
Models.db.session.add(brightness3)

Models.db.session.add(humidity1)
Models.db.session.add(humidity2)
Models.db.session.add(humidity3)

Models.db.session.add(plantPreset)

Models.db.session.add(currentplant)

Models.db.session.commit()