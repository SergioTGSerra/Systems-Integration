import csv
import xml.dom.minidom as md
import xml.etree.ElementTree as ET

from csv_reader import CSVReader
from entities.order import Order
from entities.ship import Ship
from entities.customer import Customer
from entities.address import Address
from entities.segment import Segment
from entities.country import Country
from entities.market import Market
from entities.product import Product
from entities.category import Category


class CSVtoXMLConverter:

    def __init__(self, path):
        self._reader = CSVReader(path)

    def to_xml(self):
        
        # read countries
        countries = self._reader.read_entities(
            attr="Country",
            builder=lambda row: Country(row["Country"])
        )

        # read markets
        markets = self._reader.read_entities(
            attr="Market",
            builder=lambda row: Market(
                name=row["Market"],
                region=row["Region"]
            )
        ) 

        # Read categories
        categories = self._reader.read_entities(
            attr="Category",
            builder=lambda row: Category(
                name=row["Category"]
            )
        )

        # Read subcategories
        subcategories = self._reader.read_entities(
            attr="Sub-Category",
            builder=lambda row: Category(
                name=row["Sub-Category"],
                parent_category=categories[row["Category"]] if row["Category"] in categories else None
            )
        )

        # read segments
        segments = self._reader.read_entities(
            attr="Segment",
            builder=lambda row: Segment(row["Segment"])
        )

        # read customers
        customers = self._reader.read_entities(
            attr="Customer ID",
            builder=lambda row: Customer(
                customer_id=row["Customer ID"],
                customer_name=row["Customer Name"],
                segment=segments[row["Segment"]],
                address=Address(
                    city=row["City"],
                    country=countries[row["Country"]],
                    postal_code=row["Postal Code"],
                    state=row["State"]
                )
            )
        )

        # read orders
        orders = self._reader.read_entities(
            attr="Order ID",
            builder=lambda row: Order(
                order_id=row["Order ID"],
                order_date=row["Order Date"],
                order_priority=row["Order Priority"],
                customer=customers[row["Customer ID"]],
                market=markets[row["Market"]],
                ship_info=Ship(
                    ship_date=row["Ship Date"],
                    ship_mode=row["Ship Mode"],
                    shiping_cost=row["Shipping Cost"]
                )
            )
        )

        def add_product_to_orders(product, row):
            # read csv and associate products to orders
            with open(self._reader._path, 'r') as file:
                reader = csv.DictReader(file, delimiter=',')
                for row in reader:
                    if row["Product ID"] == product.get_id():
                        orders[row["Order ID"]].add_product(product)

        # read products
        products = self._reader.read_entities(
            attr="Product ID",
            builder=lambda row: Product(
                product_id=row["Product ID"],
                product_name=row["Product Name"],
                product_category=subcategories[row["Sub-Category"]],
                sales=row["Sales"],
                quantity=row["Quantity"],
                discount=row["Discount"],
                profit=row["Profit"]
            ),
            after_create=add_product_to_orders
        )

        # generate the final xml
        root_el = ET.Element("Store")

        orders_el = ET.Element("Orders")
        for order in orders.values():
            orders_el.append(order.to_xml())

        markets_el = ET.Element("Markets")
        for market in markets.values():
            markets_el.append(market.to_xml())

        customers_el = ET.Element("Customers")
        for customer in customers.values():
            customers_el.append(customer.to_xml())

        segments_el = ET.Element("Segments")
        for segment in segments.values():
            segments_el.append(segment.to_xml())

        countries_el = ET.Element("Countries")
        for country in countries.values():
            countries_el.append(country.to_xml())

        products_el = ET.Element("Products")
        for product in products.values():
            products_el.append(product.to_xml())

        categories_el = ET.Element("Categories")
        for category in categories.values():
            categories_el.append(category.to_xml())

        for subcategory in subcategories.values():
            categories_el.append(subcategory.to_xml())
        

        root_el.append(orders_el)
        root_el.append(products_el)
        root_el.append(markets_el)
        root_el.append(customers_el)
        root_el.append(segments_el)
        root_el.append(countries_el)
        root_el.append(categories_el)

        return root_el

    def to_xml_str(self):
        xml_str = ET.tostring(self.to_xml(), encoding='utf8', method='xml').decode()
        dom = md.parseString(xml_str)
        return dom.toprettyxml()

