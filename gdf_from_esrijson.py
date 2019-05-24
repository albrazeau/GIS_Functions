import geopandas as gpd
import shapely
from shapely.geometry import Point, Polygon, LineString

def from_esrijson(ej):
    esrig = {'esriGeometryPoint': 'Point',
             'esriGeometryPolyline': 'LineString',
             'esriGeometryPolygon': 'Polygon'}
    gtype = esrig[ej['geometryType']]
    g = 'geometry'
    a = 'attributes'
    
    srs = {'init': ej['spatialReference']['wkid']}
    cols = [ej['fields'][i]['name'] for i in range(len(ej['fields']))] + [g]
    feats = ej['features']
    gdf = gpd.GeoDataFrame(columns=cols)
    gdf.crs = srs
    
    if gtype == 'LineString':
        for i, f in enumerate(feats):
            for k, v in f[a].items():
                gdf.loc[i, k] = v
            coords = f[g]['paths'][0]    
            gdf.loc[i, g] = LineString([(xy[0], xy[1]) for xy in coords])    
        return gdf
    
    elif gtype == 'Polygon':
        for i, f in enumerate(feats):
            for k, v in f[a].items():
                gdf.loc[i, k] = v
            coords = f[g]['rings'][0]    
            gdf.loc[i, g] = Polygon([(xy[0], xy[1]) for xy in coords])      
        return gdf
    
    elif gtype == 'Point':
        for i, f in enumerate(feats):
            for k, v in f[a].items():
                gdf.loc[i, k] = v
            coords = f[g]    
            gdf.loc[i, g] = Point(coords['x'], coords['y'])      
        return gdf
    
    else:
        return Exception('Invalid geometry type')
