

class Point:

    def __init__(self, address, latitude, longitude):
        self.address = address
        self.latitude = latitude
        self.longitude = longitude

    @staticmethod
    def csvFieldnames():
        return ['Address', 'Latitude', 'Longitude']

    def toDict(self):
        return {'Address': self.address, 'Latitude': self.latitude, 'Longitude': self.longitude}

    @staticmethod
    def fromDict(dictionary):
        return Point(dictionary['Address'], float(dictionary['Latitude']), float(dictionary['Longitude']))
