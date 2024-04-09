import shopify
from tap_shopify.streams.base import (Stream, shopify_error_handling)
from tap_shopify.context import Context

class Products(Stream):
    name = 'products'
    replication_object = shopify.Product
    # Added decorator over functions of shopify SDK
    replication_object.find = shopify_error_handling(replication_object.find)

    def get_product_data(self):
        # set timeout
        self.replication_object.set_timeout(self.request_timeout)
        product_page = self.replication_object.find()
        yield from product_page

        while product_page.has_next_page():
            product_page = product_page.next_page()
            yield from product_page

    def sync(self):
        for product in self.get_product_data():
            yield product.to_dict()

Context.stream_objects['products'] = Products
