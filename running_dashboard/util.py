import os
import gpxpy

# dir = os.getcwd()
# os.chdir(os.path.join(os.path.expanduser('~'), '/home/uri/Documents/programming/experiments/gpx'))
# fname = input('Paste layer name:')

def gpxToWkt(gpx_file):

    # gpx_file = open(fname)
    gpx = gpxpy.parse(gpx_file)
    wkt = "LINESTRING ("

    if len(gpx.tracks) > 0:
        for track in gpx.tracks:
            for segment in track.segments:
                for index, point in enumerate(segment.points):
                    wkt += f"{point.longitude} {point.latitude}"
                    if index < len(segment.points) - 1:
                        wkt += ","

    elif len(gpx.routes) > 0:
        for route in gpx.routes:
            for index, point in enumerate(route.points):
                wkt += f"{point.longitude} {point.latitude}"
                if index < len(route.points) - 1:
                    wkt += ","

    wkt += ")"
    return wkt