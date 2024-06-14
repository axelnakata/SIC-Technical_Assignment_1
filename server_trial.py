from flask import Flask, request, jsonify, render_template
from datetime import datetime

app = Flask(__name__)

temperature_data = None
humidity_data = None
last_updated = None

@app.route('/')
def home():
    return "Data Receiver Server - Axel Nino Nakata - Technical Assignment 1"

@app.route('/data', methods=['POST'])
def receive_data():
    global temperature_data, humidity_data, last_updated

    data = request.get_json()
    if not data:
        return jsonify({'status': 'error', 'message': 'No JSON data received'}), 400

    temperature = data.get('temperature')
    humidity = data.get('humidity')

    if temperature is None or humidity is None:
        return jsonify({'status': 'error', 'message': 'Missing temperature or humidity data'}), 400
    
    try:
        temperature = float(temperature)
        humidity = float(humidity)
    except ValueError:
        return jsonify({'status': 'error', 'message': 'Invalid data format'}), 400
    
    # Update global variables
    temperature_data = temperature
    humidity_data = humidity
    last_updated = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    print(f"Received temperature: {temperature} C, humidity: {humidity} %")
    
    return jsonify({'status': 'success', 'message': 'Data received successfully'}), 200

@app.route('/dashboard')
def dashboard():
    global temperature_data, humidity_data, last_updated
    return render_template('dashboard.html', temperature=temperature_data or "N/A", humidity=humidity_data or "N/A", last_updated=last_updated or "N/A")

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)