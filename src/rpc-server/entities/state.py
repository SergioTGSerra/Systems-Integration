import json
import xml.etree.ElementTree as ET
import urllib.request

class State:

    def __init__(self, name,):
        State.counter += 1
        self._id = State.counter
        self._name = name

    def to_xml(self):
        el = ET.Element("State")
        el.set("id", str(self._id))
        el.set("name", self._name)
        encoded_state = urllib.parse.quote(self._name)
        url = f'https://nominatim.openstreetmap.org/search?format=json&limit=1&state={encoded_state}'
        with urllib.request.urlopen(url) as response:
            data = json.loads(response.read())
            if data:
                el.set("lat", data[0]['lat'])
                el.set("lon", data[0]['lon'])

        return el

    def get_id(self):
        return self._id

    def __str__(self):
        return f"name: {self._name}, id: {self._id}"

State.counter = 0
