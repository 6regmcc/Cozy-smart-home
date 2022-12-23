

import time
from bme280 import BME280 #import sensor for temperature pressure humidity readings
from pms5003 import PMS5003, ReadTimeoutError #import sensor for air quality readings
import firebase_realtime_db as rt_db
import mqtt_publish_sub as mqtt

try:
    from smbus2 import SMBus
except ImportError:
    from smbus import SMBus

# initialise senserse
bus = SMBus(1)
bme280 = BME280(i2c_dev=bus)
pms5003 = PMS5003()
#first reading of BME280 is always incorrect 
temperature = bme280.get_temperature()
pressure = bme280.get_pressure()
humidity = bme280.get_humidity()

time.sleep(1) #sensors need time to fully initialise 

def get_room_temp_humi_pres(): 
    temperature = round(bme280.get_temperature(), 2)
    pressure = round(bme280.get_pressure(), 2)
    humidity = round(bme280.get_humidity(), 2)
    return temperature, pressure, humidity




def get_particulate_air_pollution_readings():
    readings_air = 0
    count = 0
    try:
        while count <= 10:   #take multiple reading for better accuracy as more air is pulled through sensor
            readings_air = pms5003.read()
            count += 1
    except ReadTimeoutError:
        print("ReadTimeoutError")
        get_particulate_air_pollution_readings()
    print(readings_air)
    PM1_0 = readings_air.data[0] #PM1.0 ug/m3 (ultrafine particles): 
    PM2_5 = readings_air.data[1] #PM2.5 ug/m3 (combustion particles, organic compounds, metals):
    PM10 = readings_air.data[2] #PM10 ug/m3  (dust, pollen, mould spores): 
    return PM1_0, PM2_5, PM10






#This fuction checks humidity levels and switches on the dehumidifier if levels go above 50
def switch_dehumidifier_on_off(humidity):
    if humidity > 50:
        mqtt.update_smart_plug_state("zigbee2mqtt/0xa4c138c138a2954d/set", "ON")
    else:
        mqtt.update_smart_plug_state("zigbee2mqtt/0xa4c138c138a2954d/set", "OFF")

# this fuction checks the 3 air quality readings and switches on air purifier if any of the levels are outside the normal range
def switch_air_purifier_on_off(PM1_0, PM2_5, PM10):
    if PM1_0 > 12:
        mqtt.update_smart_plug_state("zigbee2mqtt/0x00124b00246ca976/set", "ON")
    elif PM2_5 > 12:
        mqtt.update_smart_plug_state("zigbee2mqtt/0x00124b00246ca976/set", "ON")
    elif PM10 > 50:
        mqtt.update_smart_plug_state("zigbee2mqtt/0x00124b00246ca976/set", "ON")
    else:
        mqtt.update_smart_plug_state("zigbee2mqtt/0x00124b00246ca976/set", "OFF")

while True:
    temperature, pressure, humidity = get_room_temp_humi_pres()
    rt_db.save_room_temp_humi_pres('room_temperature_humidity_pressure', temperature, pressure, humidity)
    #humidity = 55
    switch_dehumidifier_on_off(humidity)
    

    PM1_0, PM2_5, PM10 = get_particulate_air_pollution_readings()
    rt_db.save_particulate_air_pollution_rds('particulate_air_pollution_readings',PM1_0, PM2_5, PM10 )
    #PM1_0 = 15
    #PM2_5 = 15
    #PM10 = 55
    switch_air_purifier_on_off(PM1_0, PM2_5, PM10)
    time.sleep(10)