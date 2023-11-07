# modules/api_utils.py

import requests
from datetime import datetime, timedelta
import os
from dotenv import load_dotenv
from pathlib import Path

# Calculate the path to the .env file
env_path = Path('..') / '.env'

# Load .env file
load_dotenv(dotenv_path=env_path)

def refresh_api_token():
    account_key = os.getenv('UBI_ACCOUNT_KEY')
    url = "https://webapi.ubibot.com/accounts/generate_access_token"
    params = {"account_key": account_key, "expire_in_seconds": 3600}  # Adjust expiry as needed

    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()
        token = data.get("token")
        expiry = datetime.now() + timedelta(seconds=int(data.get("expire_in_seconds", 3600)))
        return token, expiry
    except requests.RequestException as e:
        print(f"Error generating new API token: {e}")
        return None, None
