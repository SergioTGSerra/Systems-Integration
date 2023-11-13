import xml.etree.ElementTree as ET


class Category:

    def __init__(self, name, father_category):
        Category.counter += 1
        self._id = Category.counter
        self._category_id = father_category
        self._name = name
        self._products = []

    def to_xml(self):
        el = ET.Element("Category")
        el.set("id", str(self._id))
        el.set("name", self._name)
        el.set("category_id", str(self._category_id))
        
        for product in self._products:
            product_el = ET.Element("Product")
            product_el.text = product
            el.append(product_el)

        return el

    def get_id(self):
        return self._id

    def __str__(self):
        return f"name: {self._name}, id:{self._id}"


Category.counter = 0
