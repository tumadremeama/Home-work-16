from fastapi import FastAPI
from fastapi.responses import HTMLResponse


app = FastAPI()


@app.get('/', response_class=HTMLResponse)
async def read_root():
    return 'Главная страница'


@app.get('/user/admin', response_class=HTMLResponse)
async def read_admin():
    return 'Вы вошли как администратор'


@app.get('/user/{user_id}', response_class=HTMLResponse)
async def read_user(user_id: int):
    return f'Вы вошли как пользовател № {user_id}'


@app.get('/user', response_class=HTMLResponse)
async def read_user_info(username: str, age: int):
    return f'Информация о пользователе. Имя {username}, Возраст: {age}'
