import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
from datetime import datetime
import time




cred = credentials.Certificate('/home/greg/Desktop/cozy-smart-home-firebase-adminsdk-s2qtm-c093886e1d.json')


firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://cozy-smart-home-default-rtdb.europe-west1.firebasedatabase.app/'
})




#save temperature  pressure  humidity readings
def save_room_temp_humi_pres(db_reference, temperature, pressure, humidity):
    now = datetime.now()
    ref = db.reference(db_reference)
    ref.push({
        'timestamp': now.strftime("%m/%d/%Y, %H:%M:%S"),
        'temperature': temperature,
        'pressure': pressure,
        'humidity': humidity
    })

#https://morioh.com/p/a593f973aff0 """

#save air pollution readings
def save_particulate_air_pollution_rds(db_reference, PM1_0, PM2_5, PM10):
    now = datetime.now()
    ref = db.reference(db_reference)
    ref.push({
        'timestamp': now.strftime("%m/%d/%Y, %H:%M:%S"),
        'PM1_ugm3_(ultrafine particles)': PM1_0,
        'PM2_ugm3_(combustion particles, organic compounds, metals)': PM2_5,
        'PM10_ugm3_(dust, pollen, mould spores)': PM10
    })


#initialise database
if __name__ == "__main__":
    ref = db.reference('room_temperature_humidity_pressure')
    ref.set({
        'room_temperature_humidity_pressure': 
            {
                'temperature': 9999,
                'pressure': 9999,
                'humidity': 9999
            }
        })
    
    ref = db.reference('particulate_air_pollution_readings')
    ref.set({
        'particulate_air_pollution_readings': 
            {
                'PM1_ugm3_(ultrafine particles)': 9999,
                'PM2_ugm3_(combustion particles, organic compounds, metals)': 9999,
                'PM10_ugm3_(dust, pollen, mould spores)': 9999
            }
        })
    