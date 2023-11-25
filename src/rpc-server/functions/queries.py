from lxml import etree
from functions.db_connection import DBConnection

def get_orders_order_by_priority():
    db = DBConnection()
    db.connect()

    file_name = "Global_Superstore2.csv"

    xquery = """
        SELECT
            unnest(xpath('//Order'::text, xml))::xml AS order_xml,
            unnest(xpath('//Order/@priority'::text, xml))::text AS order_priority
        FROM
            imported_documents
        WHERE
            NOT is_deleted
            AND file_name = %s
        ORDER BY
            order_priority;
    """

    result = db.execute_query_with_return(xquery, (file_name,))

    if result:
        root = etree.Element("Orders")
        for order in result:
            root.append(etree.fromstring(order[0]))
        xml = etree.tostring(root, pretty_print=True).decode("utf-8")

        file_exists = db.execute_query_with_return("SELECT file_name FROM queries WHERE file_name = %s", ("file_get_orders_by_priority",))

        if file_exists:
            db.disconnect()
            return xml

        db.execute_query("INSERT INTO queries (query_type, file_name, xml) VALUES (1, %s, %s)", ("file_get_orders_by_priority", xml))

        db.disconnect()

        return xml
    else:
        return "No results found"
 
def get_orders_by_market_order_by_shipping_cost(market_id):
    db = DBConnection()
    db.connect()

    file_name = "Global_Superstore2.csv"

    xquery = f"""
        SELECT
            UNNEST(xpath('//Order[@market_ref="{market_id}"]', xml)) AS order_xml,
            UNNEST(xpath('//Order[@market_ref="{market_id}"]/Shipping/@cost', xml)) AS ship_cost
        FROM
            imported_documents
        WHERE
            NOT is_deleted
            AND file_name = %s
        ORDER BY
            (xpath('//Order[@market_ref="{market_id}"]/Shipping/@cost', xml))[1]::text::float DESC;
    """

    result = db.execute_query_with_return(xquery, (file_name,))

    if result:
        root = etree.Element("Orders")
        for order in result:
            root.append(etree.fromstring(order[0]))
        xml = etree.tostring(root, pretty_print=True).decode("utf-8")

        xml_result = etree.tostring(root, pretty_print=True).decode("utf-8")

        file_exists = db.execute_query_with_return("SELECT file_name FROM queries WHERE file_name = %s", ("file_get_orders_by_market_order_by_shipping_cost",))

        if file_exists:
            db.disconnect()
            return xml_result

        db.execute_query("INSERT INTO queries (query_type, file_name, xml) VALUES (2, %s, %s)", ("file_get_orders_by_market_order_by_shipping_cost", xml_result))

        db.disconnect()

        return xml_result
    else:
        return "No results found"

def retrieve_customer_information_with_address_details():
    db = DBConnection()
    db.connect()

    file_name = "Global_Superstore2.csv"

    xquery = """
            SELECT
                c.customer_id,
                c.customer_name,
                c.postal_code,
                c.city,
                co.country_name,
                s.state_name,
                s.latitude,
                s.longitude
            FROM (
                SELECT
                    unnest(xpath('//Customers/Customer/@id', xml))::text AS customer_id,
                    unnest(xpath('//Customers/Customer/@name', xml))::text AS customer_name,
                    unnest(xpath('//Customers/Customer/Address/@postal_code', xml))::text AS postal_code,
                    unnest(xpath('//Customers/Customer/Address/@city', xml))::text AS city,
                    unnest(xpath('//Customers/Customer/Address/@country_ref', xml))::text AS country_ref,
                    unnest(xpath('//Customers/Customer/Address/@state_ref', xml))::text AS state_ref
                FROM
                    imported_documents
                WHERE
                    NOT is_deleted
                    AND file_name = %s
            ) c
            JOIN (
                SELECT
                    unnest(xpath('//Countries/Country/@id', xml))::text AS country_id,
                    unnest(xpath('//Countries/Country/@name', xml))::text AS country_name
                FROM
                    imported_documents
                WHERE
                    NOT is_deleted
                    AND file_name = %s
            ) co ON c.country_ref = co.country_id
            JOIN (
                SELECT
                    unnest(xpath('//States/State/@id', xml))::text AS state_id,
                    unnest(xpath('//States/State/@name', xml))::text AS state_name,
                    unnest(xpath('//States/State/@lat', xml))::text::double precision AS latitude,
                    unnest(xpath('//States/State/@lon', xml))::text::double precision AS longitude
                FROM
                    imported_documents
                WHERE
                    NOT is_deleted
                    AND file_name = %s
            ) s ON c.state_ref = s.state_id
            GROUP BY
                c.customer_id, c.customer_name, c.postal_code, c.city, co.country_name, s.state_name, s.latitude, s.longitude
            ORDER BY
                c.customer_name;
    """

    result = db.execute_query_with_return(xquery, (file_name, file_name, file_name,))

    if result:
        root = etree.Element("Customers")
        for customer in result:
            customer_element = etree.SubElement(
                root,
                "Customer_Address",
                id=str(customer[0]),
                name=customer[1],
                postal_code=customer[2],
                city=customer[3],
                country_name=customer[4],
                state_name=customer[5],
                latitude=str(customer[6]),
                longitude=str(customer[7]),
            )

        xml_result = etree.tostring(root, pretty_print=True).decode("utf-8")

        file_exists = db.execute_query_with_return("SELECT file_name FROM queries WHERE file_name = %s", ("file_retrieve_customer_information_with_address_details",))

        if file_exists:
            db.disconnect()
            return xml_result

        db.execute_query("INSERT INTO queries (query_type, file_name, xml) VALUES (3, %s, %s)", ("file_retrieve_customer_information_with_address_details", xml_result))

        db.disconnect()

        return xml_result

