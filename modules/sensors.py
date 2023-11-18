# modules/sensors.py

from datetime import datetime
import logging

# Custom module imports
from .api_utils import generate_access_token, get_sensor_data
from .vpd_tool import calculate_vpd
from .db import Database  # Importing Database to manage API tokens

# Setup logging
logger = logging.getLogger(__name__)

def fetch_sensor_data():
    """
    Fetches the latest sensor data and calculates the VPD.
    """
    try:
        with Database() as db:
            token_data = db.get_api_token()
            if not token_data:
                logger.error("No token data available from the database.")
                return None

            token, expiry_time = token_data.get('token'), token_data.get('expiry_time')

            # Generate a new token if the current one is invalid or expired
            if not token or datetime.now() >= expiry_time:
                token, expiry_time = generate_access_token()
                if not token:
                    logger.error("Failed to generate a new access token.")
                    return None
                db.save_api_token(token, expiry_time)

        # Fetch sensor data using the valid token
        sensor_data = get_sensor_data(token)
        if not sensor_data:
            logger.error("Failed to fetch sensor data.")
            return None

        temperature = sensor_data.get('temperature')
        humidity = sensor_data.get('humidity')
        if temperature is not None and humidity is not None:
            vpd = calculate_vpd(temperature, humidity)
            sensor_data['vpd'] = vpd

            # Record the data in the database
            current_timestamp = datetime.now()
            with Database() as db:
                db.save_sensor_data(current_timestamp, temperature, humidity, vpd)
        else:
            logger.warning("Temperature or humidity data is missing.")
        return sensor_data
    except Exception as e:
        logger.exception(f"Error fetching sensor data and calculating VPD: {e}")
        return None
