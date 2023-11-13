import xml.etree.ElementTree as ET


class Customer:

    def __init__(self, customer_id, customer_name, segment, address):
        self._id = customer_id
        self._name = customer_name
        self._segment = segment
        self._address = address

    def to_xml(self):
        el = ET.Element("Customer")
        el.set("id", self._id)
        el.set("name", self._name)
        el.set("segment_ref", str(self._segment.get_id()))
        el.append(self._address.to_xml())
        return el

    def __str__(self):
        return f"{self._name}, age:{self._age}, country:{self._country}" 


Customer.count = 0