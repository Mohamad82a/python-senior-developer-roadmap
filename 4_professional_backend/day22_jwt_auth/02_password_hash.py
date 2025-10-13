from passlib.context import CryptContext

# Initialize password hashing context
pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")

# Hash password
password = 'mypassword123'
hashed_password = pwd_context.hash(password)
print(f'Hashed password: {hashed_password}')

# Verify password
valid = pwd_context.verify('mypassword123', hashed_password)
print(f'Valid password?: {valid}')
