from pydantic import BaseModel
from typing import List


class ApiResponse(BaseModel):
    result: List
    status: int
    errors: List
