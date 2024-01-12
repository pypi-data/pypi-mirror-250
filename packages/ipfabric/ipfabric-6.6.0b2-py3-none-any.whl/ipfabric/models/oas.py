from typing import Optional, List

from pydantic import BaseModel


class OAS(BaseModel):
    web_endpoint: Optional[str] = None
    columns: Optional[List[str]] = None
    nested_columns: Optional[List[str]] = None
