#!/bin/python3

import csv
import sys
from geopy.geocoders import Nominatim
from time import sleep
import numpy as np

'''
    Found through this site: https://www.w3resource.com/python-exercises/geopy/python-geopy-nominatim_api-exercise-4.php
    References here: https://geopy.readthedocs.io/en/stable/#nominatim
    Policy here: https://operations.osmfoundation.org/policies/nominatim/

'''

def _ping(geolocator, area):
    location = geolocator.geocode(area + ", Utah")
    sleep(np.random.uniform(1,4)) # only one ping per second allowed, extra to be safe
    if location != None and location.point != None: # location.point == (latitude, longitude, altitude)
        return location.point
    return None


def main(args):
    pinged = set()
    geolocator = Nominatim(user_agent="BYUcs472 avalanche project")

    with open(args[0], mode="r", newline='') as csvfile:
        with open(args[1], mode="w", newline='') as outCsvFile:
            reader = csv.reader(csvfile)
            writer = csv.writer(outCsvFile)
            
            for row in reader:
                if row[0] == 'Date':
                    writer.writerow(row[:-1] + ['longitude', 'latitude', 'altitude'] + row[-1])
                elif len(row) > 2 and len(row[1]) > 0 and row[1] not in pinged:
                    pinged.add(row[1])
                    point = None
                    point = _ping(geolocator, row[1])
                    if point != None:
                        writer.writerow(row[:-1] + [point.longitude, point.latitude, point.altitude] + row[-1])
                        print('.', end='')
                    else:
                        print('N', end='')
    print("\nDone\n")

if __name__ == "__main__":
    if len(sys.argv) < 3:
        raise SyntaxError("Need names of file to read and file to write")
    main(sys.argv[1:])
