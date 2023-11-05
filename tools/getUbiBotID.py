import requests 

def get_ubibot_device_channels(account_key):
    # Add the account_key as a query parameter in the URL
    url = f'https://webapi.ubibot.com/channels?account_key={account_key}'

    response = requests.get(url)

    if response.status_code == 200:
        # Parse the JSON response
        data = response.json()
        
        # Access the channels key in the response
        channels = data.get('channels', [])
        if channels:
            print("Channels (Devices) found:")
            for channel in channels:
                # Access the 'name' and 'channel_id' from each channel
                channel_name = channel.get('name', 'Unknown')
                channel_id = channel.get('channel_id', 'Unknown')
                print(f"Channel Name: {channel_name} - Channel ID: {channel_id}")
        else:
            print("No channels (devices) were found associated with this account.")
    else:
        print(f"Failed to retrieve channels. Status Code: {response.status_code}, Response: {response.text}")

# Replace 'your_account_key_here' with your actual UbiBot account key
account_key = 'f23b1d6093b52054e1edadd224d5a116'
get_ubibot_device_channels(account_key)
