from fastapi import FastAPI, Path
from fastapi.responses import HTMLResponse
from typing import Dict, Annotated


app = FastAPI()


# Инициализация словаря пользователей
users: Dict[str, str] = {'1': 'Имя: Example, возраст: 18'}


@app.get("/users", response_class=HTMLResponse)
async def get_users():
    return users


@app.post("/user/{username}/{age}", response_class=HTMLResponse)
async def create_user(
    username: Annotated[str, Path(min_length=5, max_length=20, description="Enter username")],
    age: Annotated[int, Path(ge=18, le=120, description="Enter age")]
):
    # Находим максимальный ключ
    new_id = str(max(map(int, users.keys()), default=0) + 1)
    users[new_id] = f"Имя: {username}, возраст: {age}"
    return f"User {new_id} is registered"


@app.put("/user/{user_id}/{username}/{age}", response_class=HTMLResponse)
async def update_user(
    user_id: Annotated[int, Path(gt=0, le=100, description="Enter User ID")],
    username: Annotated[str, Path(min_length=5, max_length=20, description="Enter username")],
    age: Annotated[int, Path(ge=18, le=120, description="Enter age")]
):
    if str(user_id) in users:
        users[str(user_id)] = f"Имя: {username}, возраст: {age}"
        return f"User {user_id} has been updated"
    return f"User {user_id} not found"


@app.delete("/user/{user_id}", response_class=HTMLResponse)
async def delete_user(
    user_id: Annotated[int, Path(gt=0, le=100, description="Enter User ID")]
):
    if str(user_id) in users:
        del users[str(user_id)]
        return f"User {user_id} has been deleted"
    return f"User {user_id} not found"
