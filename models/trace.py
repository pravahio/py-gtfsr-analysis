from models.point import GeoPoint
from collections import OrderedDict 

class GeoTrace:

    def __init__(self):
        self.timestamp_trace = OrderedDict()

    def __str__(self):
        res = ''
        for k, v in self.timestamp_trace.items():
            res += 'Timestamp: ' + str(k) + ', Point: ' + str(v) + '\n'
        return res

    def add_point(self, timestamp, geoPoint = None, latitude = None, longitude = None):
        if geoPoint != None and isinstance(geoPoint, GeoPoint):
            self.timestamp_trace[timestamp] = geoPoint
            return
        if latitude == None or longitude == None:
            print('Lat/Long should not be None')
            return
        self.timestamp_trace[timestamp] = GeoPoint(latitude, longitude)
    
    def items(self):
        for k, v in self.timestamp_trace.items():
            yield k, v
