import requests
import urllib.parse
import csv
import time

from Point import Point

def loadAddresses(filename):
    addresses = set()
    with open(filename, 'r') as addressesRawFile:
        addressCsvList = csv.DictReader(addressesRawFile)
        for row in addressCsvList:
            address = row['Address']
            addresses.add(address)
    return addresses

headers = {
    'User-Agent': 'My User Agent 1.0',
    'From': 'juk92@gmail.com'
}


def getPointFromAddress(address):
    url = 'https://nominatim.openstreetmap.org/search?q=' + urllib.parse.quote(address) +'&format=json'
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    latitude = response.json()[0]["lat"]
    longitude = response.json()[0]["lon"]
    return Point(address, latitude, longitude)
            
def main():
    filePath = 'data/newhamLicenses2023.csv'
    outputFilePath = filePath.replace('.csv','WithCoordinates.csv')

    addressesToSearch = loadAddresses(filePath)
    addressesAlreadySearched = loadAddresses(outputFilePath)
    unsearchedAddresses = [x for x in addressesToSearch if x not in addressesAlreadySearched]
    
    with open(outputFilePath, 'a') as outputFile:
        writer = csv.DictWriter(outputFile, fieldnames=Point.csvFieldnames())
        
        for address in unsearchedAddresses:
            print('Searching: ' + address)
            try:
                point = getPointFromAddress(address)
                writer.writerow(point.toDict())
                outputFile.flush()
                print('Found coordinates')
            except Exception as e:
                print('Couldn\'t search for address: ' + address + ' as ' + repr(e))
            time.sleep(1)
            

if __name__ == '__main__':
    main()
