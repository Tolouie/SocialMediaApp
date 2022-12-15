from typing import Union

from fastapi import FastAPI
from pydantic import BaseModel


class Item(BaseModel):
    name: str
    description: Union[str, None] = None
    price: float
    tax: Union[float, None] = None

app = FastAPI()

@app.get("/")
async def login():
    return {"message": "There's nothing here"}

@app.get("/post")
def get_posts():
    return {"data": "This is your posts"}


@app.post("/items/")
async def create_item(item: Item):
    return item