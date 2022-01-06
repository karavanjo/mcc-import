import logging

logger = logging.getLogger("mcc_import")

BULK_SIZE = 1000


def bulk_observations_insert(items, collection, all=False):
    if len(items) > 0 and (len(items) % BULK_SIZE == 0 or all):
        collection.insert_many(items)
        logger.info(f"{len(items)} observations imported")
        items.clear()
