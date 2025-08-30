from flask import Flask, jsonify, request
from flask_socketio import SocketIO, emit
from flask_cors import CORS
import os
from dotenv import load_dotenv
from twilio.rest import Client
import threading
import time
import random
from utils.data_simulator import DataSimulator

# Load environment variables
load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'your-secret-key-here')
CORS(app)
socketio = SocketIO(app, cors_allowed_origins="*")

# Twilio configuration
TWILIO_ACCOUNT_SID = os.getenv('TWILIO_ACCOUNT_SID')
TWILIO_AUTH_TOKEN = os.getenv('TWILIO_AUTH_TOKEN')
TWILIO_PHONE_NUMBER = os.getenv('TWILIO_PHONE_NUMBER')
ALERT_PHONE_NUMBER = os.getenv('ALERT_PHONE_NUMBER')

# Initialize Twilio client
twilio_client = None
if all([TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN, TWILIO_PHONE_NUMBER]):
    twilio_client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)

# Initialize data simulator
data_simulator = DataSimulator()

# Global variables to track alert state
last_alert_time = 0
alert_cooldown = 300  # 5 minutes cooldown between alerts

def send_sms_alert(message):
    """Send SMS alert via Twilio"""
    global last_alert_time
    
    if not twilio_client or not ALERT_PHONE_NUMBER:
        print("Twilio not configured or alert phone number missing")
        return
    
    current_time = time.time()
    if current_time - last_alert_time < alert_cooldown:
        print("Alert cooldown active, skipping SMS")
        return
    
    try:
        message = twilio_client.messages.create(
            body=f"🚨 TIDEGUARD ALERT: {message}",
            from_=TWILIO_PHONE_NUMBER,
            to=ALERT_PHONE_NUMBER
        )
        print(f"SMS alert sent: {message.sid}")
        last_alert_time = current_time
    except Exception as e:
        print(f"Failed to send SMS alert: {e}")

def check_thresholds(data):
    """Check if weather/tide data exceeds thresholds"""
    wind_speed = data.get('wind_speed', 0)
    wave_height = data.get('wave_height', 0)
    
    # Thresholds: wind_speed > 80 km/h OR wave_height > 4m
    if wind_speed > 80 or wave_height > 4:
        alert_message = f"Wind: {wind_speed} km/h, Waves: {wave_height}m"
        send_sms_alert(alert_message)
        return True
    return False

def simulate_and_broadcast():
    """Simulate data and broadcast to connected clients"""
    while True:
        try:
            # Generate simulated data
            data = data_simulator.generate_data()
            
            # Check thresholds and send alerts
            threshold_breached = check_thresholds(data)
            data['alert_active'] = threshold_breached
            
            # Broadcast to all connected clients
            socketio.emit('weather_data', data)
            
            print(f"Broadcasted data: {data}")
            
            # Wait 5 seconds before next simulation
            time.sleep(5)
            
        except Exception as e:
            print(f"Error in simulation loop: {e}")
            time.sleep(5)

@app.route('/health')
def health_check():
    """Health check endpoint"""
    return jsonify({"status": "OK", "message": "TideGuard Backend is running"})

@socketio.on('connect')
def handle_connect():
    """Handle client connection"""
    print(f"Client connected: {request.sid}")
    emit('connected', {'data': 'Connected to TideGuard Backend'})

@socketio.on('disconnect')
def handle_disconnect():
    """Handle client disconnection"""
    print(f"Client disconnected: {request.sid}")

@socketio.on('request_data')
def handle_data_request():
    """Handle client data request"""
    data = data_simulator.generate_data()
    threshold_breached = check_thresholds(data)
    data['alert_active'] = threshold_breached
    emit('weather_data', data)

if __name__ == '__main__':
    # Start data simulation in a separate thread
    simulation_thread = threading.Thread(target=simulate_and_broadcast, daemon=True)
    simulation_thread.start()
    
    print("Starting TideGuard Backend...")
    print("Data simulation started")
    print("WebSocket server ready")
    
    # Run the Flask app
    socketio.run(app, host='0.0.0.0', port=5000, debug=True)
