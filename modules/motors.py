import RPi.GPIO as GPIO

# Motor GPIO Pins - replace with your actual pin numbers
MOTOR_PINS = {
    'motor_1': {'up': 17, 'down': 27},
    'motor_2': {'up': 22, 'down': 10},
    'motor_3': {'up': 9, 'down': 11},
    'motor_4': {'up': 5, 'down': 6}
}

def setup():
    GPIO.setmode(GPIO.BCM)
    for motor in MOTOR_PINS.values():
        GPIO.setup(motor['up'], GPIO.OUT)
        GPIO.setup(motor['down'], GPIO.OUT)

def roll(direction, motor_id):
    if motor_id not in MOTOR_PINS:
        print(f"Invalid motor ID: {motor_id}")
        return

    motor = MOTOR_PINS[motor_id]
    if direction == 'up':
        GPIO.output(motor['up'], GPIO.HIGH)
        GPIO.output(motor['down'], GPIO.LOW)
    elif direction == 'down':
        GPIO.output(motor['up'], GPIO.LOW)
        GPIO.output(motor['down'], GPIO.HIGH)
    else:
        print(f"Invalid direction: {direction}")

    print(f"Motor {motor_id} is rolling {direction}...")

def stop(motor_id):
    if motor_id not in MOTOR_PINS:
        print(f"Invalid motor ID: {motor_id}")
        return

    motor = MOTOR_PINS[motor_id]
    GPIO.output(motor['up'], GPIO.LOW)
    GPIO.output(motor['down'], GPIO.LOW)
    print(f"Motor {motor_id} has been stopped...")

# Ensure to call setup() at the appropriate place the application.

