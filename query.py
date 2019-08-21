import sys
import datetime

from gtfsrt.reader import GTFSRtReader
from importer.database import Database
from models.trace import GeoTrace

import folium
from folium import plugins

def main(argv):
    db = Database()

    """ pi = [
        {'$match': {'trip.routeId': '467'}},
        {'$group': {'_id': '$trip.tripId', 'rr': {'$first': '$trip.routeId'}}}
    ] """

    pi = [
        {
            '$match': {
                '$and': [
                    {
                        'vehicle.id': {
                            '$in': ['HR55AF0643']
                        }
                    }
                ]
            }
        }
    ]

    l = list(db.aggregate('vehicle_position', pi))

    print(len(l))
    """ print(l[0])
    print(l[len(l)-1]) """

    j = GeoTrace()
    
    for i in l:
        j.add_point(
            timestamp = i['timestamp'], 
            latitude = i['position']['latitude'],
            longitude = i['position']['longitude']
            )

    m = init_folium()
    geo = []
    for k, v in j.items():
        geo.append({
            'time': k.strftime('%Y/%m/%d %H:%M:%S'),
            'coordinates': [v.longitude, v.latitude]
        })
        """ marker = folium.Marker(
            location = [v.latitude, v.longitude],
            popup = str(k)
        )
        m.add_child(marker) """
    #print(geo)

    features = [
    {
        'type': 'Feature',
        'geometry': {
            'type': 'Point',
            'coordinates': point['coordinates'],
        },
        'properties': {
            'time': point['time'],
            'popup': point['time'],
            'id': 'house',
            'icon': 'marker'
        }
    } for point in geo
]
    plugins.TimestampedGeoJson(
        {
            'type': 'FeatureCollection',
            'features': features
        },
        period='PT1M',
        add_last_point=True,
        auto_play=False,
        loop=False,
        max_speed=1,
        loop_button=True,
        date_options='YYYY/MM/DD HH:mm:ss',
        time_slider_drag_update=True,
        duration='PT1M'
    ).add_to(m)
    
    m.save('index.html')

def init_folium():
    m = folium.Map(
        location=[28.607417678833008, 77.09991829736328], 
        zoom_start=11, 
        tiles="OpenStreetMap"
        #tiles='https://api.tiles.mapbox.com/v4/mapbox.streets/{z}/{x}/{y}.png?access_token=pk.eyJ1IjoidXBwZXJ3YWwiLCJhIjoiY2lxNmVvcGo4MDA3MGZ2bTY1b255OW14dSJ9.h18VG_xCO7yQXMajIqKyHg',
        #attr='Map data &copy; <a href="https://www.openstreetmap.org/">OpenStreetMap</a> contributors, <a href="https://creativecommons.org/licenses/by-sa/2.0/">CC-BY-SA</a>, Imagery © <a href="https://www.mapbox.com/">Mapbox</a>'
    )
    return m

if __name__ == '__main__':
    main(argv = sys.argv[1:])
