import redis, json

r = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True)

def update_user(user_id: int, new_name: str):
    user = {
        'id': user_id,
        'name': new_name
    }
    r.setex(f'user: {user_id}', 60, json.dumps(user))
    print('Cache updated: ', user)

def invalidate_cache(user_id: int):
    r.delete(f'user: {user_id}')
    print(f'Cache invalidated for user: {user_id}')

update_user(1, 'django')
invalidate_cache(1)

