import os
import requests

channel_id = os.getenv('UBI_CHANNEL_ID')
api_key = os.getenv('UBI_API_KEY')

def fetch_sensor_data(api_key, channel_id):
    """
    Fetches the latest sensor data (temperature and humidity) from UbiBot.
    """
    url = f'https://webapi.ubibot.com/channels/{channel_id}/feeds.json?api_key={api_key}'
    response = requests.get(url)
    
    if response.status_code == 200:
        data = response.json()
        latest_data = data['feeds'][0] if data['feeds'] else None
        if latest_data:
            return {
                'temperature': latest_data.get('Temperature'),
                'humidity': latest_data.get('Humidity')
            }
    else:
        raise Exception(f"Failed to fetch data: {response.status_code}")

def calculate_vpd(temperature, humidity):
    """
    Calculates Vapor Pressure Deficit (VPD) from temperature and humidity.
    Implement the VPD formula here.
    """
    # VPD calculation logic
    return vpd

def get_sensor_data_and_vpd(api_key, channel_id):
    """
    Gets sensor data and calculates VPD.
    """
    try:
        sensor_data = fetch_sensor_data(api_key, channel_id)
        vpd = calculate_vpd(sensor_data['temperature'], sensor_data['humidity'])
        return {**sensor_data, 'vpd': vpd}
    except Exception as e:
        print(f"Error: {e}")
        return None
