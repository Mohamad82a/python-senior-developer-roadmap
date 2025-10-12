from fastapi import FastAPI


app = FastAPI()

@app.get("/user/{name}")
def read_user(name: str):
    return {'message': f'Hello, {name}'}
