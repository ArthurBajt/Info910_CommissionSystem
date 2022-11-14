from fastapi import APIRouter


app: APIRouter = APIRouter(prefix="/commission", tags=["Commission"])


@app.get('/')
@app.get('/all')
def all():
    return []
