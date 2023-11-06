from periphery import GPIO

# Motor GPIO Pins - replace with your actual pin numbers
MOTOR_PINS = {
    'motor_1': {'up': 17, 'down': 27},
    'motor_2': {'up': 22, 'down': 10},
    'motor_3': {'up': 9, 'down': 11},
    'motor_4': {'up': 5, 'down': 6}
}

def roll(direction, motor_id):
    if motor_id not in MOTOR_PINS:
        print(f"Invalid motor ID: {motor_id}")
        return

    motor = MOTOR_PINS[motor_id]
    with GPIO(motor['up'], "out") as gpio_up, GPIO(motor['down'], "out") as gpio_down:
        if direction == 'up':
            gpio_up.write(True)
            gpio_down.write(False)
        elif direction == 'down':
            gpio_up.write(False)
            gpio_down.write(True)
        else:
            print(f"Invalid direction: {direction}")

        print(f"Motor {motor_id} is rolling {direction}...")

def stop(motor_id):
    if motor_id not in MOTOR_PINS:
        print(f"Invalid motor ID: {motor_id}")
        return

    motor = MOTOR_PINS[motor_id]
    with GPIO(motor['up'], "out") as gpio_up, GPIO(motor['down'], "out") as gpio_down:
        gpio_up.write(False)
        gpio_down.write(False)

        print(f"Motor {motor_id} has been stopped...")
