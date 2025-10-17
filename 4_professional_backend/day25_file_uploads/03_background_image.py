from fastapi import FastAPI, File, UploadFile, BackgroundTasks
import aiofiles
from PIL import Image
import os


app = FastAPI()

def resize_image(path: str):
    img = Image.open(path)
    img.thumbnail((128, 128))
    img.save(path.replace(".jpg", "_resized.jpg"))
    print('Image resized')

@app.post('/upload')
async def upload_file(file: UploadFile = File(...), background_tasks: BackgroundTasks = None):
    os.makedirs('uploads', exist_ok=True)

    path = f'uploads/{file.filename}'
    async with aiofiles.open(path, 'wb') as out_file:
        while content := await file.read(1024):
            await out_file.write(content)
    background_tasks.add_task(resize_image, path)
    return {"message": "Upload complete, processing in background"}


