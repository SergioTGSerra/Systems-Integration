import xml.etree.ElementTree as ET

class State:

    def __init__(self, name, coordinates):
        State.counter += 1
        self._id = State.counter
        self._name = name
        self._lat = coordinates[0]
        self._log = coordinates[1]

    def to_xml(self):
        el = ET.Element("State")
        el.set("id", str(self._id))
        el.set("name", self._name)
        el.set("lat", self._lat)
        el.set("lon", self._log)

        return el

    def get_id(self):
        return self._id

    def __str__(self):
        return f"name: {self._name}, id: {self._id}"

State.counter = 0
