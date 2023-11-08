# modules/sensors.py

from .api_utils import get_sensor_data
from .vpd_tool import calculate_vpd

def fetch_sensor_data_and_vpd():
    """
    Fetches the latest sensor data and calculates the VPD.
    """
    try:
        sensor_data = get_sensor_data()
        if sensor_data:
            temperature = sensor_data.get('temperature')
            humidity = sensor_data.get('humidity')
            if temperature is not None and humidity is not None:
                vpd = calculate_vpd(temperature, humidity)
                sensor_data['vpd'] = vpd
            return sensor_data
        else:
            return None
    except Exception as e:
        print(f"Error fetching sensor data and calculating VPD: {e}")
        return None
