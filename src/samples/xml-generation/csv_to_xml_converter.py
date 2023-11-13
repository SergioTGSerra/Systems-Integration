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


class CSVtoXMLConverter:

    def __init__(self, path):
        self._reader = CSVReader(path)

    def to_xml(self):
        
        # read countries
        countries = self._reader.read_entities(
            attr="Country",
            builder=lambda row: Country(row["Country"])
        )

        # read segments
        segments = self._reader.read_entities(
            attr="Segment",
            builder=lambda row: Segment(row["Segment"])
        )

        # read orders
        orders = self._reader.read_entities(
            attr="Order ID",
            builder=lambda row: Order(
                order_id=row["Order ID"],
                order_date=row["Order Date"],
                market=row["Market"],
                order_priority=row["Order Priority"],
                ship_info=Ship(
                    ship_date=row["Ship Date"],
                    ship_mode=row["Ship Mode"],
                    shiping_cost=row["Shipping Cost"]
                )
            )
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


        # generate the final xml
        root_el = ET.Element("Store")

        orders_el = ET.Element("Orders")
        for order in orders.values():
            orders_el.append(order.to_xml())

        customers_el = ET.Element("Customers")
        for customer in customers.values():
            customers_el.append(customer.to_xml())

        segments_el = ET.Element("Segments")
        for segment in segments.values():
            segments_el.append(segment.to_xml())

        countries_el = ET.Element("Countries")
        for country in countries.values():
            countries_el.append(country.to_xml())

        root_el.append(orders_el)
        root_el.append(customers_el)
        root_el.append(segments_el)
        root_el.append(countries_el)

        return root_el

    def to_xml_str(self):
        xml_str = ET.tostring(self.to_xml(), encoding='utf8', method='xml').decode()
        dom = md.parseString(xml_str)
        return dom.toprettyxml()

