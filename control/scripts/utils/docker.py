import os
import logging

logger = logging.Logger("connection")

def is_running_in_docker():
    try:
        return os.environ['DOCKER_RUNNING'] == 'true'
    except Exception as e:
        logger.error(f"Docker is not running. = {e}")
        return False


def convert_if_docker_localhost(url: str) -> str:
    if url in ('localhost', '127.0.0.1') and is_running_in_docker():
        url = 'host.docker.internal'
    return url
