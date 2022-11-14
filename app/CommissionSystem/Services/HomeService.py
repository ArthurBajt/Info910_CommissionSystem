from fastapi import APIRouter
from fastapi.responses import RedirectResponse


app: APIRouter = APIRouter(prefix="", tags=["Home"])


@app.get('/')
def home():
    return RedirectResponse(url='/docs')
