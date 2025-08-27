from fastapi import APIRouter, Depends
from schemas import items as ItemSchema
from api.depends import verify_apikey
from database.fake_db import get_db

fake_db = get_db()

router = APIRouter(
    tags=["items"], 
    prefix="/api",
    dependencies=[Depends(verify_apikey)]
)

@router.get("/items/{item_id}" , response_model=ItemSchema.ItemRead)
def get_item_by_id(item_id : int , qry : str = None ):
    if item_id not in fake_db["items"]:
        return {"error": "Item not found"}
    return fake_db['items'][item_id]

@router.post("/items" , response_model=ItemSchema.ItemCreate)
def create_items(item: ItemSchema.ItemCreate ):
    fake_db["items"][item.id] = item
    return item

@router.delete("/items/{item_id}")
def delete_items(item_id: int):
    item = fake_db["items"].pop(item_id)
    return item