"""
Forward the port 8000 from the Android device to the host machine.
Check the device ID with:
adb devices
Then:
adb -s R52R902GW2J reverse tcp:8000 tcp:8000
To start the server, run:
uvicorn main:app --host localhost --port 8000
or:
uvicorn main:app --reload --host 0.0.0.0 --port 8000
"""
import os
from fastapi import APIRouter, File, UploadFile, Depends, HTTPException, Header
from auth.jwt_utils import decode_token
from fastapi.responses import JSONResponse

from config import config

router = APIRouter()
UPLOAD_DIR = config['path']['assets']


def get_user_id(authorization: str = Header(...)):
    if not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Invalid token format")
    token = authorization[7:]
    decoded = decode_token(token)
    if not decoded:
        raise HTTPException(status_code=401, detail="Token invalid or expired")
    return decoded["user_id"]

# When accessed to the root URL


# @app.get("/")
@router.get("/")
def read_root():
    return {"greeting": "Hello World from Python FastAPI!!!"}


# @app.post("/upload")
@router.post("/upload")
async def upload_video(file: UploadFile = File(...), user_id: int = Depends(get_user_id)):
    folder = os.path.join(UPLOAD_DIR, str(user_id))
    os.makedirs(folder, exist_ok=True)
    filepath = os.path.join(folder, file.filename)
    # Read bytes
    contents = await file.read()

    with open(filepath, "wb") as f:
        f.write(contents)

    return JSONResponse({"status": "success", "filename": file.filename})
