from dataclasses import dataclass


@dataclass
class ConnectionInfo:
    host: str
    port: int
    username: str
    password: str
    connection_mode: str