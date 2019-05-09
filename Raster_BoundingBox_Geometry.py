# Python 3.6, gdal, ogr
# Getting the extent of the DEM
# ulx, uly is the upper left corner, lrx, lry is the lower right corner
# poly is returned as an ogr geometry object. use .ExportToWkt() to make it wkt, .ExportToJson(), etc...

import gdal
import ogr

# From local
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

# From s3
from io import BytesIO
import boto3
# one of these needs to be set... not sure which
#s3 = boto3.resource('s3')
#s3_client = boto3.client('s3')

def tif_enve_to_poly(s3tif):

# include these three lines if it is an s3 path not an s3 object
#     bucket_name = s3path.split(r's3://')[1].split(r'/')[0]
#     key = s3path.split(r'{}/'.format(bucket_name))[1] 
#     s3tif = s3.Object(bucket_name=bucket_name, key=key)
    image_data = BytesIO(s3tif.get()['Body'].read())
    tif_inmem = "/vsimem/data.tif" #Virtual Folder to Store Data
    gdal.FileFromMemBuffer(tif_inmem, image_data.read())
    
    src = gdal.Open(tif_inmem)
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
