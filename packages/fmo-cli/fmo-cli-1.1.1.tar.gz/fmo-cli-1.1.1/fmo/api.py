import requests
import pandas
import datetime
import geojson

FMO_API_URL = "https://api.findmyoyster.com/v1"


def any_to_unix_time(any):
    if isinstance(any, datetime.datetime):
        return int(datetime.datetime.timestamp(any))

    if isinstance(any, str):
        return int(datetime.datetime.fromisoformat(any).timestamp())

    if isinstance(any, int):
        return any

    raise Exception("Failed to convert timestamp")


def login_to_get_token(url, farm, user, password) -> str:
    response = requests.post(
        f"{url}/sessions/login",
        json={"farm": farm, "username": user, "password": password},
    )
    if not response.ok:
        raise Exception(response.reason)

    return response.json()["referenceToken"]


class GPSPath:
    def __init__(self, coords):
        """A GPSPath is a sequence of time referenced GPS coordinates

        Args:
            coords (List): [(time, lat, lng), (time, lat, lng), ...]
        """
        self._coords = coords

    def fmo_path_json(self):
        return {
            "points": [
                {"lat": c[1], "lng": c[2], "timestamp": any_to_unix_time(c[0])}
                for c in self._coords
            ]
        }

    def dataframe(self):
        return pandas.DataFrame(self._coords, columns=["Time", "Latitude", "Longitude"])
    
    def geojson(self):
        line_coordinates = [(lng, lat) for _, lat, lng in self._coords]
        line = geojson.LineString(line_coordinates)
        feature = geojson.Feature(geometry=line)
        feature_collection = geojson.FeatureCollection([feature])
        return feature_collection


class FMO:
    def __init__(self, token, url="api.findmyoyster.com/v1"):
        self._url = url
        self._token = token

    def upload_path(self, path: GPSPath):
        response = requests.post(
            f"{self._url}/paths",
            json=path.fmo_path_json(),
            headers={"Authorization": f"Bearer {self._token}"},
        )
        if not response.ok:
            print(response.text)
            raise Exception(response.reason)

    def list_water_leases(self):
        response = requests.get(
            f"{self._url}/leases",
            headers={"Authorization": f"Bearer {self._token}"},
        )
        if not response.ok:
            print(response.text)
            raise Exception(response.reason)

        return response.json()["data"]
