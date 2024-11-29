from pydantic import BaseModel, Field


class UserCreate(BaseModel):
    firstName: str = Field(..., min_length=2, max_length=50, example="Mehrdad")
    lastName: str = Field(..., min_length=2, max_length=50, example="Kazazi")
    nationalCode: str = Field(..., pattern=r"^\d+$", min_length=8, max_length=10, example="14159252")
    password: str = Field(..., min_length=8, max_length=255, example="password@12345")


class UserResponse(BaseModel):
    id: int
    firstName: str
    lastName: str
    nationalCode: str

    class Config:
        orm_mode = True
