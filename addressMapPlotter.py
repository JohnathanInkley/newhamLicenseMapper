import csv

from gmplot import gmplot
from Point import Point

def loadAddressCoordinates(filePath):
    with open(filePath, 'r') as rawFile:
        points = []
        rows = csv.DictReader(rawFile)
        for row in rows:
            point = Point.fromDict(row)
            points.append(point)
        return points

def makeMap(points):  
    gmap = gmplot.GoogleMapPlotter(points[0].latitude, points[0].longitude, 13)

    for point in points:
        gmap.marker(point.latitude, point.longitude, title=point.address)

    gmap.draw("index.html")

def main():
    points = loadAddressCoordinates('data/newhamLicenses2023WithCoordinates.csv')
    makeMap(points)


if __name__ == '__main__':
    main()
