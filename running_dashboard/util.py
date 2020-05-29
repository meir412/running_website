import os
import gpxpy

from gpxpy.gpx import GPXXMLSyntaxException


def attributesFromGpx(gpx_string):
    """
    Function that receives a string containing the contents of a gpx file, parses it using
    a method from the gpxpy module and returns a string containing the well known text value
    of the route or track found in the gpx string.
    """
    try:
        gpx = gpxpy.parse(gpx_string)

    except GPXXMLSyntaxException:
        raise ValueError("File is not a gpx file")

    wkt = "LINESTRING ("

    if len(gpx.tracks) > 0:
        for track in gpx.tracks:
            for segment in track.segments:
                for index, point in enumerate(segment.points):
                    wkt += f"{point.longitude} {point.latitude}"
                    if index < len(segment.points) - 1:
                        wkt += ","
    
    else:
        raise ValueError("No tracks were found inside the gpx file")

    start_time = gpx.tracks[0].segments[0].points[0].time
    end_time = gpx.tracks[0].segments[0].points[-1].time
    time_sec = (end_time - start_time).seconds


    # elif len(gpx.routes) > 0:
    #     for route in gpx.routes:
    #         for index, point in enumerate(route.points):
    #             wkt += f"{point.longitude} {point.latitude}"
    #             if index < len(route.points) - 1:
    #                 wkt += ","

    attributes = {}
    wkt += ")"
    attributes["wkt"] = wkt
    attributes["start_time"] = start_time
    attributes["time_sec"] = time_sec
    return attributes