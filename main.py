from flask import Flask, render_template, jsonify, request
from flask_socketio import SocketIO
from datetime import datetime
import logging
import os
import traceback
from dotenv import load_dotenv

# Import custom modules
from modules.db import Database
from modules import motors as motor_control
from modules.sensors import fetch_sensor_data
from app_logging.logging_module import setup_logging
from app_logging.error_handlers import handle_404
from modules.api_utils import refresh_api_token

# Load the .env file
load_dotenv()

# Set up logging configuration
setup_logging()

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'
socketio = SocketIO(app)

logger = logging.getLogger('my_application.main')

app.register_error_handler(404, handle_404)

@app.before_request
def before_request():
    logger.info("Request received at %s", datetime.now())

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/set_time', methods=['POST'])
def set_time():
    logger.info('Headers: %s', request.headers)
    logger.info('Body: %s', request.get_data(as_text=True))

    roll_up_time = request.form.get('roll_up_time')
    roll_down_time = request.form.get('roll_down_time')

    logger.info('Roll-up time: %s', roll_up_time)
    logger.info('Roll-down time: %s', roll_down_time)

    try:
        with Database() as db:
            db.save_time_settings(roll_up_time, roll_down_time)
        socketio.emit('update_time_settings', {'roll_up_time': roll_up_time, 'roll_down_time': roll_down_time})
        return jsonify({'status': 'success'}), 200
    except Exception as e:
        logger.error("Failed to set times: %s", e)
        return jsonify({'status': 'error', 'message': str(e)}), 500

@app.route('/get_motor_statuses')
def get_motor_statuses():
    try:
        with Database() as db:
            motor_statuses = db.get_motor_statuses()
            return jsonify(motor_statuses), 200
    except Exception as e:
        logger.error(f"Failed to fetch motor statuses: {e}")
        return jsonify({'status': 'error', 'message': str(e)}), 500

@app.route('/motor_status/<motor_id>', methods=['POST'])
def update_motor_status(motor_id):
    try:
        data = request.get_json()
        status = data['status']

        with Database() as db:
            db.update_motor_status(motor_id, status)
        return jsonify({'status': 'success'}), 200
    except Exception as e:
        logger.error(f"Failed to update motor status for {motor_id}: {e}")
        return jsonify({'status': 'error', 'message': str(e)}), 500

@app.route('/get_sensor_data')
def sensor_data():
    try:
        with Database() as db:
            token_data = db.get_api_token()
            token, expiry_time = token_data['token'], token_data['expiry_time']

        if not token or datetime.now() >= expiry_time:
            token, expiry_time = refresh_api_token()  # Implement this function
            with Database() as db:
                db.save_api_token(token, expiry_time)

        data = fetch_sensor_data(token, os.getenv('UBI_CHANNEL_ID'))
        return jsonify(data)
    except Exception as e:
        app.logger.error("Failed to fetch sensor data: %s", e)
        return jsonify({'status': 'error', 'message': str(e)}), 500

@socketio.on('request_sensor_data')
def handle_request_sensor_data():
    try:
        with Database() as db:
            token_data = db.get_api_token()
            token, expiry_time = token_data['token'], token_data['expiry_time']

        if not token or datetime.now() >= expiry_time:
            token, expiry_time = refresh_api_token()
            with Database() as db:
                db.save_api_token(token, expiry_time)

        data = fetch_sensor_data(token, os.getenv('UBI_CHANNEL_ID'))
        socketio.emit('sensor_data_response', data)
    except Exception as e:
        app.logger.error("WebSocket: Failed to fetch sensor data: %s", e)
        socketio.emit('sensor_data_error', {'status': 'error', 'message': str(e)})

@socketio.on('connect')
def test_connect():
    logger.info('Client connected at %s', datetime.now())

@socketio.on('disconnect')
def test_disconnect():
    logger.info('Client disconnected at %s', datetime.now())

@socketio.on('request_motor_status')
def handle_request_motor_status():
    try:
        with Database() as db:
            motor_statuses = db.get_motor_statuses()
        logger.info("Motor statuses fetched successfully")
        socketio.emit('motor_status_response', motor_statuses)
    except Exception as e:
        error_message = f"Failed to fetch motor statuses: {e}, traceback: {traceback.format_exc()}"
        logger.error(error_message)
        socketio.emit('motor_status_error', {'status': 'error', 'message': str(e)})

@socketio.on('trigger_motor_action')
def handle_motor_action(data):
    action = data.get('action')
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    try:
        motor_control.handle_action(action)
        logger.info(f"Motor action '{action}' triggered at {timestamp}")
        socketio.emit('motor_action_response', {'status': 'success', 'action': action, 'timestamp': timestamp})
    except Exception as e:
        logger.error(f"Error triggering motor action '{action}' at {timestamp}: {e}")
        socketio.emit('motor_action_error', {'status': 'error', 'action': action, 'message': str(e), 'timestamp': timestamp})

# Route for handling motor actions
@app.route('/motor_action/<action>', methods=['POST'])
def motor_action(action):
    try:
        data = request.get_json()
        motor_statuses = data.get('motor_statuses')

        # Check and perform the action for each motor based on its status
        for motor_id, is_active in motor_statuses.items():
            if is_active:
                motor_control.perform_action(action, motor_id)

        return jsonify({'status': 'success', 'action': action, 'message': f"{action} performed successfully on active motors"}), 200
    except Exception as e:
        logger.error(f"Error in motor action '{action}': {e}")
        return jsonify({'status': 'error', 'message': str(e)}), 500
      
if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5000)
