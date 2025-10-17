from fastapi import FastAPI, File, UploadFile

app = FastAPI()

@app.post('/upload')
async def upload_file(file: UploadFile = File(...)):
    contents = await file.read()
    return {'filename': file.filename, 'size': len(contents)}
