from functions.connect_rpc import connect_rpc

server = connect_rpc().server

def get_orders_order_by_priority():
    return server.get_orders_order_by_priority()

def get_orders_by_market_order_by_shipping_cost(market_id):
    return server.get_orders_by_market_order_by_shipping_cost(market_id)

def retrieve_customer_information_with_address_details():
    return server.retrieve_customer_information_with_address_details()

def count_the_number_of_customers_by_segment_server():
    return server.count_the_number_of_customers_by_segment_server()

def get_order_and_customer_details_with_geographic_information():
    return server.get_order_and_customer_details_with_geographic_information()