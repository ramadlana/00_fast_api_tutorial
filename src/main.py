from fastapi import FastAPI, Depends, HTTPException, Response, Cookie
from typing import Union
from . import auth
from . import schemas
import os

# Mongo related import
import pymongo
MONGO_SERVER_STRING = os.environ["MONGO_SERVER_STRING"]
client = pymongo.MongoClient(MONGO_SERVER_STRING)
db = client.db_tutorial
users_col = db.col_users

# APP
app = FastAPI(title="Lingkar Academy",
    description="Open Api using python and fastapi",
    version="2.0.0",
    terms_of_service="http://example.com/terms/",
    contact={
        "name": "Lingkar Academy",
        "url": "https://netventura.com",
        "email": "hidayahweb@gmail.com",
    },
    license_info={
        "name": "Apache 2.0",
        "url": "https://www.apache.org/licenses/LICENSE-2.0.html",
    },)

# CORS
from fastapi.middleware.cors import CORSMiddleware
origins = [
    "http://localhost",
    "http://localhost:3000",
    "https://example.com",
    "https://3545-115-178-194-222.ap.ngrok.io",
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Auth Handler and Wrapper 
auth_handler = auth.AuthHandler()
auth_wrapper = auth_handler.auth_wrapper
auth_wrapper_secure = auth_handler.auth_wrapper_secure

@app.get("/")
async def home():
    return {"message": "home"}

# use schema for return in swager and redoc using responses property
@app.post('/register',name="Register user",tags=["Auth"], description="create new users", responses={**schemas.custom_response_schema_1})
async def register(auth_details: schemas.AuthDetailsRequest):
    # check if username is exist
    if users_col.find_one({"username": auth_details.username}) != None:
        raise HTTPException(status_code=400, detail='Username is taken')
    
    # Hash password
    hashed_password = auth_handler.get_password_hash(auth_details.password)
    
    # insert to db
    users_col.insert_one({
        'username': auth_details.username,
        'password': hashed_password    
    })
    return {"message": "successfully created"}

# Login to get Token
@app.post('/login', name="Login user to get Token", tags=["Auth"])
async def login(auth_details: schemas.AuthDetailsRequest):
    user = users_col.find_one({"username": auth_details.username})
    # if user not found, or password is not correct
    if (user is None) or (not auth_handler.verify_password(auth_details.password, user['password'])):
        raise HTTPException(status_code=401, detail='Invalid username and/or password')
    token = auth_handler.encode_token(user['username'])
    return { 'token': token }

# Path | Path is variable url 
@app.get('/itemsdetail/{example_string}')
async def example_path(example_string: str):
    return {'message': example_string}

#Query | Query is on url after question mark: http://127.0.0.1:8000/items/?skip=0&limit=10
@app.get("/items/",name="get query",tags=["Others"], description="get query",  responses={**schemas.custom_response_schema_1})
# has default value 0 and 10, 
async def read_item(skip: int = 0, limit: int = 10, username=Depends(auth_wrapper)):
    return {"skip": skip, "limit": limit, "username": username}

# Un Protected Routes
@app.get('/unprotected',name="unprotected routes", tags=["Protected Routes"])
async def unprotected():
    return { 'hello': 'world' }

# Protected Routes
@app.get('/protected', tags=["Protected Routes"], description="Use login to get token", responses={**schemas.custom_response_schema_1})
async def protected(username=Depends(auth_wrapper)):
    return { 'name': username }




### End ##
# Secure login use for front end to backend
@app.post('/secure-login')
async def login_http_only(auth_details: schemas.AuthDetailsRequest, response: Response):
    user = users_col.find_one({"username": auth_details.username})
    # if user not found, or password is not correct
    if (user is None) or (not auth_handler.verify_password(auth_details.password, user['password'])):
        raise HTTPException(status_code=401, detail='Invalid username and/or password')
    token = auth_handler.encode_token(user['username'])
    response.set_cookie(key='token', value=token, httponly=True,domain=".ngrok.io", max_age=18000, expires=18000, samesite='None',secure=False)
    return { 'message': "login success" }

# protected routes using wrapper http only cookies
@app.get("/protected-http-only-cookies")
async def protected_cookes(token=Depends(auth_wrapper_secure)):
    return {"token": token}
# End of secure login