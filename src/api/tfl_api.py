# tfl_api.py
import requests
import yaml

# Load YAML configuration file
def load_config(config_file='C:\\Users\\blake\\Documents\\github\\credentials\\tfl_api_credentials.yaml'):
    """
    Load the configuration file (YAML) that contains the API key and other settings.
    
    Args:
        config_file (str): Path to the YAML configuration file.
    
    Returns:
        dict: Configuration settings.
    """
    try:
        with open(config_file, 'r') as file:
            config = yaml.safe_load(file)
        return config
    except FileNotFoundError:
        print(f"Configuration file {config_file} not found.")
        return None
    except yaml.YAMLError as e:
        print(f"Error parsing YAML file: {e}")
        return None

# TFL API URL
BASE_URL = "https://api.tfl.gov.uk/line/{line}/arrivals"

def get_train_data(line, app_key):
    """
    Fetch real-time train data for a specific Tube line from the TFL API.
    
    Args:
        line (str): The name of the tube line (e.g., 'central', 'northern', 'piccadilly')
        app_key (str): The API key to authenticate the request.
    
    Returns:
        list: A list of dictionaries containing train arrival data for the line.
    """
    url = BASE_URL.format(line=line)
    
    try:
        response = requests.get(url, params={'app_key': app_key})
        response.raise_for_status()  # Raise an exception for HTTP errors
        return response.json()  # Return the JSON data as a Python list/dict
    except requests.RequestException as e:
        print(f"Error fetching data from TFL API: {e}")
        return []

def filter_train_data(data, station_name):
    """
    Filter train data for a specific station.
    
    Args:
        data (list): List of train arrival data from the API.
        station_name (str): The name of the station you want to filter for.
    
    Returns:
        list: A list of train information for the specific station.
    """
    return [train for train in data if train['stationName'].lower() == station_name.lower()]


# Example usage:
if __name__ == "__main__":
    # Load the API key from the config.yaml file
    config = load_config()
    if config and 'tfl_api' in config and 'app_key' in config['tfl_api']:
        app_key = config['tfl_api']['app_key']
        
        line = 'central'
        station_name = 'Oxford Circus'
        
        # Fetch the real-time train data
        train_data = get_train_data(line, app_key)
        
        if train_data:
            # Filter the train data for a specific station
            filtered_data = filter_train_data(train_data, station_name)
            for train in filtered_data:
                print(f"Train to {train['destinationName']} arriving at {train['stationName']} in {train['timeToStation']} seconds.")
    else:
        print("API key not found in the configuration file.")
