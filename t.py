#!/usr/bin/python
import os
import time
from phue import Bridge

print os.path.join(os.getcwd(), '.python_hue')
b = Bridge('192.168.136.56', config_file_path="./confighue")
print b.username
# If the app is not registered and the button is not pressed, press the button and call connect() (this only needs to be run a single time)
b.connect()

# Get the bridge state (This returns the full dictionary that you can explore)
b.get_api()
lights = b.get_light_objects('name')
print lights
