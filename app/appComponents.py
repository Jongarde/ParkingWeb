from pydantic import BaseModel
from typing import Optional, List

class BrandListRequest(BaseModel):
    brands: List[str]