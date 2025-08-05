from pydantic import BaseModel

#class Item(BaseModel):
#    name: str
#    price: float
#    brand: str

class ItemBase(BaseModel):
    id: int

class ItemCreate(ItemBase):
    name: str
    price: float
    brand: str

class ItemRead(ItemBase):
    name: str
    price: float