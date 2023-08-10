from pydantic import BaseModel


class Timezone(BaseModel):
    timezone: str