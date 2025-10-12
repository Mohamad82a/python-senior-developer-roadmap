from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

users = {}

class User(BaseModel):
    name: str
    age: int

@app.post('/user_create')  # --- Create ---
def create_user(user: User):
    users[user.name] = user.age
    return {'message': 'user created'}

@app.get('/user/{name}') # --- Read ---
def read_user(name: str):
    return {'name': name, 'age': users.get(name)}
