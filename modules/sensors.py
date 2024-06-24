from datetime import datetime, timedelta
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
        token, expiry_time = None, None
        with Database() as db:
            token_data = db.get_api_token()
            if token_data:
                token, expiry_time = token_data.get('token'), token_data.get('expiry_time')

        if not token or datetime.now() >= expiry_time:
            logger.info("Generating a new token as the current one is invalid or expired.")
            token, expiry_time = generate_access_token()
            if not token:
                logger.error("Failed to generate a new access token.")
                return None
            with Database() as db:
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
