from flask import Flask, request, jsonify
# Import functionalities from your modules as required
from modules import db, motors, sensors
from modules.db import Database

# Create an instance of the Database class
db_instance = Database()
app = Flask(__name__)

# Initial states
motor_states = {
    'sidewall-left': True,
    'sidewall-right': True,
    'overhead-left': True,
    'overhead-right': True
}

@app.route('/motor_status/<motor_id>', methods=['POST'])
def set_motor_status(motor_id):
    status = request.json.get('status')
    motor_states[motor_id] = status == 'Active'
    return jsonify({'status': 'success'})

@app.route('/get_motor_statuses', methods=['GET'])
def get_motor_statuses():
    return jsonify(motor_states)

@app.route('/motor_action/<action>', methods=['POST'])
def trigger_motor(action):
    if action == "roll_up":
        motors.roll_up()
    elif action == "roll_down":
        motors.roll_down()
    else:
        return jsonify({'status': 'error', 'message': f'Unknown action: {action}'}), 400

    return jsonify({'status': 'success'})

@app.route('/get_current_times', methods=['GET'])
def get_current_times():
    with Database() as db:
        times = db.get_latest_time_settings()
    if times:
        roll_up_time, roll_down_time = times
        return jsonify({"roll_up": roll_up_time, "roll_down": roll_down_time})
    else:
        return jsonify({"error": "Failed to fetch times"}), 500

if __name__ == "__main__":
    app.run(debug=True)
