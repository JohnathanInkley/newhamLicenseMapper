import csv
import re

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

    gmap.draw("oldIndex.html")

def postProcessHTML():
    with open('oldIndex.html', 'r') as file:
        html_content = file.read()

    initialize_pattern = re.compile(
        r'function\s+initialize\s*\(\)\s*{([\s\S]*?)}\s*</script>', re.DOTALL
    )
    initialize_function_match = initialize_pattern.search(html_content)

    if initialize_function_match:
        initialize_function_body = initialize_function_match.group(1)

        map_and_icon_setup_pattern = re.compile(
            r'var map = new google\.maps\.Map\(.*?\}\);\s*var marker_icon_FF0000 = \{.*?\};',
            re.DOTALL
        )
        map_and_icon_setup_match = map_and_icon_setup_pattern.search(initialize_function_body)
        
        if map_and_icon_setup_match:
            map_and_icon_setup_code = map_and_icon_setup_match.group(0)

            markers = []
            marker_count = 0
            originalMarkers = initialize_function_body.split('new google.maps.Marker')[1:]
            for marker_data in originalMarkers:
                if '});' in marker_data:
                    marker_content = marker_data.split('});')[0] + '});'
                    marker_code = f'var marker_{marker_count} = new google.maps.Marker{marker_content}\nallMarkers.push(marker_{marker_count});'
                    markers.append(marker_code)
                    marker_count += 1
                   
            markers_code = "\n".join(markers)
            all_markers_array = "var allMarkers = [];\n"

            click_functionality_code = """
            allMarkers.forEach(function(marker) {
                var infoWindow = new google.maps.InfoWindow({
                    content: marker.getTitle()
                });
                marker.addListener('click', function() {
                    infoWindow.open(marker.getMap(), marker);
                });
            });
            """

            modified_initialize_function = f"function initialize() {{\n{map_and_icon_setup_code}\n{all_markers_array}\n{markers_code}\n{click_functionality_code}\n}}\n</script>"
            html_content = initialize_pattern.sub(modified_initialize_function, html_content)

            with open('oldIndex.html', 'w') as file:
                file.write(html_content)
            print("Markers successfully modified and click functionality added.")
        else:
            print("Map and marker icon setup not found in the initialize function.")
    else:
        print("Initialize function not found in the HTML.")
    
def main():
    points = loadAddressCoordinates('data/newhamLicenses2023WithCoordinates.csv')
    makeMap(points)
    postProcessHTML()

if __name__ == '__main__':
    main()
