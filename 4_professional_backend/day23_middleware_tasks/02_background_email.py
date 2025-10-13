from fastapi import FastAPI, BackgroundTasks
import time

app = FastAPI()

def send_email(email: str, message: str):
    print(f'Sending email to {email}...')
    time.sleep(2)
    print(f'Email sent to {email}: {message}')

@app.post('/send-email')
async def send_email_endpoint(email: str, background_tasks: BackgroundTasks):
    background_tasks.add_task(send_email, email, 'welcome to my fastapi app')
    return {'status': 'Email schedules'}


