from fastapi import FastAPI, Request
import time

app = FastAPI()


@app.middleware('http')
async def log_request(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    duration = time.time() - start_time
    print(f'{request.method} {request.url} completed in: {duration:.3f}s')
    return response

@app.get('/')
async def index():
    return {'message': 'Hello middleware!'}


