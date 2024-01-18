from fastapi import UploadFile

async def store_file_locally(file: UploadFile):
    new_file = open(f'/tmp/{file.filename}', 'w')
    file_contents = await file.read()
    file_contents = file_contents.decode('utf-8')
    new_file.write(file_contents)
    new_file.close()