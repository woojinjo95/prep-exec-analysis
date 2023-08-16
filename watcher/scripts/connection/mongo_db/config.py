from dataclasses import dataclass
import os


@dataclass
class Settings:
    MONGODB_SERVER: str = os.getenv("MONGODB_SERVER")
    MONGODB_NAME: str = os.getenv("MONGODB_NAME")
    MONGODB_PORT: str = os.getenv("MONGODB_PORT")
    MONGODB_USERNAME: str = os.getenv("MONGODB_USERNAME")
    MONGODB_PASSWORD: str = os.getenv("MONGODB_PASSWORD")
    MONGODB_AUTHENTICATION_SOURCE: str = os.getenv("MONGODB_AUTHENTICATION_SOURCE")
