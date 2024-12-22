from fastapi import FastAPI, HTTPException, Path
from pydantic import BaseModel
from typing import List, Optional

app = FastAPI()

# Модель пользователя
class User(BaseModel):
    id: int
    username: str
    age: int

# Изначальный пустой список пользователей
users: List[User ] = []

# GET запрос для получения всех пользователей
@app.get("/users", response_model=List[User ])
async def get_users():
    return users

# POST запрос для добавления нового пользователя
@app.post("/user/{username}/{age}", response_model=User )
async def create_user(
    username: str,
    age: int
):
    new_id = (users[-1].id + 1) if users else 1
    new_user = User(id=new_id, username=username, age=age)
    users.append(new_user)
    return new_user

# PUT запрос для обновления пользователя
@app.put("/user/{user_id}", response_model=User )
async def update_user(
    user_id: int = Path(..., description="Enter user ID"),
    username: str = Path(..., description="Enter username"),
    age: int = Path(..., description="Enter age")
):
    for user in users:
        if user.id == user_id:
            user.username = username
            user.age = age
            return user
    raise HTTPException(status_code=404, detail="User  was not found")

# DELETE запрос для удаления пользователя
@app.delete("/user/{user_id}", response_model=User )
async def delete_user(user_id: int = Path(..., description="Enter user ID")):
    for index, user in enumerate(users):
        if user.id == user_id:
            return users.pop(index)
    raise HTTPException(status_code=404, detail="User  was not found")