def count_the_number_of_customers_by_segment_server():
    db = DBConnection()
    db.connect()

    file_name = "Global_Superstore2.csv"

    xquery = """
            SELECT
                segment_name,
                COUNT(*) AS customer_count
            FROM (
                SELECT
                    unnest(xpath('/Store/Customers/Customer/@name', xml))::text AS customer_name,
                    unnest(xpath('/Store/Customers/Customer/@segment_ref', xml))::text AS segment_id
                FROM imported_documents
                WHERE
                    NOT is_deleted
                    AND file_name = %s
            ) AS customer_xml
            JOIN (
                SELECT
                    unnest(xpath('/Store/Segments/Segment/@id', xml))::text AS segment_id,
                    unnest(xpath('/Store/Segments/Segment/@name', xml))::text AS segment_name
                FROM imported_documents
                WHERE
                    NOT is_deleted
                    AND file_name = %s
            ) AS segment_xml
            ON customer_xml.segment_id = segment_xml.segment_id
            GROUP BY segment_name; 
    """

    result = db.execute_query_with_return(xquery, (file_name, file_name,))

    if result:
        root = etree.Element("Segments")
        for segment in result:
            segment_element = etree.SubElement(
                root,
                "Segment",
                name=segment[0],
                number_of_customers=str(segment[1]),
            )

        xml_result = etree.tostring(root, pretty_print=True).decode("utf-8")

        file_exists = db.execute_query_with_return("SELECT file_name FROM queries WHERE file_name = %s", ("file_count_the_number_of_customers_by_segment_server",))

        if file_exists:
            db.disconnect()
            return xml_result

        db.execute_query("INSERT INTO queries (query_type, file_name, xml) VALUES (4, %s, %s)", ("file_count_the_number_of_customers_by_segment_server", xml_result))

        db.disconnect()

        return xml_result
    else:
        return "No results found"

def get_order_and_customer_details_with_geographic_information():
    db = DBConnection()
    db.connect()

    file_name = "Global_Superstore2.csv"

    xquery = """
            SELECT
                o.order_id,
                o.order_date,
                o.shipped_date,
                o.ship_mode,
                c.customer_name,
                c.postal_code,
                s.state_name,
                s.latitude,
                s.longitude
            FROM (
                SELECT
                    unnest(xpath('//Orders/Order/@id', xml))::text AS order_id,
                    unnest(xpath('//Orders/Order/@date', xml))::text AS order_date,
                    unnest(xpath('//Orders/Order/Shipping/@date', xml))::text AS shipped_date,
                    unnest(xpath('//Orders/Order/Shipping/@mode', xml))::text AS ship_mode,
                    unnest(xpath('//Orders/Order/@customer_ref', xml))::text AS customer_ref
                FROM
                    imported_documents
                WHERE
                    NOT is_deleted
                    AND file_name = %s
            ) o
            JOIN (    
                SELECT
                    unnest(xpath('//Customers/Customer/@id', xml))::text AS customer_id,
                    unnest(xpath('//Customers/Customer/@name', xml))::text AS customer_name,
                    unnest(xpath('//Customers/Customer/Address/@postal_code', xml))::text AS postal_code,
                    unnest(xpath('//Customers/Customer/Address/@city', xml))::text AS city,
                    unnest(xpath('//Customers/Customer/Address/@state_ref', xml))::text AS state_ref
                FROM
                    imported_documents
                WHERE
                    NOT is_deleted
                    AND file_name = %s
            ) c ON o.customer_ref = c.customer_id
            JOIN (
                SELECT
                    unnest(xpath('//States/State/@id', xml))::text AS state_id,
                    unnest(xpath('//States/State/@name', xml))::text AS state_name,
                    unnest(xpath('//States/State/@lat', xml))::text::double precision AS latitude,
                    unnest(xpath('//States/State/@lon', xml))::text::double precision AS longitude
                FROM
                    imported_documents
                WHERE
                    NOT is_deleted
                    AND file_name = %s
            ) s ON c.state_ref = s.state_id
            GROUP BY
                o.order_id, o.order_date, o.shipped_date, o.ship_mode, c.customer_name, c.postal_code, c.city, s.state_name, s.latitude, s.longitude
            """
    
    result = db.execute_query_with_return(xquery, (file_name, file_name, file_name,))

    if result:
        root = etree.Element("Orders")
        for order in result:
            order_element = etree.SubElement(
                root,
                "Order",
                id=str(order[0]),
                order_date=order[1],
                shipped_date=order[2],
                ship_mode=order[3],
                customer_name=order[4],
                postal_code=order[5],
                state_name=order[6],
                latitude=str(order[7]),
                longitude=str(order[8]),
            )

        xml_result = etree.tostring(root, pretty_print=True).decode("utf-8")

        file_exists = db.execute_query_with_return("SELECT file_name FROM queries WHERE file_name = %s", ("file_get_order_and_customer_details_with_geographic_information",))

        if file_exists:
            db.disconnect()
            return xml_result

        db.execute_query("INSERT INTO queries (query_type, file_name, xml) VALUES (5, %s, %s)", ("file_get_order_and_customer_details_with_geographic_information", xml_result))

        db.disconnect()

        return xml_result
    
    else:
        return "No results found"

            

