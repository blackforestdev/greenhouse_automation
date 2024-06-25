import logging
import lgpio
from modules.db import Database
from config import MOTOR_PIN_CONFIG, MOTOR_IDS

# Set up logging
logger = logging.getLogger(__name__)

# Initialize GPIO handle
chip = 1  # Assuming all pins are on gpiochip1
h = lgpio.gpiochip_open(chip)

def set_gpio_value(line, value):
    try:
        lgpio.gpio_claim_output(h, line, 0)  # Claim the line for output
        lgpio.gpio_write(h, line, value)
        logger.info(f"Successfully set GPIO line {line} to {value}")
    except Exception as e:
        logger.error(f"Failed to set GPIO line {line} to {value}: {e}")

def update_motor_status_in_db(motor_id, status):
    try:
        with Database() as db:
            db.update_motor_status(motor_id, status)
    except Exception as e:
        logger.error(f"Error updating motor status in database: {e}")

def perform_action_all(action):
    for motor_id in MOTOR_PIN_CONFIG.keys():
        perform_action(action, motor_id)

def perform_action(action, motor_id):
    if motor_id == 'all':
        perform_action_all(action)
    else:
        if action == 'roll_up':
            roll('up', motor_id)
        elif action == 'roll_down':
            roll('down', motor_id)
        elif action == 'stop':
            stop(motor_id)
        else:
            logger.error(f"Invalid action: {action}")

def roll(direction, motor_id):
    if motor_id not in MOTOR_PIN_CONFIG:
        logger.error(f"Invalid motor ID: {motor_id}")
        return

    motor = MOTOR_PIN_CONFIG[motor_id]
    operate_motor(motor, direction, motor_id)

def operate_motor(motor_pins, direction, motor_id):
    try:
        if direction == 'up':
            set_gpio_value(motor_pins['up'], 1)
            set_gpio_value(motor_pins['down'], 0)
            update_motor_status_in_db(motor_id, 'Active')
        elif direction == 'down':
            set_gpio_value(motor_pins['up'], 0)
            set_gpio_value(motor_pins['down'], 1)
            update_motor_status_in_db(motor_id, 'Active')
        elif direction == 'stop':
            set_gpio_value(motor_pins['up'], 0)
            set_gpio_value(motor_pins['down'], 0)
            update_motor_status_in_db(motor_id, 'Deactivated')
        else:
            logger.error(f"Invalid direction: {direction}")

        logger.info(f"Motor {motor_id} is rolling {direction}...")
    except Exception as e:
        logger.error(f"Error operating motor {motor_id} for direction {direction}: {e}")

def roll_up(motor_id):
    roll('up', motor_id)

def roll_down(motor_id):
    roll('down', motor_id)

def stop(motor_id):
    if motor_id not in MOTOR_PIN_CONFIG:
        logger.error(f"Invalid motor ID: {motor_id}")
        return

    motor = MOTOR_PIN_CONFIG[motor_id]
    operate_motor(motor, 'stop', motor_id)
