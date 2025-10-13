import jwt
from datetime import datetime, timedelta, timezone
import jdatetime

current_time_utc = datetime.now(timezone.utc) + timedelta(hours=3, minutes=30)
expiration_time = current_time_utc + timedelta(minutes=10)


SECRET_KEY = 'mysecret'
ALGORITH = 'HS256'

payload = {
    'sub': 'user@example.com',
    'exp': expiration_time,
    'persian_exp': expiration_time.strftime('%Y/%m/%d - %H:%M'),
}

token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITH)
print('Encoded Token:', token)

decoded = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITH])
print('Decoded Token:', decoded)
