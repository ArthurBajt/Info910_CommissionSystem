from fastapi import FastAPI
from .Services import services
from .Controllers import Env

app: FastAPI = FastAPI()
app.secret_key = Env.APP_SECRET

for service in services:
    app.include_router(service)
