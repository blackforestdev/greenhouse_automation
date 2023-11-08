import requests
import json
from dotenv import load_dotenv
import os

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
        token = response.json().get("token_id")
        print("Generated Token:", token)
        return token
    else:
        print("Access Token Generation Failed:", response.text)
        raise Exception("Failed to generate access token")

def get_sensor_data(token):
    headers = {'content-type': 'application/json', 'Authorization': f'Bearer {token}'}
    url = "https://webapi.ubibot.com/channels"
    params = {'token_id': token}
    response = requests.get(url, headers=headers, params=params)
    if response.status_code == 200:
        return response.json()
    else:
        print("Sensor Data Retrieval Failed:", response.text)
        raise Exception("Failed to get sensor data")

def main():
    try:
        token = generate_access_token()
        sensor_data = get_sensor_data(token)
        
        # Extracting temperature and humidity
        for channel in sensor_data.get('channels', []):
            if channel['channel_id'] == UBI_CHANNEL_ID:
                last_values = json.loads(channel.get('last_values', '{}'))
                temp = last_values.get('field1', {}).get('value')
                humidity = last_values.get('field2', {}).get('value')
                print(f"Temperature: {temp}°C, Humidity: {humidity}%")
                break
        else:
            print("Channel not found.")
        
    except Exception as e:
        print("Error:", e)

if __name__ == "__main__":
    main()
