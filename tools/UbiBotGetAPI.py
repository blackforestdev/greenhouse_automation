import os
import requests
from dotenv import load_dotenv

# Load environment variables from the .env file in the parent directory
parent_directory = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
dotenv_path = os.path.join(parent_directory, '.env')
load_dotenv(dotenv_path)

ubi_channel_id = os.getenv("UBI_CHANNEL_ID")
ubi_account_key = os.getenv("UBI_ACCOUNT_KEY")
ubi_read_api_key = os.getenv("UBI_READ_API_KEY")
ubi_write_api_key = os.getenv("UBI_WRITE_API_KEY")

def validate_read_api_key(channel_id, read_api_key):
    url = f"https://webapi.ubibot.com/channels/{channel_id}/feeds.json"
    
    headers = {"api_key": read_api_key}
    try:
        response = requests.get(url, headers=headers)
        
        if response.status_code == 200:
            print("Read API Key is valid.")
            return True
        else:
            print(f"Read API Key validation failed. Status Code: {response.status_code}")
            return False
    except Exception as e:
        print(f"Error during Read API Key validation: {e}")
        return False

def main():
    if validate_read_api_key(ubi_channel_id, ubi_read_api_key):
        print("Read API Key validation successful.")
    else:
        print("Read API Key validation failed.")

if __name__ == "__main__":
    main()
