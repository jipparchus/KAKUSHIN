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

from fastapi import FastAPI
from routes import upload
from routes import auth
from routes import user_info

import os
from config import config
import db.init_rdb as init_rdb

"""
Database initialisation
"""

if os.path.exists(config['paths']['database']):
    pass
else:
    init_rdb.main()

"""
Start API
"""

# Create FastAPI instance
app = FastAPI()
# Authentication: Who are you?
# Authorization: What can you do? - JWT can carry role as well.
app.include_router(auth.router, prefix="/auth")
app.include_router(user_info.router, prefix="/user")
app.include_router(upload.router)
