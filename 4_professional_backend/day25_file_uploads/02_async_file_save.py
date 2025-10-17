from fastapi import FastAPI, File, UploadFile
import aiofiles
import os

app = FastAPI()

@app.post('/save-file')
async def save_file(file: UploadFile = File(...)):
    os.makedirs('uploads', exist_ok=True)

    async with aiofiles.open(f'uploads/{file.filename}', 'wb') as out_file:
        while content := await file.read(1024):
            await out_file.write(content)
    return {'message': 'File saved!'}