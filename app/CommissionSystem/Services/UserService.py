from fastapi import APIRouter, HTTPException, Form, Depends
from fastapi.security import OAuth2PasswordRequestForm
from ..Models import User, UserOut, UserToken
from ..Controllers import oauth2_scheme


app: APIRouter = APIRouter(prefix="/user", tags=["User"])


@app.get('/', response_model=list[UserOut])
@app.get('/all', response_model=list[UserOut])
def all():
    return User.all()


@app.get('/id/<id>', response_model=UserOut)
def get_user(id: str):
    user: User = User.get(id)
    if user is None:
        raise HTTPException(404, detail="User not found")
    return user


@app.get('/username/<username>', response_model=UserOut)
def get_user_by_username(username: str):
    user: User = User.get_by_username(username)
    if user is None:
        raise HTTPException(404, detail="User not found")
    return user


@app.get('/me', response_model=UserOut)
def get_current_user(token: str = Depends(oauth2_scheme)):
    user: User = User.get_by_token_id(token)
    if user is None:
        raise HTTPException(400, detail="Not found")
    return user


@app.post('/create', response_model=UserOut, description="Creates a new user")
def create(username: str = Form(...), password: str = Form(...)):
    if not User.is_username_available(username):
        raise HTTPException(409, detail="User already exist")

    if len(password) < 4:
        raise HTTPException(400, detail="Password too short")

    if len(username) == 0:
        raise HTTPException(400, detail="username too short or not provided.")

    user: User = User.create(username, password)

    if user is None:
        raise HTTPException(400, detail="Could not create user")
    else:
        return user


@app.post("/login")
async def login(form: OAuth2PasswordRequestForm = Depends()):
    user: User = User.get_by_username(form.username)
    if (user is not None):
        token = User.login(form.username, form.password)
        if token is not None:
            return {"access_token": str(token["_id"]), "token_type": "bearer"}
    raise HTTPException(400, detail="Incorrect username/password")

