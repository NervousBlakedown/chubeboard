# test_api.py
import requests
import yaml
import pandas as pd

app_key = None

# 'modes' parameter options
modes = """tube,dlr,overground,tram,bus,national-rail,
           tflrail,river-bus,river-tour,cable-car,coach,
           cycle-hire,walking,hire-car"""

# Tube line options
line_ids = ['bakerloo', 'central', 'circle', 'district', 'hammermsmith-city',
            'jubilee','metropolitan', 'northern', 'piccadilly', 'victoria',
            'waterloo-city']

# Load API creds
def load_config(config_file='C:\\Users\\blake\\Documents\\github\\credentials\\tfl_api_credentials.yaml'):
    """
    Load the YAML configuration file and set the global app_key.

    Args:
        config_file (str): Path to the YAML configuration file.

    Returns:
        dict: Configuration settings.
    """
    global app_key  # use app_key once

    try:
        with open(config_file, 'r') as file:
            config = yaml.safe_load(file)
        
        if config and 'app_key' in config:
            app_key = config['app_key']  # Assign API key to the global variable
        else:
            print("API key not found in the configuration file.")
    except FileNotFoundError:
        print(f"Configuration file {config_file} not found.")
    except yaml.YAMLError as e:
        print(f"Error parsing YAML file: {e}")

load_config()

# Now app_key can be used globally in any function
def test_api_call():
    """
    Example function to demonstrate using the global app_key.
    """
    if app_key:
        print(f"API key found: {app_key}")
        # Here you would make your actual API call using app_key
    else:
        print("API key is not set.")


# 1. Get tube line names (not needed, but good start ('Victoria' or 'victoria', 'Central,' etc.))
def get_tube_lines(app_key):
    """
    Fetch all Tube lines with their IDs.

    Args:
        app_key (str): The application key for authenticating the API request.
    """
    url = "https://api.tfl.gov.uk/line/mode/tube"
    try:
        response = requests.get(url, params={'app_key': app_key})
        response.raise_for_status()
        tube_lines = response.json()
        print(f"Found {len(tube_lines)} tube lines:")
        for line in tube_lines:
            print(f"{line['name']} (ID: {line['id']})")
        return tube_lines
    except requests.RequestException as e:
        print(f"Error fetching Tube lines: {e}")


# 2. Get IDs for all stations on a specific Tube line
def get_stations_on_lines(line_ids, app_key):
    """
    Fetch all stations on multiple Tube lines.

    Args:
        line_ids (list): A list of Tube line IDs (e.g., ['central', 'victoria']).
        app_key (str): The application key for authenticating the API request.

    Returns:
        dict: A dictionary where the key is the Tube line ID and the value is the list of stations.
    """
    all_stations = {}

    for line_id in line_ids:
        url = f"https://api.tfl.gov.uk/line/{line_id}/stoppoints"
        try:
            response = requests.get(url, params={'app_key': app_key})
            response.raise_for_status()
            stations = response.json()
            print(f"Found {len(stations)} stations on the {line_id} line:")

            station_list = []
            for station in stations:
                station_info = {
                    'station_name': station['commonName'],
                    'station_id': station['stationNaptan']
                }
                print(f"{station_info['station_name']} (ID: {station_info['station_id']})")
                station_list.append(station_info)

            # Add the list of stations for this line to the dictionary
            all_stations[line_id] = station_list

        except requests.RequestException as e:
            print(f"Error fetching stations for {line_id} line: {e}")
            all_stations[line_id] = None  # Indicate failure to retrieve stations for this line

    return all_stations

# 3. Disruptions
def get_all_line_disruptions(app_key, modes = 'tube,dlr,overground,tram'):
    """
    Fetch real-time disruptions on all Tube lines.

    Args:
        app_key (str): The application key for authenticating the API request.

    Returns:
        list: A list of disruptions across all Tube lines, or None if there are no disruptions.
    """
    url = f"https://api.tfl.gov.uk/line/mode/{modes}/disruption"
    print()
    try:
        response = requests.get(url, params={'app_key': app_key})
        response.raise_for_status()
        disruptions = response.json()
        
        if disruptions:
            print(f"Found {len(disruptions)} disruptions on the Tube network:")
            for disruption in disruptions:
                line_name = disruption.get('lineId', 'Unknown Line')
                print(f"\nLine: {line_name}")
                print(f"Category: {disruption['category']}")
                print(f"Description: {disruption['description']}")
                print("Affected Stops:")
                for stop in disruption.get('affectedStops', []):
                    print(f"  - {stop['commonName']} (ID: {stop['stationNaptan']})")
            return disruptions
        else:
            print("No disruptions found on the Tube network.")
            return None
    except requests.RequestException as e:
        print(f"Error fetching disruptions for the Tube network: {e}")
        return None

