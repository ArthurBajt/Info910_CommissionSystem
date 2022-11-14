from pydantic import BaseModel, Field
from bson import ObjectId
from .PyObjectId import PyObjectId
from ..Controllers.DB import collection_user, collection_user_token
from ..Controllers import PasswordEncoder


class User(BaseModel):
    username: str = Field(...)
    files: list[PyObjectId] = Field()

    password_encoded: bytes = Field(...)
    password_salt: bytes = Field(...)

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}

    @staticmethod
    def is_username_available(username: str) -> bool:
        return collection_user.find_one({"username": username}) is None

    @staticmethod
    def get(id: str) -> 'User':
        objId = None
        try:
            objId = ObjectId(id)
        except:
            return None
        return collection_user.find_one({"_id": objId})

    @staticmethod
    def get_by_username(username: str) -> 'User':
        cursor = collection_user.find_one({"username": username})
        if cursor is not None:
            try:
                return User.parse_obj(cursor)
            except:
                pass
        return None

    @staticmethod
    def get_by_token_id(token_id):
        return UserToken.get_associated_user(token_id)

    @staticmethod
    def create(username: str, password: str) -> 'User':
        salt: bytes = PasswordEncoder.generate_salt()
        password_encoded: bytes = PasswordEncoder.encode(password, salt)
        user: User = User(username=username, files=[], password_encoded=password_encoded, password_salt=salt)

        if not User.is_username_available(username):
            return None

        inserted_id = collection_user.insert_one(user.dict()).inserted_id
        return User.get(inserted_id)

    @staticmethod
    def all() -> list['User']:
        return list(collection_user.find({}))

    @staticmethod
    def login(username: str, plain_password: str) -> 'UserToken':
        user = collection_user.find_one({"username": username})
        if user is None:
            return None

        if PasswordEncoder.verify(plain_password, user["password_encoded"], user["password_salt"]):
            return UserToken.create(str(user["_id"]))

        return None


class UserOut(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    username: str = Field(...)
    files: list[PyObjectId] = Field()

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}


# ---

class UserToken(BaseModel):
    user_id: str = Field(...)

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}

    @staticmethod
    def create(user_id: str) -> 'UserToken':
        UserToken.delete_user_tokens(user_id)
        user: User = User.get(user_id)
        if user is None:
            return None

        token: UserToken = UserToken(user_id=user_id)
        inserted_id = collection_user_token.insert_one(token.dict()).inserted_id
        return collection_user_token.find_one({"_id": inserted_id})

    @staticmethod
    def delete_user_tokens(user_id: str):
        collection_user_token.delete_many({"user_id": user_id})

    @staticmethod
    def get_associated_user(token_id: str) -> User:
        obj_id: ObjectId = None
        try:
            obj_id = ObjectId(token_id)
        except:
            pass

        if obj_id is None:
            return None
        token: UserToken = UserToken.parse_obj(collection_user_token.find_one({"_id": obj_id}))

        return User.get(token.user_id)