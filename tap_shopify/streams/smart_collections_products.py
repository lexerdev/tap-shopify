import shopify

from tap_shopify.context import Context
from tap_shopify.streams.base import (Stream,
                                      RESULTS_PER_PAGE,
                                      shopify_error_handling,
                                      OutOfOrderIdsError)

class SmartCollectionsProducts(Stream):
    name = 'smart_collections_products'
    replication_object = shopify.SmartCollection
    replication_key = 'updated_at'


    def get_objects(self):
        'Paginate the return and add collection_id to returned product objects'
        page = self.replication_object.find()
        while True:
            for collection in page:
                collection_products_page = collection.products()
                while True:
                    for product in collection_products_page:
                        edit_product = product.to_dict()
                        edit_product["collection_id"] = collection.id
                        yield edit_product
                    if collection_products_page.has_next_page():
                        collection_products_page = collection_products_page.next_page()
                    else:
                        break
            if page.has_next_page():
                page = page.next_page()
            else:
                break

    def sync(self):
        for product in self.get_objects():
            yield product

Context.stream_objects['smart_collections_products'] = SmartCollectionsProducts