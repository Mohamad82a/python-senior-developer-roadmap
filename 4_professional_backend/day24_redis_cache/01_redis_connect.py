import redis

r = redis.Redis(host='localhost', port=6379, db=0)

r.set('message', 'Hello mate')
print(f'Stored msg: {r.get("message").decode()}')