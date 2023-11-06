from periphery import GPIO

# Motor GPIO Pins - replace with your actual pin numbers
MOTOR_PINS = {
    'motor_1': {'up': 17, 'down': 27},
    'motor_2': {'up': 22, 'down': 10},
    'motor_3': {'up': 9, 'down': 11},
    'motor_4': {'up': 5, 'down': 6}
}

def perform_action(action, motor_id):
    if action == 'roll_up':
        roll('up', motor_id)
    elif action == 'roll_down':
        roll('down', motor_id)
    elif action == 'stop':
        stop(motor_id)
    else:
        raise ValueError(f"Invalid action: {action}")

def roll(direction, motor_id):
    if motor_id not in MOTOR_PINS:
        print(f"Invalid motor ID: {motor_id}")
        return

    motor = MOTOR_PINS[motor_id]
    operate_motor(motor, direction)

def operate_motor(motor_pins, direction):
    with GPIO(motor_pins['up'], "out") as gpio_up, GPIO(motor_pins['down'], "out") as gpio_down:
        if direction == 'up':
            gpio_up.write(True)
            gpio_down.write(False)
        elif direction == 'down':
            gpio_up.write(False)
            gpio_down.write(True)
        else:
            print(f"Invalid direction: {direction}")

        print(f"Motor is rolling {direction}...")

def roll_up(motor_id):
    roll('up', motor_id)

def roll_down(motor_id):
    roll('down', motor_id)

def stop(motor_id):
    if motor_id not in MOTOR_PINS:
        print(f"Invalid motor ID: {motor_id}")
        return

    motor = MOTOR_PINS[motor_id]
    operate_motor(motor, 'stop')

def operate_motor(motor_pins, command):
    with GPIO(motor_pins['up'], "out") as gpio_up, GPIO(motor_pins['down'], "out") as gpio_down:
        if command == 'stop':
            gpio_up.write(False)
            gpio_down.write(False)
            print(f"Motor {motor_id} has been stopped...")
        else:
            print("Invalid command.")
