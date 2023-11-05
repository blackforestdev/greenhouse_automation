from flask import Flask, render_template, jsonify, request
from flask_socketio import SocketIO
from datetime import datetime
import logging
import traceback

# Import custom modules
from modules.db import Database
from modules import motors as motor_control
from modules import sensors as sensors
from app_logging.logging_module import setup_logging
from app_logging.error_handlers import handle_404

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

# Additional routes for motor actions
@app.route('/motor_action/roll_up', methods=['POST'])
def motor_roll_up():
    try:
        # Logic for rolling up
        motor_control.roll_up()  # You need to define this in your motor_control module
        return jsonify({'status': 'success', 'action': 'roll_up'}), 200
    except Exception as e:
        logger.error(f"Error in roll_up action: {e}")
        return jsonify({'status': 'error', 'message': str(e)}), 500

@app.route('/motor_action/roll_down', methods=['POST'])
def motor_roll_down():
    try:
        # Logic for rolling down
        motor_control.roll_down()  # Define this in your motor_control module
        return jsonify({'status': 'success', 'action': 'roll_down'}), 200
    except Exception as e:
        logger.error(f"Error in roll_down action: {e}")
        return jsonify({'status': 'error', 'message': str(e)}), 500

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5000)
