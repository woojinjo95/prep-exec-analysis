from dataclasses import dataclass
import os
from scripts.config.config import get_setting_with_env

@dataclass
class Settings:
    MONGODB_SERVER: str = get_setting_with_env("MONGODB_SERVER")
    MONGODB_NAME: str = get_setting_with_env("MONGODB_NAME")
    MONGODB_PORT: str = get_setting_with_env("MONGODB_PORT")
    MONGODB_USERNAME: str = get_setting_with_env("MONGODB_USERNAME")
    MONGODB_PASSWORD: str = get_setting_with_env("MONGODB_PASSWORD")
    MONGODB_AUTHENTICATION_SOURCE: str = get_setting_with_env("MONGODB_AUTHENTICATION_SOURCE")

