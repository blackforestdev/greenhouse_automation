import requests
import os

channel_id = os.getenv('UBI_CHANNEL_ID')
account_key = os.getenv('UBI_ACCOUNT_KEY')

def get_ubibot_data(account_key, channel_id):
    # Function logic here
    # ...

def fetch_sensor_data(account_key, channel_id):
    """
    Fetches the latest sensor data (temperature and humidity) from UbiBot.
    """
    url = f'https://api.ubibot.com/channels/{channel_id}/feeds.json?account_key={account_key}'
    response = requests.get(url)
    
    if response.status_code == 200:
        data = response.json()
        latest_data = data['feeds'][0] if data['feeds'] else None
        if latest_data:
            return {
                'temperature': latest_data.get('field1'),  # Replace with your actual field key for temperature
                'humidity': latest_data.get('field2')  # Replace with your actual field key for humidity
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

def get_sensor_data_and_vpd(account_key, channel_id):
    """
    Gets sensor data and calculates VPD.
    """
    try:
        sensor_data = fetch_sensor_data(account_key, channel_id)
        vpd = calculate_vpd(sensor_data['temperature'], sensor_data['humidity'])
        return {**sensor_data, 'vpd': vpd}
    except Exception as e:
        print(f"Error: {e}")
        return None
