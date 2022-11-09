import os
from dotenv import load_dotenv


load_dotenv(".env", override=True)


class Env:
    MONGO_URI: str = os.getenv("MONGO_URI")
    DATABASE_NAME: str = os.getenv("DATABASE_NAME")
    APP_SECRET: str = os.getenv("APP_SECRET")
    APP_PORT: int = int(os.getenv("APP_PORT"))
