# Used to create geometry of a feature in a GeoJSON file directly from the text string
# Getting the geometry of each building to test for intersection with each tiff
# Pulled from a line in a JSON file as a string, output is ogr geometry, can be exported to JSON or WKT
# The .split argument subject to change based on the GeoJSON format

import gdal
import ogr

def create_reproj_building_geom(building_line_from_json):

    json_coords = building_line_from_json.split('"coordinates": [ [ ')[1].split(' ] ] } }')[0].split(' ], [ ')
    ring = ogr.Geometry(ogr.wkbLinearRing)
    for coord in json_coords:
        a = coord.split(',')
        b = list(map(float, a))
        ring.AddPoint(b[0], b[1])
    poly = ogr.Geometry(ogr.wkbPolygon)
    poly.AddGeometry(ring)
    
    return poly
