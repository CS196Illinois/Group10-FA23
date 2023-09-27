from typing import List

import gpxpy
import gpxpy.gpx
import matplotlib.pyplot as plt
from scipy.signal import medfilt

with open('../data/Evening_Ride2.gpx', 'r') as f:
    gpx = gpxpy.parse(f)


for track in gpx.tracks:
    for segment in track.segments:
        fig, (ax1, ax2, ax3) = plt.subplots(nrows=3, ncols=1)

        speeds = [segment.get_speed(i) for i in range(len(segment.points))]
        ax1.plot(speeds)
        for i in range(5):
            segment.smooth(horizontal=True)

        point_smoothed_speeds = [segment.get_speed(i) for i in range(len(segment.points))]
        ax2.plot(point_smoothed_speeds)

        median_smoothed_speeds = medfilt(speeds, kernel_size=7)
        ax3.plot(median_smoothed_speeds)

        plt.show()



