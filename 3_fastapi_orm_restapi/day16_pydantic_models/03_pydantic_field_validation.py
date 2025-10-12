from fastapi import FastAPI
from pydantic import BaseModel, Field


app = FastAPI()

class Register(BaseModel):
    username: str = Field(min_length=8, max_length=30)
    password: str = Field(min_length=8, max_length=30)
    email: str

@app.post("/register")
def register(data: Register):
    return {'status':'User registered', 'user':data.username}
