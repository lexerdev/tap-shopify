import shopify

from tap_shopify.streams.base import Stream
from tap_shopify.context import Context


class Shop(Stream):
    name = 'shop'
    replication_object = shopify.Shop

Context.stream_objects['shop'] = Shop
