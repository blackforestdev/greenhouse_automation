import os
from dotenv import load_dotenv

# Load the environment variables from the .env file
load_dotenv()

# Flask app settings
SECRET_KEY = os.environ.get('FLASK_SECRET_KEY', 'default_secret_key_for_local_development')
DEBUG = bool(os.environ.get('FLASK_DEBUG', True))

DB_CONFIG = {
    'host': os.environ.get('DB_HOST', 'localhost'),
    'user': os.environ.get('DB_USER_NAME', 'greenhouse_automation'),
    'password': os.environ.get('DB_PASSWORD', 'default_password'),
    'database': os.environ.get('DB_NAME', 'greenhouse_automation')
}

# Motor settings
MOTOR_PIN_CONFIG = {
    'motor_1': {
        'forward_pin': 21,
        'backward_pin': 20
    },
    'motor_2': {
        'forward_pin': 23,
        'backward_pin': 22
    }
}
MOTOR_RUN_TIME = int(os.environ.get('MOTOR_RUN_TIME', 10))  # time in seconds

# Sensor settings
SENSOR_PIN_CONFIG = {
    'temp_sensor': 4
}
SENSOR_READ_INTERVAL = int(os.environ.get('SENSOR_READ_INTERVAL', 60))  # time in seconds

# Other settings
TIME_ZONE = os.environ.get('TIME_ZONE', 'America/Los_Angeles')
LOG_SETTINGS = {
    'log_file': os.environ.get('LOG_FILE', 'greenhouse_automation.log'),
    'log_level': os.environ.get('LOG_LEVEL', 'DEBUG')
}
