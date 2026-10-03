from os import name

from fastapi import APIRouter, FastAPI
from pydantic import BaseModel
from mongoengine import Document, StringField, IntField, connect
from typing import Optional

import uvicorn

app=FastAPI()
router=APIRouter()

connect(
    db="my_database",
    host="mongodb://mongodb:27017"                  
)

class users(Document):
    name=StringField(null=True)
    age=IntField(null=True)

    def payload(self):
        return {
            "id": str(self.id),
            "name": self.name,
            "age": self.age
        }

class createusers(BaseModel):
    id:Optional[str]=None
    name:Optional[str]=None
    age:Optional[int]=None  



@router.get("/users")
async def get_users(userid:str=None):
    if userid:
        user = users.objects(id=userid).get()
        return user.payload()
    else:
        users_list = users.objects().all()
        return [user.payload() for user in users_list]

@router.post("/createusers")
async def create_user(user: createusers,userid:str=None):
    if userid:
        existing_user = users.objects(id=userid).get()
        if user:
            existing_user.name = user.name
            existing_user.age = user.age
            existing_user.save()
            return existing_user.payload()
    else:
        new_user = users(name=user.name, age=user.age)
        new_user.save()
        return new_user.payload()

@router.delete("/deleteusers")
async def delete_user(userid:str):
    user = users.objects(id=userid).get()
    user.delete()
    return {"message": "User deleted successfully"}

app.include_router(router)

if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)