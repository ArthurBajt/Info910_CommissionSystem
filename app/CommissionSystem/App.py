from fastapi import FastAPI
from .Controllers import *
from .Services import services
from .Controllers import Env

app: FastAPI = FastAPI(
    title="Commission Service",
    description="A rest backend to get, update and follows Commission",
    version="0.1.0"
)


app.secret_key = Env.APP_SECRET

for service in services:
    app.include_router(service)
