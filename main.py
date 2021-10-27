import geopandas as gpd
from shapely.geometry import Point, LineString, shape
import shapely.wkt
import json
import folium
from folium import IFrame
from folium.raster_layers import WmsTileLayer
start_coords = (43.16214328034576, 21.4536145167952)
m = folium.Map(
    location=start_coords, zoom_start=8
)

'''
            "http://server.arcgisonline.com/ArcGIS/rest/services/World_Topo_Map/MapServer" // World Topographic Map
            "http://server.arcgisonline.com/ArcGIS/rest/services/World_Street_Map/MapServer" // World Street Map
            "http://services.arcgisonline.com/ArcGIS/rest/services/Canvas/World_Light_Gray_Base/MapServer" // Light Gray Canvas
            "http://services.arcgisonline.com/ArcGIS/rest/services/NatGeo_World_Map/MapServer" // National Geographic World Map
            "http://services.arcgisonline.com/ArcGIS/rest/services/Ocean_Basemap/MapServer" // Ocean Basemap
            "http://services.arcgisonline.com/ArcGIS/rest/services/World_Terrain_Base/MapServer" // Terrain with Labels
            "http://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer" // World Imagery
'''

url = (
    'http://services.arcgisonline.com/arcgis/rest/services/World_Imagery'
    + '/MapServer/tile/{z}/{y}/{x}'
)
WmsTileLayer(
    url=url,
    layers=None,
    name='ESRI Imagery',
    attr='ESRI World Imagery',
).add_to(m)



df = gpd.read_file('medieini1.geojson')
d = df['geometry']
gdd = gpd.GeoDataFrame.from_dict(d, orient='columns')
index1 = gdd.index
index2 = gdd.index.stop
v = 0
for v in range(index2):
    s = gpd.GeoSeries(d)
    test = str(s[v])
    print(test)
    g1 = shapely.wkt.loads(test)
    g2 = shapely.geometry.mapping(g1)
    g3 = json.dumps(g2)
    print(g3)
    n = df['NAME'][v]
    fillColor = df['_umap_options'][v]['color']
    fillOpacity = df['_umap_options'][v]['fillOpacity']
    color = 'Black'
    print(fillColor, fillOpacity)
    sf = lambda y, fillColor=fillColor, fillOpacity=fillOpacity, color=color: {
        'fillColor': fillColor,
        'fillOpacity': fillOpacity,
        'color': color,
    }
    a = folium.GeoJson(
        data=g3,
        name='noms des calques',
        style_function=sf,
        tooltip=n,
    )
    print("Travail accompli")
    a.add_to(m)

folium.LayerControl().add_to(m)
m.save('index.html')
