from fastapi import APIRouter


app: APIRouter = APIRouter(prefix="", tags=["Home"])


@app.get('/')
async def home():
    return "Hello World"
