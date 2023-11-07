import os
from dotenv import load_dotenv

# Load environment variables from the .env file in the parent directory
parent_directory = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
dotenv_path = os.path.join(parent_directory, '.env')
load_dotenv(dotenv_path)

ubi_account_key = os.getenv("UBI_ACCOUNT_KEY")

import requests

def generate_access_token(account_key, expire_in_seconds=3600):
    url = f"https://webapi.ubibot.com/accounts/generate_access_token?account_key={account_key}&expire_in_seconds={expire_in_seconds}"
    
    try:
        response = requests.get(url)  # or requests.post(url) if required
        if response.status_code == 200:
            data = response.json()
            return data.get("token_id")
        else:
            print(f"Failed to generate access token. Status Code: {response.status_code}")
            return None
    except Exception as e:
        print(f"Error during Access Token generation: {e}")
        return None

def main():
    token_id = generate_access_token(ubi_account_key)
    if token_id:
        print(f"Access Token generated successfully: {token_id}")
        # You can now use this token_id for further API calls
    else:
        print("Failed to generate Access Token.")

if __name__ == "__main__":
    main()
