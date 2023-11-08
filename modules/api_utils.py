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

def generate_access_token():
    url = "https://webapi.ubibot.com/accounts/generate_access_token"
    params = {"account_key": UBI_ACCOUNT_KEY}
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()
        token = data.get("token_id")
        expiry_seconds = int(data.get("expire_in_seconds", 3600))
        expiry_time = datetime.now() + timedelta(seconds=expiry_seconds)
        print(f"Access Token: {token}, Expires in: {expiry_seconds} seconds")
        return token, expiry_time
    except requests.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}, Response: {response.text}")
    except Exception as err:
        print(f"Other error occurred: {err}")

def get_sensor_data(token):
    headers = {'content-type': 'application/json', 'Authorization': f'Bearer {token}'}
    url = "https://webapi.ubibot.com/channels"
    params = {'token_id': token}
    try:
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()
        sensor_data = response.json()

        # Extracting temperature and humidity for the specific channel
        for channel in sensor_data.get('channels', []):
            if channel['channel_id'] == UBI_CHANNEL_ID:
                last_values = json.loads(channel.get('last_values', '{}'))
                temperature = last_values.get('field1', {}).get('value')
                humidity = last_values.get('field2', {}).get('value')
                print(f"Retrieved Sensor Data: Temperature - {temperature}, Humidity - {humidity}")
                return {'temperature': temperature, 'humidity': humidity}
        else:
            print("Channel not found.")
            return {}

    except requests.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}, Response: {response.text}")
    except Exception as err:
        print(f"Other error occurred: {err}")

# Testing the functions (optional)
if __name__ == "__main__":
    try:
        token, _ = generate_access_token()
        if token:
            get_sensor_data(token)
    except Exception as e:
        print(f"Error in main: {e}")
