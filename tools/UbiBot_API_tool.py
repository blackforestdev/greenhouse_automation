import requests
import json

def get_ubibot_device_channels(account_key):
    # Add the account_key as a query parameter in the URL
    url = f'https://webapi.ubibot.com/channels?account_key={account_key}'
    
    response = requests.get(url)
    
    if response.status_code == 200:
        # Print the raw response to understand the structure
        print(json.dumps(response.json(), indent=4))
        
        channels = response.json().get('result')
        if channels:
            print("Channels (Devices) found:")
            for channel in channels:
                # Let's print what 'channel' actually is
                print(channel)
                # If 'channel' is indeed a dictionary, this will work, otherwise we will adjust
                print(f"Channel Name: {channel.get('channel_name', 'Unknown')} - Channel ID: {channel.get('channel_id', 'Unknown')}")
        else:
            print("No channels (devices) were found associated with this account.")
    else:
        print(f"Failed to retrieve channels. Status Code: {response.status_code}, Response: {response.text}")

# Replace 'your_account_key_here' with your actual UbiBot account key
account_key = 'f23b1d6093b52054e1edadd224d5a116'
get_ubibot_device_channels(account_key)
