import redis
from fastapi import FastAPI
import json


app = FastAPI()
r = redis.Redis(host='localhost', port=6379, db=0)

@app.get('/user/{user_id}')
async def get_user(user_id: int):
    cached = await r.get(f'user {user_id}')
    if cached:
        return {'source': 'cache', 'data': json.loads(cached)}

    data = {'id': user_id, 'name': 'Alex'}
    await r.setex(f'user {user_id}', 60, json.dumps(data))
    return {'source': 'database', 'data': data}
