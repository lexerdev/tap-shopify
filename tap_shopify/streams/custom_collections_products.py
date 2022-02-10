import shopify

from tap_shopify.context import Context
from tap_shopify.streams.base import (Stream,
                                      RESULTS_PER_PAGE,
                                      shopify_error_handling,
                                      OutOfOrderIdsError)


class CustomCollectionsProducts(Stream):
    name = 'custom_collections_products'
    replication_object = shopify.CustomCollection
    replication_key = 'updated_at'

    @shopify_error_handling
    def get_collection_products(self, collection):
        return collection.products()

    @shopify_error_handling
    def get_custom_collections_products(self):
        # set timeout
        self.replication_object.set_timeout(self.request_timeout)
        return self.replication_object.find()

    def get_objects(self):
        'Paginate the return and add collection_id to returned product objects'
        page = self.get_custom_collections_products()
        while True:
            for collection in page:
                collection_products_page = self.get_collection_products(collection)
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

Context.stream_objects['custom_collections_products'] = CustomCollectionsProducts