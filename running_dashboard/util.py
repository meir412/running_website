import os
import gpxpy

def gpxToWkt(gpx_string):
    """
    Function that receives a string containing the contents of a gpx file, parses it using
    a method from the gpxpy module and returns a string containing the well known text value
    of the route or track found in the gpx string.
    """
    gpx = gpxpy.parse(gpx_string)
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