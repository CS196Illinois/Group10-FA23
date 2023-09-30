import gpxpy
import mpu
from dateutil import parser
from haversine import *



def motionFunc( file ):
    parsed_file = gpxpy.parse(file)

    for track in parsed_file.tracks:
        for segment in parsed_file.segments:
            previousPoint = ""
            totalDistance = 0
            totalTime = 0

            for currentPoint in segment.points:
                if previousPoint == "":
                    previousPoint = currentPoint
                
                dist = mpu.haversine((previousPoint.latitude, previousPoint.longitude), (currentPoint.latitude, currentPoint.longitude))
                totalDistance += dist
                time = (previousPoint.time - currentPoint.time).total_seconds()
                totalTime += time

                if time == 0:
                    previousPoint = currentPoint
                    continue

                previousPoint = currentPoint

    avgVelocity = totalDistance/totalTime





