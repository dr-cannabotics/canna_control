from flask import Flask, request, jsonify, render_template

app = Flask(__name__)

# Relay states (True = ON, False = OFF)
relay_states = {'relay_0': False, 'relay_1': False, 'relay_2': False, 'relay_3': False}

# Sensor data
sensor_data = {
    'temperature': None,
    'humidity': None,
    'pressure': None,
    'soilMoisture': None,
    'phValue': None,
    'lightIntensity': None,
    'co2': None,
    'waterLevel': None,
    'nutrientConcentration': None,
    'leafMoisture': None,
    'rootTemperature': None,
    'daylightHours': None,
    'oxygenLevel': None,
    'airSpeed': None,
    'ecValue': None,
    'growthRate': None,
    'airQuality': None,
    'leafTemperature': None,
    'waterConsumption': None,
    'airChangeRate': None,
    'uvLightIntensity': None
}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/toggle/<relay_id>', methods=['POST'])
def toggle_relay(relay_id):
    global relay_states
    if relay_id in relay_states:
        relay_states[relay_id] = not relay_states[relay_id]
        state_str = "ON" if relay_states[relay_id] else "OFF"
        print(f"{relay_id} state toggled to: {state_str}")
        return jsonify({'state': state_str, 'status': 'success'}), 200
    return jsonify({'status': 'error', 'message': 'Invalid relay ID'}), 400

@app.route('/status')
def status():
    state_dict = {key: "ON" if value else "OFF" for key, value in relay_states.items()}
    return jsonify(state_dict), 200

@app.route('/sensor', methods=['POST'])
def update_sensor_data():
    global sensor_data
    data = request.get_json()
    for key in sensor_data.keys():
        if key in data:
            sensor_data[key] = data[key]
    return jsonify(sensor_data), 200

@app.route('/sensor')
def get_sensor_data():
    return jsonify(sensor_data), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=420)
