# /modules/api_utils.py

import requests
import json
from datetime import datetime, timedelta
import os
from dotenv import load_dotenv

# Load .env file
load_dotenv(os.path.join(os.path.dirname(__file__), '../.env'))

# Get UbiBot account details from .env file
UBI_ACCOUNT_KEY = os.getenv("UBI_ACCOUNT_KEY")
UBI_CHANNEL_ID = os.getenv("UBI_CHANNEL_ID")
UBI_READ_API_KEY = os.getenv("UBI_READ_API_KEY")

def generate_access_token():
    url = "https://webapi.ubibot.com/accounts/generate_access_token"
    params = {"account_key": UBI_ACCOUNT_KEY}
    response = requests.get(url, params=params)
    if response.status_code == 200:
        data = response.json()
        token = data.get("token_id")
        expiry_seconds = int(data.get("expire_in_seconds", 3600))
        expiry_time = datetime.now() + timedelta(seconds=expiry_seconds)
        return token, expiry_time
    else:
        print("Access Token Generation Failed:", response.text)
        raise Exception("Failed to generate access token")

def get_sensor_data(token):
    headers = {'content-type': 'application/json', 'Authorization': f'Bearer {token}'}
    url = f"https://webapi.ubibot.com/channels/{UBI_CHANNEL_ID}/feeds.json"
    params = {'api_key': UBI_READ_API_KEY}
    response = requests.get(url, headers=headers, params=params)
    if response.status_code == 200:
        sensor_data = response.json()
        latest_data = sensor_data.get('feeds', [])[0] if sensor_data.get('feeds') else {}
        temperature = latest_data.get('field1', {}).get('value')
        humidity = latest_data.get('field2', {}).get('value')
        return {'temperature': temperature, 'humidity': humidity}
    else:
        raise Exception(f"Failed to get sensor data: {response.text}")
