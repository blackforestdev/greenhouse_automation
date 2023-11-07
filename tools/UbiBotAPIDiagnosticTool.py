from dotenv import load_dotenv
import os
import logging
import requests

load_dotenv()
# load data from .env
ubi_channel_id = os.getenv("UBI_CHANNEL_ID")
ubi_account_key = os.getenv("UBI_ACCOUNT_KEY")
ubi_api_key = os.getenv("UBI_API_KEY")

# API Request Function
def make_ubibot_api_request():
    url = "https://api.ubibot.io/channels/{}/feeds.json".format(ubi_channel_id)
    headers = {
        "account_key": ubi_account_key,
        "api_key": ubi_api_key
    }
    
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.HTTPError as errh:
        print("Http Error:", errh)
    except requests.exceptions.ConnectionError as errc:
        print("Error Connecting:", errc)
    except requests.exceptions.Timeout as errt:
        print("Timeout Error:", errt)
    except requests.exceptions.RequestException as err:
        print("OOps: Something Else", err)

# Main Function
def main():
    api_response = make_ubibot_api_request()
    if api_response:
        # Process the response
        print(api_response)
    else:
        print("Failed to get a valid response from the UbiBot API.")

if __name__ == "__main__":
    main()

#error logging
logging.basicConfig(filename='ubibot_api_errors.log', level=logging.DEBUG)
