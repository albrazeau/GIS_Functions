#########################################################
### FIND TIFFS THAT INTERSECT WITH SPECIFIC SHAPEFILES###
#########################################################
## Python 3.6

import os
from glob import glob
import gdal
import fiona
import ogr
from datetime import datetime

## FUNCTIONS ##
#--------------------------------------------------------------------------------------------------

# Define the tif_enve_to_poly function
# Getting the extent of the DEM
# ulx, uly is the upper left corner, lrx, lry is the lower right corner
# poly is returned as an ogr geometry object. use .ExportToWkt() to make it wkt, .ExportToJson(), etc...
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

## VARIABLES / PATHS ##
#--------------------------------------------------------------------------------------------------

txt_file = r'C:\Data\HurricaneMichael\intersects_lists.txt'
extent_shpfile = r'C:\Data\HurricaneMichael\Mexico_Beach.shp'
tiff_dir = r'C:\Data\HurricaneMichael\NOAA_Imagery\20181011a_RGB'

tiff_filetype = '.tif'

tiffs = glob(os.path.join(tiff_dir, '*{}'.format(tiff_filetype)))
print(len(tiffs))

## CODE ##
#--------------------------------------------------------------------------------------------------

# Start your engines
start = datetime.now()
print('Start time = ', start)

driver = ogr.GetDriverByName("ESRI Shapefile")
dataSource = driver.Open(extent_shpfile, 0)
layer = dataSource.GetLayer()

tiff_intersect_list = []
tiff_intersect_paths = []

for feature in layer:
    MEgeom = feature.GetGeometryRef()

    for i, tiff in enumerate(tiffs):
        tiffname = os.path.basename(tiff).split('.')[0]
        tiff_extent = tif_enve_to_poly(tiff)
        if i %100 == 0:
            print(i, '/', len(tiffs))
        
        if tiff_extent.Intersect(MEgeom):
            print(tiffname)
            tiff_intersect_list.append(tiffname)
            tiff_intersect_paths.append(tiff)

with open(txt_file, 'w') as text:
    text.write('There are {} tiffs that intersect.\n\nTiff names:\n'.format(len(tiff_intersect_list))\
               + str(tiff_intersect_list) + '\n\nTiff Paths:\n' + str(tiff_intersect_paths))
            
# Game over
print('Time complete: ', datetime.now())
proc_time = datetime.now()-start
print('Processing time = ', proc_time)

