class GeoPoint:
    def __init__(self, latitude, longitude):
        self.latitude = latitude
        self.longitude = longitude

    def __str__(self):
        return '{Lat: ' + str(self.latitude) + ', Long: ' + str(self.longitude) + '}'

