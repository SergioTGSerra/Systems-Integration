from csv_to_xml_converter import CSVtoXMLConverter

if __name__ == "__main__":
    converter = CSVtoXMLConverter("/data/Global_Superstore2.csv")
    data = converter.to_xml_str()
    print(data)

    #export to xml file
    with open("/data/Global_Superstore2.xml", "w") as file:
        file.write(data)
