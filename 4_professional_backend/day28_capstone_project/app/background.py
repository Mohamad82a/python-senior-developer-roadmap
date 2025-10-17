import time


def send_welcome_email(email: str):
    # This function simulates sending an email (blocking)
    print(f'Welcome to {email}!')
    time.sleep(2)
    print(f'Welcome email sent to {email}!')
