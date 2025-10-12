from fastapi import FastAPI

app = FastAPI()

@app.get('/')
def index():
    """Basix GET endpoint"""
    return {'message': 'Hello World!'}
