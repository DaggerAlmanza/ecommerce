import os


POSTGRES_DB = os.getenv("POSTGRES_DB")
POSTGRES_HOST = os.getenv("POSTGRES_HOST")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD")
POSTGRES_USER = os.getenv("POSTGRES_USER")

DATABASE_URL = f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}/{POSTGRES_DB}"

ACCEPTED = 202
BAD_REQUEST = 400
CREATED = 201
FORBIDDEN = 403
INTERNAL_SERVER_ERROR = 500
NOT_FOUND = 404
OK = 200
UNAUTHORIZED = 401
UNPROCESSABLE_ENTITY = 422

ACCESS_TOKEN_EXPIRE_MINUTES = 30
ALGORITHM = "HS256"
SECRET_KEY = ""

ADMIN_ROL = "admin"
USER_ROL = "user"

NO_EXISTENT_PRODUCT = "El producto no existe"
NOT_ALLOWED = "No tiene permiso para hacer esta acción"

ALLOWED_EXTENSIONS = [".png", ".jpg", ".jpeg", ".gif"]
