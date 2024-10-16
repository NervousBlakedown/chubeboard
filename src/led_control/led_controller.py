import requests
import time
import board
import neopixel

# Set up the LED strip (GPIO pin 18, 50 LEDs)
pixel_pin = board.D18
num_pixels = 50
pixels = neopixel.NeoPixel(pixel_pin, num_pixels, brightness=0.5, auto_write=False)

# Function to light up an LED based on train data
def light_up_led(position):
    # Turn off all LEDs first
    pixels.fill((0, 0, 0))
    
    # Light up the LED at the train's position
    pixels[position] = (255, 0, 0)  # Red color for train location
    pixels.show()

# Example usage: Light up the 10th LED
light_up_led(10)

def get_train_position(station_name):
    # Simple mapping from station names to LED positions
    station_map = {
        'Oxford Circus': 5,
        'Bond Street': 6,
        'Bank': 10,
        'Liverpool Street': 12,
    }
    return station_map.get(station_name, -1)

# Example usage: Get train position and light up corresponding LED
train_station = 'Oxford Circus'
position = get_train_position(train_station)
if position != -1:
    light_up_led(position)

while True:
    # Fetch train data for a specific line
    train_data = get_train_data('central')
    
    # Iterate through each train and update the corresponding LED
    for train in train_data:
        station_name = train['stationName']
        led_position = get_train_position(station_name)
        if led_position != -1:
            light_up_led(led_position)
    
    # Wait a few seconds before fetching new data
    time.sleep(10)