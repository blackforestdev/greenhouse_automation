import os
import requests

channel_id = os.getenv('UBI_CHANNEL_ID')
account_key = os.getenv('UBI_ACCOUNT_KEY')

def get_ubibot_data():
    account_key = os.getenv('UBI_ACCOUNT_KEY')

    url = f"https://webapi.ubibot.com/channels?account_key={account_key}"

    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        return data
    except requests.RequestException as e:
        print(f"Error fetching data from UbiBot API: {e}")
        return None

# Additional processing and error handling can be added as needed

def fetch_sensor_data():
    """
    Fetches the latest sensor data (temperature and humidity) from UbiBot.
    """
    account_key = os.getenv('UBI_ACCOUNT_KEY')
    channel_id = os.getenv('UBI_CHANNEL_ID')

    url = f'https://webapi.ubibot.com/channels/{channel_id}/feeds.json?account_key={account_key}'
    
    try:
        response = requests.get(url)
        response.raise_for_status()

        data = response.json()
        latest_data = data['feeds'][0] if data['feeds'] else None

        if latest_data:
            # Replace 'field1' and 'field2' with your actual field keys
            temperature = latest_data.get('field1')
            humidity = latest_data.get('field2')

            return {'temperature': temperature, 'humidity': humidity}

    except requests.RequestException as e:
        # Log the error (consider using a logging framework)
        print(f"Failed to fetch data: {e}")
        return None

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
