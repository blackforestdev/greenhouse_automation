import lgpio

# Define the GPIO pins you want to initialize
pins = [79, 80, 81, 82, 83, 84, 85, 86]

def initialize_pins():
    h = lgpio.gpiochip_open(0)  # Open GPIO chip 0
    for pin in pins:
        lgpio.gpio_claim_output(h, pin, 0)  # Set the pin to output and low
    lgpio.gpiochip_close(h)  # Close the GPIO chip

if __name__ == "__main__":
    initialize_pins()
    print("GPIO pins initialized to low.")
