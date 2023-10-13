#RESEARCH FILE

import gpxpy
import gpxpy.gpx
import xml
import math
from haversine import *
from dateutil import parser
from datetime import date

#Parse the gpx file provided by Nikhil

file = open(r'C:\Users\srika\.vscode\Group10-FA23\Research\sgiri6\Evening_Ride2.gpx', 'r')
parsed_file = gpxpy.parse(file)


#Print out positional data for testing purposes


for track in parsed_file.tracks:
    for segment in track.segments:
        point1 = ""
        totalDistance = 0
        elapsedTime = 0
        for point2 in segment.points:

            if point1 == "":
               point1 = point2

            distance = haversine((point1.latitude, point1.longitude), (point2.latitude, point2.longitude), unit='km')
            totalDistance += distance
            time = (point2.time - point1.time).total_seconds()
            elapsedTime += time

            if time == 0:
               continue

            velocity = distance / time
             
            print('Point at ({0},{1}) -> with elevation of {2}'.format(point2.latitude, point2.longitude, point2.elevation))
            print('Distance covered in this time of {0} s is {1} km, with velocity of {2} km/hr'.format(time, distance, velocity * 3600))
            point1 = point2

        elapsedTime /= 3600
        aVelocity = totalDistance/elapsedTime
        print("Total distance covered in km: " + str(totalDistance))
        print("Total time elapsed in hours: " + str(elapsedTime))
        print(("Average velocity in kph: " + str(aVelocity)))


