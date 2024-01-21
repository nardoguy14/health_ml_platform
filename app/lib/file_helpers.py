from fastapi import UploadFile
import tempfile


async def store_file_locally(file: UploadFile):
    new_file = open(f'/tmp/{file.filename}', 'w')
    file_contents = await file.read()
    file_contents = file_contents.decode('utf-8')
    new_file.write(file_contents)
    new_file.close()


async def get_file_locally(filename_path: str):
    readfile = open(filename_path, 'r')
    return readfile
