# Python 3.6, gdal, ogr
# Getting the extent of the DEM
# ulx, uly is the upper left corner, lrx, lry is the lower right corner
# poly is returned as an ogr geometry object. use .ExportToWkt() to make it wkt, .ExportToJson(), etc...

import gdal
import ogr

def tif_enve_to_poly(tif_path):
    src = gdal.Open(tif_path)
    ulx, xres, xskew, uly, yskew, yres  = src.GetGeoTransform()
    lrx = ulx + (src.RasterXSize * xres)
    lry = uly + (src.RasterYSize * yres)

    # Create polygon from bounding box
    # Create ring
    ring = ogr.Geometry(ogr.wkbLinearRing)
    ring.AddPoint(ulx, uly)
    ring.AddPoint(ulx, lry)
    ring.AddPoint(lrx,lry)
    ring.AddPoint(lrx, uly)
    ring.AddPoint(ulx, uly)

    # Create polygon
    poly = ogr.Geometry(ogr.wkbPolygon)
    poly.AddGeometry(ring)
    
    return poly
