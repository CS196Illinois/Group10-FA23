import gpxpy
import mpu
from dateutil import parser
from haversine import *


#takes file as input
def motionFunc( file ):
    parsed_file = gpxpy.parse(file)
    #we want total distance and time to find avg velocity
    totalDistance = 0
    totalDuration = 0

    #going over each track
    for track in parsed_file.tracks:
        #going over each segment
        for segment in parsed_file.segments:
            #set previousPoint to be uninitialzed at first
            previousPoint = ""

            for currentPoint in segment.points:
                if previousPoint == "":
                    previousPoint = currentPoint
                
                #not sure about this way of getting distance
                dist = mpu.haversine((previousPoint.latitude, previousPoint.longitude), (currentPoint.latitude, currentPoint.longitude))
                totalDistance += dist
                duration = (previousPoint.time - currentPoint.time).total_seconds()
                totalDuration += duration
  
                #update previousPoint
                previousPoint = currentPoint

    avgVelocity = totalDistance/totalDuration
    return avgVelocity

git config --global user.email "ilacpetrovic@gmail.com"
git config --global user.name "Ila Petrovic"






