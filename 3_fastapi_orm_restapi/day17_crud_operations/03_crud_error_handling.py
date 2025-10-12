from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel

app = FastAPI()

users = {}

class User(BaseModel):
    first_name: str
    last_name: str
    username: str
    age: int
    phone_number: str

@app.post('/user_create')  # --- Create ---
def create_user(user: User):
    if user.username in users:
        raise HTTPException(status_code=400, detail="Username already exists")

    users[user.username] = user.model_dump()
    return {'message': 'User created successfully'}


@app.get('/users/{username}') # --- Read ---
def read_user(username: str):
    if username not in users:
        raise HTTPException(status_code=404, detail='User not found')
    return {'user': users[username]}


@app.put('/users/{username}') # --- Update ---
def update_user(username:str, user:User):
    if username not in users:
        raise HTTPException(status_code=404, detail='User not found')

    if user.username != username:
        if user.username in users:
            raise HTTPException(status_code=404, detail='Username already exists')
        del users[username]
        users[user.username] = user.model_dump()
    else:
        users[username] = user.model_dump()
    return {'message': 'User updated successfully', 'user': users[user.username]}



@app.delete('/users/{username}') # --- Delete ---
def delete_user(username:str):
    if username not in users:
        raise HTTPException(status_code=404, detail='User not found')
    else:
        users.pop(username, None)
    return {'message': 'User deleted successfully'}


