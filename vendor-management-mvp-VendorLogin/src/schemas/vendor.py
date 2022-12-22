from pydantic import BaseModel, Field

class VendorSchema(BaseModel):
    name: str = Field(min_length=1)
    Phone: int = Field()
    email: str = Field(min_length=1)

class MenuSchema(BaseModel):
    user_id: str = Field()
    date: str= Field(min_length=1)
    breakfast: str= Field(min_length=1)
    lunch: str= Field(min_length=1)
    dinner: str= Field(min_length=1)