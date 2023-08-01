import pymongo
from app.core.config import settings


def conn_mongodb():
    client = pymongo.MongoClient(
        f"mongodb://{settings.MONGODB_USERNAME}:{settings.MONGODB_PASSWORD}@{settings.MONGODB_SERVER}:{settings.MONGODB_PORT}/{settings.MONGODB_NAME}?authSource={settings.MONGODB_AUTHENTICATION_SOURCE}&readPreference=primary&ssl=false")
    return client


db_session = conn_mongodb()
