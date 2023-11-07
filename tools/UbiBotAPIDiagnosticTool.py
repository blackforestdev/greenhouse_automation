import os
import requests
from dotenv import load_dotenv

# Load environment variables from the .env file located in the parent directory
parent_directory = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
dotenv_path = os.path.join(parent_directory, '.env')
load_dotenv(dotenv_path)

ubi_channel_id = os.getenv("UBI_CHANNEL_ID")
ubi_account_key = os.getenv("UBI_ACCOUNT_KEY")
ubi_api_key = os.getenv("UBI_API_KEY")

def validate_api_credentials(channel_id, account_key, api_key):
    if not all([channel_id, account_key, api_key]):
        print("One or more credentials (Channel ID, Account Key, API Key) are missing.")
        return False
    
    # Test API call
    url = f"https://webapi.ubibot.com/channels/{channel_id}/feeds.json"
    headers = {"account_key": account_key, "api_key": api_key}
    
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return True
        else:
            print(f"API credentials validation failed. Status Code: {response.status_code}")
            return False
    except Exception as e:
        print(f"Error during API credentials validation: {e}")
        return False

def fetch_sensor_data(channel_id, account_key, api_key):
    # Function to fetch data from UbiBot API
    # You should add the actual code to fetch data here
    pass  # Use 'pass' as a placeholder if there's no implementation yet

def main():
    if validate_api_credentials(ubi_channel_id, ubi_account_key, ubi_api_key):
        data = fetch_sensor_data(ubi_channel_id, ubi_account_key, ubi_api_key)
        # Process and print data
    else:
        print("Invalid API credentials. Please check your .env file.")

if __name__ == "__main__":
    main()
