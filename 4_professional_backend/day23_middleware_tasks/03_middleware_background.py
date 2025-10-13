from fastapi import FastAPI, BackgroundTasks, Request
import time

app = FastAPI()

def log_to_file(message: str):
    with open('logs.txt', 'a') as file:
        file.write(message + '\n')

@app.middleware("http")
async def timing_and_logging(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    duration = time.time() - start_time
    with open('requests.log', 'a') as file:
        file.write(f'{request.method} {request.url.path} took {duration:.3f}s\n')
    return response

@app.get('/')
async def index(background_tasks: BackgroundTasks):
    background_tasks.add_task(log_to_file, 'User visited home page')
    return {'message': 'Logged visit'}

