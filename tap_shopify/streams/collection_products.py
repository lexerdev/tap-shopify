import shopify

from tap_shopify.context import Context
from tap_shopify.streams.base import (Stream,
                                      RESULTS_PER_PAGE,
                                      shopify_error_handling,
                                      OutOfOrderIdsError)


class CollectionProducts(Stream):
    name = 'collection_products'
    replication_object = shopify.CustomCollection
    replication_key = 'updated_at'

    def get_objects(self):
        while True:
            page = self.get_page()
            for collection in page:
                for product in collection.products():
                    yield product
            if page.has_next_page():
                page = page.next_page()
            else:
                break

    @shopify_error_handling
    def get_page(self):
        return self.replication_object.find()

    def sync(self):
        for product in self.get_objects():
            yield product.to_dict()

Context.stream_objects['collection_products'] = CollectionProducts
