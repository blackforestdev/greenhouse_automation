# New code
import requests
from datetime import datetime, timedelta
import os
from dotenv import load_dotenv
from pathlib import Path
import json

# Calculate the path to the .env file
env_path = Path('..') / '.env'

# Load .env file
load_dotenv(dotenv_path=env_path)

UBI_CHANNEL_ID = os.getenv('UBI_CHANNEL_ID')
UBI_READ_API_KEY = os.getenv('UBI_READ_API_KEY')

def generate_access_token():
    account_key = os.getenv('UBI_ACCOUNT_KEY')
    url = "https://webapi.ubibot.com/accounts/generate_access_token"
    params = {"account_key": account_key, "expire_in_seconds": 3600}  # Adjust expiry as needed

    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()
        token = data.get("token_id")
        expiry_seconds = int(data.get("expire_in_seconds", 3600))
        expiry_time = datetime.now() + timedelta(seconds=expiry_seconds)
        return token, expiry_time
    except requests.RequestException as e:
        print(f"Error generating new API token: {e}")
        return None, None

def get_sensor_data(token):
    headers = {'Authorization': f'Bearer {token}'}
    url = f"https://webapi.ubibot.com/channels/{UBI_CHANNEL_ID}/feeds.json"
    params = {'api_key': UBI_READ_API_KEY}
    response = requests.get(url, headers=headers, params=params)
    if response.status_code == 200:
        sensor_data = response.json()
        # Extracting temperature and humidity from the sensor data
        latest_data = sensor_data.get('feeds', [])[0] if sensor_data.get('feeds') else {}
        temperature = latest_data.get('field1', {}).get('value')
        humidity = latest_data.get('field2', {}).get('value')
        return {'temperature': temperature, 'humidity': humidity}
    else:
        raise Exception(f"Failed to get sensor data: {response.text}")

# Add any other utility functions if needed
