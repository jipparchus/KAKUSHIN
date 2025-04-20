
"""
Schemas:
Data class used for input/output validation in FastAPI

Used for...
- API request validation
- API response formatting
"""


from pydantic import BaseModel
from typing import Optional


class AuthData(BaseModel):
    username: str
    password: str


class RegisterUser(BaseModel):
    username: str
    password: str


class CreateClimb(BaseModel):
    user_id: int
    name: str


class UserProfile(BaseModel):
    v_grade: Optional[int]  # int or nan
    height: Optional[float]  # float or nan
    weight: Optional[float]  # float or nan
    share_info: bool

    class Config:
        orm_mode = True
