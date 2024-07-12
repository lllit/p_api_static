from fastapi import APIRouter,Response,HTTPException
from starlette.status import HTTP_201_CREATED, HTTP_204_NO_CONTENT, HTTP_401_UNAUTHORIZED
#from schema.user_schema import UserSchema, DataUser
from config.db import engine
#from model.users import users
#from werkzeug.security import generate_password_hash,check_password_hash
from typing import List