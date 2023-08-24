from pydantic import BaseModel


class Timezone(BaseModel):
    timezone: str


class ServiceStateBase(BaseModel):
    state: str


class ServiceState(BaseModel):
    items: ServiceStateBase
