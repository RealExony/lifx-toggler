import os
import requests
import json

# Define the path to the configuration file
CONFIG_FILE = "lifx_config.json"

# Define the LIFX API endpoint
TOGGLE_ENDPOINT = "https://api.lifx.com/v1/lights/all/toggle"

def get_api_key():
    """
    Returns the LIFX API key from the configuration file, if it exists.
    Otherwise, prompts the user to enter the API key and saves it to the
    configuration file.
    """
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, "r") as f:
            config = json.load(f)
            api_key = config.get("api_key")
    else:
        api_key = input("Enter your LIFX API key: ")
        with open(CONFIG_FILE, "w") as f:
            json.dump({"api_key": api_key}, f)
    return api_key


def toggle_lights():
    """
    Toggles the state of all LIFX lights using the LIFX API.
    Returns True if the lights were successfully toggled, False otherwise.
    """
    api_key = get_api_key()
    headers = {"Authorization": f"Bearer {api_key}"}
    response = requests.post(TOGGLE_ENDPOINT, headers=headers)
    if response.status_code == 207:
        response_data = response.json()
        first_light_state = response_data[0]["status"]["power"]
        if first_light_state == "on":
            print("Lights turned off")
        else:
            print("Lights turned on")
        return True
    else:
        print(f"Error toggling lights: {response.status_code}")
        return False

if __name__ == "__main__":
    toggle_lights()
