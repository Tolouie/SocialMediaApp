from fastapi import FastAPI
from random import randrange
import pymongo_get_database
from pydantic import BaseModel
from typing import Optional, Union

#Test Database / Fake database
my_posts = [{"title":"Best Breakfast Foods","content":"Chicken and Waffles or Pancakes", "id":1},{"title":"Best Lunch Foods","content":"McDonalds or BurgerKing", "id":2}]

#Model
class Item(BaseModel):
    name: str
    description: Union[str, None] = None
    price: float
    tax: Union[float, None] = None

class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    rating: Optional[int] = None

class Userlogindetails(BaseModel): 
    username: str
    password: str

#Operations
app = FastAPI()

def find_post(id):
    if id in my_posts:
        return my_posts[id]
    else:
        print("Post does not exist")

def find_user(username):
    db = pymongo_get_database.get_database()["login_info"]
    dbUsername = db.find({"username":username})
    if str(dbUsername) is None:
        print("Could not find user")
        return None
    else:
        print(dbUsername)
        return(dbUsername)

@app.post("/signup") #TODO: Convert encrypt password
async def signup(userInfo: Userlogindetails):
    print(userInfo)
    print(find_user(userInfo.username))

    try:
        db = pymongo_get_database.get_database()
    except:
        print("Failed to connect")
    
    try:
        collection_name = db["login_info"]
    except:
        print("Failed to assign collection_name")

    try:
        collection_name.insert_many({"username": userInfo.username, "password":userInfo.password})
    except:
        print("Failed to insert")
    
    return("hello world")
    # collection_login.insert(insert_item)
    # if find_user(userInfo.username) is not None:
    #     db = pymongo_get_database.get_database()["login_info"]
    #     insert_item = {
    #     "username": userInfo.username,
    #     "password": userInfo.password
    #     }    
    #     db.insert_one(insert_item)
    # else:
    #     print("User already exists")
    

@app.post("/login/{username}")
async def login(username):
    return {"message": "There's nothing here"}

@app.get("/posts")
def get_posts():
    return {"data": my_posts}

@app.post("/posts")
async def create_posts(post: Post):
    post_dict = post.dict()
    post_dict['id'] = randrange(0,10000)
    my_posts.append(post_dict)
    return {"data": post_dict}

@app.get("/posts/{id}")
async def get_post(id):
    print(int(id))
    post = find_post(int(id))
    return {"post_detail": post}

@app.post("/items/")
async def create_item(item: Item):
    print(item.name)
    return {"data":"item"}