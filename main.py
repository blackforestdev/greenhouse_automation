from flask import Flask, render_template, jsonify, request
from flask_socketio import SocketIO
from datetime import datetime, timedelta
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
from modules.api_utils import generate_access_token, get_sensor_data

# Load the .env file
load_dotenv()
# for debugging the credentials 
print("DB Host:", os.environ.get('DB_HOST'))
print("DB User:", os.environ.get('DB_USER_NAME'))
print("DB Password:", os.environ.get('DB_PASSWORD'))
print("DB Name:", os.environ.get('DB_NAME'))

# Set up logging configuration
setup_logging()

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'
socketio = SocketIO(app)

logger = logging.getLogger('my_application.main')

app.register_error_handler(404, handle_404)

current_action = "Motors idle"

@app.before_request
def before_request():
    logger.info("Request received at %s", datetime.now())

def timedelta_to_time_string(timedelta_obj):
    total_seconds = int(timedelta_obj.total_seconds())
    hours = total_seconds // 3600
    minutes = (total_seconds % 3600) // 60
    seconds = total_seconds % 60
    return f"{hours:02d}:{minutes:02d}:{seconds:02d}"

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
            db.update_time_settings(roll_up_time, roll_down_time)
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

@app.route('/motor_status/<string:motor_switch_id>', methods=['POST'])
def update_motor_status(motor_switch_id):
    global current_action
    try:
        data = request.get_json()
        status = data['status']

        with Database() as db:
            db.update_motor_status(motor_switch_id, status)

        if status == "Active":
            current_action = f"All Motors rolling {motor_switch_id.split('-')[-1]}"  # Adjust this logic based on your motor ID naming
        elif status == "Deactivated":
            current_action = "All Motors stopped"
        else:
            current_action = "Motors idle"

        socketio.emit('motor_status_updated', {'motor_switch_id': motor_switch_id, 'status': status})
        return jsonify({'status': 'success'}), 200
    except Exception as e:
        logger.error(f"Failed to update motor status for {motor_switch_id}: {e}")
        return jsonify({'status': 'error', 'message': str(e)}), 500

@app.route('/get_motor_action')
def get_motor_action():
    return jsonify(action=current_action)

@app.route('/get_sensor_data')
def sensor_data():
    try:
        sensor_data = fetch_sensor_data()
        if sensor_data:
            return jsonify(sensor_data), 200
        else:
            return jsonify({'status': 'error', 'message': 'No sensor data available'}), 404
    except Exception as e:
        app.logger.error("Failed to fetch sensor data: %s", e)
        return jsonify({'status': 'error', 'message': str(e)}), 500

@app.route('/motor_action/<string:action>', methods=['POST'])
def motor_action(action):
    try:
        data = request.get_json()
        motor_id = data.get('motor_id', 'all')  # Default to 'all' if no motor_id is provided
        motor_control.perform_action(action, motor_id)
        return jsonify({'status': 'success', 'action': action, 'motorId': motor_id}), 200
    except Exception as e:
        logger.error(f"Error in {action}: {e}")
        return jsonify({'status': 'error', 'message': str(e)}), 500

@app.route('/manual_control', methods=['POST'])
def manual_control():
    global current_action
    # Get the control action from the request
    action = request.form['action']
    motor_id = request.form['motor_id']
    
    # Call the motor control function with the action
    result = motor_control.perform_action(action, motor_id)
    
    # Update the status
    current_action = f"Motor {motor_id} {action.replace('_', ' ')}"
    return jsonify({'status': 'success'})

@socketio.on('request_sensor_data')
def handle_request_sensor_data():
    try:
        sensor_data = fetch_sensor_data()
        if (sensor_data):
            socketio.emit('sensor_data_response', sensor_data)
        else:
            socketio.emit('sensor_data_error', {'status': 'error', 'message': 'No sensor data available'})
    except Exception as e:
        app.logger.error("WebSocket: Failed to fetch sensor data: %s", e)
        socketio.emit('sensor_data_error', {'status': 'error', 'message': str(e)})

@socketio.on('request_current_times')
def handle_request_current_times():
    try:
        with Database() as db:
            time_settings = db.get_latest_time_settings()
            if (time_settings):
                roll_up_time = timedelta_to_time_string(time_settings['roll_up_time'])
                roll_down_time = timedelta_to_time_string(time_settings['roll_down_time'])

                socketio.emit('current_times', {'roll_up': roll_up_time, 'roll_down': roll_down_time})
            else:
                socketio.emit('current_times', {'roll_up': "Not set", 'roll_down': "Not set"})
    except Exception as e:
        logger.error("Failed to fetch current times: %s", e)

@socketio.on('trigger_motor_action')
def handle_motor_action(data):
    global current_action
    action = data.get('action')
    motor_id = data.get('motor_id')
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    try:
        motor_control.perform_action(action, motor_id)
        logger.info(f"Motor action '{action}' triggered for motor_id={motor_id} at {timestamp}")

        with Database() as db:
            new_status = 'Active' if action == 'turn_on' else 'Inactive'
            db.update_motor_status(motor_id, new_status)
        
        if action == 'turn_on':
            current_action = f"All Motors rolling {motor_id.split('-')[-1]}"  # Adjust this logic based on your motor ID naming
        elif action == 'turn_off':
            current_action = "All Motors stopped"
        else:
            current_action = "Motors idle"

        socketio.emit('motor_action_response', {
            'status': 'success', 
            'action': action, 
            'motor_id': motor_id, 
            'timestamp': timestamp
        })
    except Exception as e:
        logger.error(f"Error triggering motor action '{action}' for motor_id={motor_id} at {timestamp}: {e}")
        socketio.emit('motor_action_error', {
            'status': 'error', 
            'action': action, 
            'motor_id': motor_id, 
            'message': str(e), 
            'timestamp': timestamp
        })

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5000, debug=True)
