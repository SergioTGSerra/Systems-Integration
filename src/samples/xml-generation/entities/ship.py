import xml.etree.ElementTree as ET


class Ship:

    def __init__(self, ship_date, ship_mode, shiping_cost):
        self._ship_date = ship_date
        self._ship_mode = ship_mode
        self._shiping_cost = shiping_cost

    def to_xml(self):
        el = ET.Element("Ship")
        el.set("ship_date", self._ship_date)
        el.set("ship_mode", self._ship_mode)
        el.set("shiping_cost", self._shiping_cost)
        
        return el

    def __str__(self):
        return f"name: {self._name}, id:{self._id}"