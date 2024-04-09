import shopify

from tap_shopify.streams.base import Stream
from tap_shopify.context import Context


class Products(Stream):
    name = 'products'
    replication_object = shopify.Product
    replication_method = "FULL_TABLE"

Context.stream_objects['products'] = Products
