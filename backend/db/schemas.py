
"""
Schemas:
Data class used for input/output validation in FastAPI

Used for...
- API request validation
- API response formatting
"""


from pydantic import BaseModel


class RegisterUser(BaseModel):
    username: str
    password: str


class CreateClimb(BaseModel):
    user_id: int
    name: str
