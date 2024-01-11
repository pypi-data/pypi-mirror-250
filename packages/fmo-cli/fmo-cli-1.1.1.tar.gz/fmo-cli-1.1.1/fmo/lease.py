
class Lease:
    def __init__(self, lease_data):
        self._data = lease_data

    def center(self):
        coords = [(c['lat'], c['lng']) for c in self._data["coords"]]
        return coords[0]

    def geojson_data(self):
        coords = [(c['lng'], c['lat']) for c in self._data["coords"]]
        geojson_data = {
            "type": "Feature",
            "properties": {},
            "geometry": {
                "type": "Polygon",
                "coordinates": [coords]
            }
        }

        return geojson_data