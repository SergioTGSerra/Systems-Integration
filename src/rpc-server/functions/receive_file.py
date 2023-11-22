from functions.csv_to_xml_converter import CSVtoXMLConverter
import psycopg2

def receive_file(binary_data):
    with open('/data/Global_Superstore2.csv', 'wb') as handle:
        handle.write(binary_data.data)
    converter = CSVtoXMLConverter("/data/Global_Superstore2.csv")
    data = converter.to_xml_str()

    try:
        print("Connecting to database")
        connection = psycopg2.connect(user="is",
                                  password="is",
                                  host="is-db",
                                  port="5432",
                                  database="is")

        cursor = connection.cursor()
        cursor.execute("INSERT INTO imported_documents (file_name, xml) VALUES (%s, %s)", ("teste", data,))

        connection.commit()

    except (Exception, psycopg2.Error) as error:
        print("Failed to fetch data", error)

    finally:
        if connection:
            cursor.close()
            connection.close()

    return "ok"
    
