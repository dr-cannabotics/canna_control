import network
import urequests
import ujson
import dht
from machine import Pin, PWM
import time
import random

SSID = 'WifiName'
PASSWORD = 'WifiPasswoed'

FLASK_URL_STATUS = 'http://212.000.00.00:420/status'
FLASK_URL_SENSOR = 'http://212.000.00.00:420/sensor'

INFLUXDB_URL = 'http://http://212.000.00.00:8086/api/v2/write?org=sensorboard&bucket=cannabucket'
INFLUXDB_MEASUREMENT = 'sensorboard'
INFLUXDB_TOKEN = 'INFLUXTOKEN'

RELAY_PINS = [Pin(i, Pin.OUT) for i in (1, 2, 3, 4)]

dht_sensor = dht.DHT22(Pin(15))

piezo = PWM(Pin(0))

def play_tone(frequency, duration):
    if frequency <= 0:
        print(f"[ERROR] Invalid frequency: {frequency}. Must be greater than 0.")
        return
    
    try:
        piezo.freq(frequency)
        piezo.duty_u16(32768)
        time.sleep(duration)
        piezo.duty_u16(0)
        time.sleep(0.05)
    except ValueError as e:
        print(f"[ERROR] ValueError in play_tone with frequency {frequency}: {e}")

def play_melodic_tone():
    tones = [(523, 0.15), (659, 0.15), (784, 0.15), (1046, 0.15)]
    for frequency, duration in tones:
        play_tone(frequency, duration)

def connect_to_wifi():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(SSID, PASSWORD)
    
    print("Attempting to connect to WiFi...")
    timeout = time.time() + 30
    
    while not wlan.isconnected() and time.time() < timeout:
        print(f"Current connection status: {wlan.ifconfig()}")
        time.sleep(5)
        
    if wlan.isconnected():
        print(f"Connected to {SSID} with IP address {wlan.ifconfig()[0]}")
        play_melodic_tone()
    else:
        print("Failed to connect to WiFi within timeout period.")
    
    return wlan

def update_relay_status():
    try:
        response = urequests.get(FLASK_URL_STATUS)
        data = ujson.loads(response.text)
        for i in range(4):
            relay_state = data.get(f'relay_{i}', 'OFF') == 'ON'
            RELAY_PINS[i].value(relay_state)
        response.close()
    except Exception as e:
        print(f'[ERROR] Error updating relay status: {e}')

def read_soil_moisture():
    return round(50 + (20 * (2 * (random.random() - 0.5))), 2)

def gather_sensor_data():
    try:
        dht_sensor.measure()
        data = {
            'temperature': dht_sensor.temperature(),
            'humidity': dht_sensor.humidity(),
            'pressure': round(1013 + (10 * (2 * (random.random() - 0.5))), 2),
            'soilMoisture': read_soil_moisture(),
            'phValue': round(6 + (2 * (2 * (random.random() - 0.5))), 2),
            'lightIntensity': round(1000 + (500 * (2 * (random.random() - 0.5))), 2),
            'co2': round(400 + (100 * (2 * (random.random() - 0.5))), 2),
            'waterLevel': round(50 + (30 * (2 * (random.random() - 0.5))), 2),
            'nutrientConcentration': round(1000 + (500 * (2 * (random.random() - 0.5))), 2),
            'leafMoisture': round(40 + (30 * (2 * (random.random() - 0.5))), 2),
            'rootTemperature': round(20 + (10 * (2 * (random.random() - 0.5))), 2),
            'daylightHours': round(12 + (2 * (2 * (random.random() - 0.5))), 2),
            'oxygenLevel': round(21 + (1 * (2 * (random.random() - 0.5))), 2),
            'airSpeed': round(5 + (2 * (2 * (random.random() - 0.5))), 2),
            'ecValue': round(1.5 + (0.5 * (2 * (random.random() - 0.5))), 2),
            'growthRate': round(0.5 + (0.2 * (2 * (random.random() - 0.5))), 2),
            'airQuality': round(50 + (10 * (2 * (random.random() - 0.5))), 2),
            'leafTemperature': round(22 + (5 * (2 * (random.random() - 0.5))), 2),
            'waterConsumption': round(2 + (1 * (2 * (random.random() - 0.5))), 2),
            'airChangeRate': round(1 + (0.5 * (2 * (random.random() - 0.5))), 2),
            'uvLightIntensity': round(10 + (5 * (2 * (random.random() - 0.5))), 2)
        }
        return data
    except Exception as e:
        print(f'[ERROR] Error gathering sensor data: {e}')
        return {}

def send_data_to_flask(data):
    try:
        payload = ujson.dumps(data)
        response = urequests.post(FLASK_URL_SENSOR, data=payload, headers={'Content-Type': 'application/json'})
        print('Sensor data sent to Flask server:', response.text)
        response.close()
    except Exception as e:
        print(f'[ERROR] Error sending data to Flask server: {e}')

def send_data_to_influxdb(data):
    try:
        influx_payload = f"{INFLUXDB_MEASUREMENT} "
        influx_payload += ','.join([f"{key}={value}" for key, value in data.items() if value is not None])
        headers = {
            'Authorization': f'Token {INFLUXDB_TOKEN}',
            'Content-Type': 'text/plain'
        }
        response = urequests.post(INFLUXDB_URL, data=influx_payload, headers=headers)
        print("Data sent to InfluxDB successfully! Status code:", response.status_code)
        response.close()
    except Exception as e:
        print(f'[ERROR] Error sending data to InfluxDB: {e}')

def main():
    play_melodic_tone()
    connect_to_wifi()
    
    last_sensor_update = time.time()
    sensor_update_interval = 1
    
    while True:
        update_relay_status()
        
        current_time = time.time()
        if current_time - last_sensor_update >= sensor_update_interval:
            sensor_data = gather_sensor_data()
            if sensor_data:
                send_data_to_flask(sensor_data)
                send_data_to_influxdb(sensor_data)
            last_sensor_update = current_time
        
        time.sleep(1)

if __name__ == "__main__":
    main()

