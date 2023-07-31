from typing import List, Optional

from pydantic import BaseModel


class FileRead(BaseModel):
    file_name: str
    file_type: str