#!/bin/bash

# Array of GPIO pins
declare -a gpio_pins=("17" "27" "22" "10" "9" "11" "5" "6")

# Setup each GPIO pin
for pin in "${gpio_pins[@]}"; do
    echo "Setting up GPIO pin $pin on chip gpiochip1"
    if gpioset gpiochip1 $pin=0; then
        echo "Successfully set GPIO pin $pin on chip gpiochip1 to output active_low"
    else
        echo "Failed to set GPIO pin $pin on chip gpiochip1"
    fi
done
