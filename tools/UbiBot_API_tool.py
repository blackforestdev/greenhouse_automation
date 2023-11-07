import requests
import json

def get_ubibot_device_channels(account_key):
    url = f'https://webapi.ubibot.com/channels?account_key={account_key}'
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

account_key = 'f23b1d6093b52054e1edadd224d5a116'
get_ubibot_device_channels(account_key)