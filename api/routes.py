from flask import Flask, jsonify, request
from modules.motors import MotorController

app = Flask(__name__)
motor_controller = MotorController()

@app.route('/api/motors/status', methods=['GET'])
def get_motor_status():
    status = motor_controller.get_status()
    return jsonify(status)

@app.route('/api/motors/control', methods=['POST'])
def control_motor():
    data = request.json
    result = motor_controller.set_status(data['motor_id'], data['state'])
    return jsonify(result)

# Add more routes as needed for other functionalities
