import folium
import pandas as pd

# Variable for data from text file
data = pd.read_csv("Volcanoes.txt")

# Data converted into list: latitude, longitude, elevation and name
lat = list(data["LAT"])
lon = list(data["LON"])
elev = list(data["ELEV"])
name = list(data["NAME"])

def color_producer(elevation):
    if elevation < 1000:
        return 'green'
    elif 1000 <= elevation < 3000:
        return 'orange'
    else:
        return 'red'


html = """
Volcano name:<br>
<a href="https://www.google.com/search?q=%%22%s%%22" target="_blank">%s</a><br>
Height: %s m
"""


#Map Initialization over the Slovakia with level of zoom 6
map = folium.Map(location=[37.782572718124115, -106.04005803196567], zoom_start=4, tiles="Stamen Terrain")

fgv = folium.FeatureGroup(name="Volacanoes")
#Adding a new custom point with .add_child folium method
for lt, ln, el, name in zip(lat, lon, elev, name):
    iframe = folium.IFrame(html=html % (name, name, el), width=200, height=100)
    fgv.add_child(folium.CircleMarker(location=[lt, ln],
                            radius= 10,
                            popup=folium.Popup(iframe),
                            fill_color=color_producer(el),
                            color = 'white',
                            fill_opacity = 0.7))
fgp = folium.FeatureGroup(name="Population")
fgp.add_child(folium.GeoJson(data=open('world.json', 'r', encoding='utf-8-sig').read(),
                            style_function=lambda x: {'fillColor': 'green' if x['properties']['POP2005'] < 10000000
                            else 'orange' if 10000000 <= x['properties']['POP2005'] < 20000000
                            else 'red'}))


map.add_child(fgv)
map.add_child(fgp)
map.add_child(folium.LayerControl())
#Export map as html output
map.save("Map_advanced.html")
print("Done")