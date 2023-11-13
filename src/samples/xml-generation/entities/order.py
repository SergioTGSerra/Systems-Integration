import xml.etree.ElementTree as ET

class Order:

    def __init__(self, order_id, order_date, market, order_priority, ship_info):
        self._id = order_id
        self._order_date = order_date
        self._market = market
        self._order_priority = order_priority
        self._ship_info = ship_info

    def to_xml(self):
        order_element = ET.Element("Order")
        order_element.set("id", self._id)
        order_element.set("order_date", self._order_date)
        order_element.set("market", self._market)
        order_element.set("order_priority", self._order_priority)
        order_element.append(self._ship_info.to_xml())
        
        return order_element

    def get_id(self):
        return self._id

    def __str__(self):
        return f"Order ID: {self._id}, Order Date: {self._order_date}, Ship Date: {self._ship_date}"
