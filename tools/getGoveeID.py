import requests

api_key = '6e59604b-9dad-4ed2-a24e-9f833556be9e'
# url = 'https://developer-api.govee.com/v1/devices'  # Endpoint to list devices
url = 'https://developer-api.govee.com/v1/appliance/devices' #Endpoint to list Appliance

headers = {
    'Govee-API-Key': api_key
}

response = requests.get(url, headers=headers)

if response.status_code == 200:
    # If the request was successful, print the raw response
    print("Raw API response:")
    print(response.json())
    
    # Extract and print all devices
    devices = response.json().get('data', {}).get('devices', [])
    if devices:
        print("Devices found:")
        for device in devices:
            print(f"Device Name: {device.get('deviceName')} - Device ID: {device.get('device')}")
    else:
        print("No devices were listed in the API response.")
else:
    print("Failed to retrieve devices from Govee API:", response.status_code)
