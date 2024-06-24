import os
from periphery import GPIO

# Mapping for the headers based on the CSV data
gpio_mapping = {
    17: {'chip': 0, 'line': 5},   # Example mapping, replace with actual mappings from the CSV
    27: {'chip': 0, 'line': 4},
    22: {'chip': 1, 'line': 22},
    10: {'chip': 1, 'line': 10},
    9: {'chip': 1, 'line': 9},
    11: {'chip': 1, 'line': 11},
    5: {'chip': 1, 'line': 5},
    6: {'chip': 1, 'line': 6},
}

def set_gpio_value(chip, line, value):
    try:
        gpio = GPIO(chip, line, "out")
        gpio.write(value)
        result = gpio.read()
        gpio.close()
        return result
    except Exception as e:
        return f"An error occurred: {e}"

for pin, mapping in gpio_mapping.items():
    chip = f"/dev/gpiochip{mapping['chip']}"
    line = mapping['line']
    print(f"Setting GPIO {pin} to 0 using periphery")
    result = set_gpio_value(chip, line, False)
    print(f"GPIO {pin} value is now {result}")

    print(f"Setting GPIO {pin} to 1 using periphery")
    result = set_gpio_value(chip, line, True)
    print(f"GPIO {pin} value is now {result}")
