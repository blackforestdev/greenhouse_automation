# modules/sensors.py

from datetime import datetime

# Custom module imports
from .api_utils import generate_access_token, get_sensor_data
from .vpd_tool import calculate_vpd
from .db import Database  # Importing Database to manage API tokens

def fetch_sensor_data():
    """
    Fetches the latest sensor data and calculates the VPD.
    """
    try:
        with Database() as db:
            token_data = db.get_api_token()
            token, expiry_time = token_data['token'], token_data['expiry_time']

            # Generate a new token if the current one is invalid or expired
            if not token or datetime.now() >= expiry_time:
                token, expiry_time = generate_access_token()
                db.save_api_token(token, expiry_time)

        # Fetch sensor data using the valid token
        sensor_data = get_sensor_data(token)
        if sensor_data:
            temperature = sensor_data.get('temperature')
            humidity = sensor_data.get('humidity')
            if temperature is not None and humidity is not None:
                vpd = calculate_vpd(temperature, humidity)
                sensor_data['vpd'] = vpd

                # Record the data in the database
                current_timestamp = datetime.now()
                with Database() as db:
                    db.execute("INSERT INTO sensor_data (timestamp, temperature, humidity, vpd) VALUES (%s, %s, %s, %s)",
                            (current_timestamp, temperature, humidity, vpd))
            return sensor_data
        else:
            return None    except Exception as e:
        print(f"Error fetching sensor data and calculating VPD: {e}")
        return None
        