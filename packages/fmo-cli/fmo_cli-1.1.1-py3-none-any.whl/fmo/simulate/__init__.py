from fmo.simulate.circle import Circle
import json
from random import randrange


class PathCreator():
    """
        Usage instructions
        given a min max xy area a path can be generated then translated over to the area defined by the gps coordinates
        first initialize the class with the defined areas
        then a path can be created in the arbitrary xy coords 
        you can use PathCreator.circle.outputCircles() to view the path given in xy coords
        finally gps_to_geojson outputs the coords in the gps frame in gejson format

    """
    def __init__(self,xy_min = (-10,-1), xy_max =(5,10), gps_min=(-76.47785558589752, 38.908054359143165), gps_max=(-76.4824111255889, 38.913442426008885)):
        self.xy_min = xy_min
        self.xy_max = xy_max
        self.gps_min = gps_min
        self.gps_max = gps_max
    def create_path(self, random = True, choosenpoints = [],center=(0, 0),x_stretch = 2, y_stretch = 1, circle_number = 25, noise = 0.001):
        """
        Choosenpoints override random create path creates a path using the circle module
        """
        if choosenpoints and len(choosenpoints) == 4:
            self.circle = Circle(1,pathpoints=choosenpoints,center=center,x_stretch=x_stretch,y_stretch=y_stretch,circle_number=circle_number)
        elif random:
            points = [(randrange(self.xy_min[0]+((abs(self.xy_min[0])+abs(self.xy_max[0]))//4*(1+i)),self.xy_max[0]//(4-i)),randrange(self.xy_min[1],self.xy_max[1])) for i in range(0,4)]
            self.circle = Circle(1,pathpoints=points,center=center,x_stretch=x_stretch,y_stretch=y_stretch,circle_number=circle_number)
        else:
            self.circle = Circle(1,center=center,x_stretch=x_stretch,y_stretch=y_stretch,circle_number=circle_number)
        self.points = self.circle.outputCircles(fidelity=500, noise=noise)

        return self.points
    
    def xy_to_gps(self, xy):
        x, y = xy
        x_min, y_min = self.xy_min
        x_max, y_max = self.xy_max
        lat_min, lon_min = self.gps_min
        lat_max, lon_max = self.gps_max
        
        # Compute the fractional distances of the x and y coordinates within the rectangle
        x_frac = (x - x_min) / (x_max - x_min)
        y_frac = (y - y_min) / (y_max - y_min)
        
        # Compute the corresponding GPS coordinates using linear interpolation
        lat = lat_min + (lat_max - lat_min) * y_frac
        lon = lon_min + (lon_max - lon_min) * x_frac

        return (lon, lat)
    def gps_to_geojson(self, coords):
        coordinates = []
        for point in coords:
            lon, lat = self.xy_to_gps(point)
            coordinates.append([lat, lon])
        feature = {
            "type": "Feature",
            "geometry": {
                "type": "LineString",
                "coordinates": coordinates
            },
            "properties": {
                "id": 0
            }
        }
        feature_collection = {
            "type": "FeatureCollection",
            "features": [feature]
        }
        return json.dumps(feature_collection)