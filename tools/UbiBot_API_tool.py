import requests
import json
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

def get_ubibot_device_channels(api_key):
    url = f'https://webapi.ubibot.com/channels?api_key={api_key}'
    response = requests.get(url)
    
    if response.status_code == 200:
        response_data = response.json()
        channels = response_data.get('channels', [])
        if channels:
            print("Channels (Devices) found:")
            for channel in channels:
                print(f"Channel Name: {channel.get('name', 'Unknown')} - Channel ID: {channel.get('channel_id', 'Unknown')}")
        else:
            print("No channels (devices) were found associated with this account.")
    else:
        print(f"Failed to retrieve channels. Status Code: {response.status_code}, Response: {response.text}")

# Retrieve the API key from the .env file
api_key = os.getenv('UBI_API_KEY')

get_ubibot_device_channels(api_key)