import os
import pymongo

MONGODB_USERNAME = os.getenv("MONGODB_USERNAME", "admin")
MONGODB_PASSWORD = os.getenv("MONGODB_PASSWORD", ".nextlab6318!")
MONGODB_SERVER = os.getenv("MONGODB_SERVER", "localhost")
MONGODB_PORT = os.getenv("MONGODB_PORT", 27017)
MONGODB_NAME = os.getenv("MONGODB_NAME", "prep-exec-analysis")
MONGODB_AUTHENTICATION_SOURCE = os.getenv("MONGODB_AUTHENTICATION_SOURCE", "admin")

MONGODB_COLLECTION_NAME = os.getenv("MONGODB_COLLECTION_NAME", "shell_log")


def conn_mongodb():
    client = pymongo.MongoClient(
        f"mongodb://{MONGODB_USERNAME}:{MONGODB_PASSWORD}@{MONGODB_SERVER}:{MONGODB_PORT}/{MONGODB_NAME}?authSource={MONGODB_AUTHENTICATION_SOURCE}&readPreference=primary&ssl=false")
    return client


def get_collection() -> pymongo.collection.Collection:
    db = MONGODB_NAME
    client = conn_mongodb()
    result_db = client[db]
    target_collection = result_db[MONGODB_COLLECTION_NAME]
    return target_collection
