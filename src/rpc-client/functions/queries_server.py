from functions.connect_rpc import connect_rpc

server = connect_rpc().server

def get_orders_order_by_priority(file_name):
    return server.get_orders_order_by_priority(file_name)

def get_orders_by_market_order_by_shipping_cost(market_id, file_name):
    return server.get_orders_by_market_order_by_shipping_cost(market_id, file_name)

def retrieve_customer_information_with_address_details(file_name):
    return server.retrieve_customer_information_with_address_details(file_name)

def count_the_number_of_customers_by_segment_server(file_name):
    return server.count_the_number_of_customers_by_segment_server(file_name)

def get_order_and_customer_details_with_geographic_information(file_name):
    return server.get_order_and_customer_details_with_geographic_information(file_name)