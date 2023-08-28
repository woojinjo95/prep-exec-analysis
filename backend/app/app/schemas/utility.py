from pydantic import BaseModel


class Timezone(BaseModel):
    timezone: str


class ServiceStateBase(BaseModel):
    state: str


class ServiceState(BaseModel):
    items: ServiceStateBase


class LogConnectionStatusBase(BaseModel):
    status: str


class LogConnectionStatus(BaseModel):
    items: LogConnectionStatusBase
