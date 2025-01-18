from fastapi import FastAPI, Path
from fastapi.responses import HTMLResponse
from typing import Annotated

app = FastAPI()


@app.get('/', response_class=HTMLResponse)
async def read_root():
    return 'Главная страница'


@app.get('/user/admin', response_class=HTMLResponse)
async def read_admin():
    return "Вы вошли как администратор"


@app.get("/user/{user_id}", response_class=HTMLResponse)
async def read_user(
    user_id: Annotated[int, Path(gt=0, le=100, description="Enter User ID")]
):
    return f"Вы вошли как пользователь № {user_id}"


@app.get("/user/{username}/{age}", response_class=HTMLResponse)
async def read_user_info(
    username: Annotated[str, Path(min_length=5, max_length=20, description="Enter username")],
    age: Annotated[int, Path(ge=18, le=120, description="Enter age")]
):
    return f"Информация о пользователе. Имя: {username}, Возраст: {age}"