from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from typing import List

app = FastAPI()


users: List['User'] = []


class User(BaseModel):
    id: int
    username: str = Field(..., min_length=5, max_length=20, description='Имя пользователя')
    age: int = Field(..., ge=18, le=120, description='Возраст пользователя')


@app.get('/users', response_model=List[User])
async def get_users():
    return users


@app.post('/users/{username}/{age}', response_model=User)
async def create_user(username: str, age: int):
    new_id = len(users) + 1
    user = User(id=new_id, username=username, age=age)
    users.append(user)
    return user


@app.put('/user/{user_id}/{username}/{age}', response_model=User)
async def update_user(user_id: int, username: str, age: int):
    for user in users:
        if user.id == user_id:
            user.username = username
            user.age = age
            return user
    raise HTTPException(status_code=404, detail='User was not found')


@app.delete('/user/{user_id}', response_model=User)
async def delete_user(user_id: int):
    for user in users:
        if user.id == user_id:
            users.remove(user)
            return user
    raise HTTPException(status_code=404, detail='User was not found')
