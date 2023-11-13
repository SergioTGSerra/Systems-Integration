import xml.etree.ElementTree as ET


class Product:

    def __init__(self, product_id, name, category_id, sales, quantity, discount, profit):
        self._id = product_id
        self._name = name
        self._category_id = category_id
        self._sales = sales
        self._quantity = quantity
        self._discount = discount
        self._profit = profit

    def to_xml(self):
        el = ET.Element("Product")
        el.set("id", str(self._id))
        el.set("name", self._name)
        el.set("category_id", str(self._category_id))
        el.set("sales", str(self._sales))
        el.set("quantity", str(self._quantity))
        el.set("discount", str(self._discount))
        el.set("profit", str(self._profit))
        return el

    def get_id(self):
        return self._id

    def __str__(self):
        return f"name: {self._name}, id:{self._id}"


Product.counter = 0
