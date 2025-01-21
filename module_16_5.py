from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel, Field
from typing import List

app = FastAPI()

users: List['User'] = []


class User(BaseModel):
    id: int
    username: str = Field(..., min_length=5, max_length=20, description='Имя пользователя')
    age: int = Field(..., ge=18, le=120, description='Возраст пользователя')


templates = Jinja2Templates(directory='templates')


@app.get('/', response_class=HTMLResponse)
async def read_users(request: Request):
    return templates.TemplateResponse('users.html', {'request': request, 'users': users})


@app.get('/user/{user_id}', response_class=HTMLResponse)
async def read_user(request: Request, user_id: int):
    for user in users:
        if user.id == user_id:
            return templates.TemplateResponse('users.html', {'request': request, 'user': user})
    raise HTTPException(status_code=404, detail='User was not found')


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


@app.on_event("startup")
async def startup_event():
    users.append(User(id=1, username="UrbanUser", age=24))
    users.append(User(id=2, username="UrbanTest", age=22))
    users.append(User(id=3, username="Capybara", age=60))
