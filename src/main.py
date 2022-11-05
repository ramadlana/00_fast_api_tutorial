from fastapi import FastAPI, Depends, HTTPException
from pydantic import BaseModel
from typing import Union
import auth
import schemas

# Mongo related import
import pymongo
client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client.db_tutorial
users_col = db.col_users

#app
app = FastAPI(title="Tech With Rama",
    description="Open Api using python and fastapi",
    version="1.0.0",
    terms_of_service="http://example.com/terms/",
    contact={
        "name": "Tech With Rama",
        "url": "https://netventura.com",
        "email": "hidayahweb@gmail.com",
    },
    license_info={
        "name": "Apache 2.0",
        "url": "https://www.apache.org/licenses/LICENSE-2.0.html",
    },)
auth_handler = auth.AuthHandler()
auth_wrapper = auth_handler.auth_wrapper



# custom model for open api response docs
class ReturnModelOpenApi(BaseModel):
    foo: Union[str, None]
    message: Union[str, None]

# custom open api responses
open_api_schema_response = {
    201: {
         "model": ReturnModelOpenApi,
        "description": "Successfully created",
        "content": {
            "application/json": {
                "example": {
                    "status": "ok",
                    "message": "successfully created"
                }
            }
        }
    },
    404: {
        "model": ReturnModelOpenApi,
        "description": "Item Not Found",
        "content": {
            "application/json": {
                "example": {
                    "foo": "bar",
                    "message": "username not found"
                }
            }
        }
    },
    302: {"model": ReturnModelOpenApi,"description": "The item was moved"},
    400: {
         "model": ReturnModelOpenApi,
        "description": "username already taken",
        "content": {
            "application/json": {
                "example": {
                    "foo": "bar",
                    "message": "id already taken"
                }
            }
        }
    }
}

@app.post('/register', description="create new users", responses={**open_api_schema_response})
def register(auth_details: schemas.AuthDetails):
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


@app.post('/login')
def login(auth_details: schemas.AuthDetails):
    user = users_col.find_one({"username": auth_details.username})
    # if user not found, or password is not correct
    if (user is None) or (not auth_handler.verify_password(auth_details.password, user['password'])):
        raise HTTPException(status_code=401, detail='Invalid username and/or password')
    token = auth_handler.encode_token(user['username'])
    return { 'token': token }


@app.get('/unprotected')
def unprotected():
    return { 'hello': 'world' }

# Protected
@app.get('/protected')
def protected(username=Depends(auth_wrapper)):
    return { 'name': username }

# Path | Path is variable url 
@app.get('/itemsdetail/{example_string}')
def example_path(example_string: str):
    return {'message': example_string}

#Query | Query is on url: http://127.0.0.1:8000/items/?skip=0&limit=10
@app.get("/items/")
# has default value 0 and 10, 
async def read_item(skip: int = 0, limit: int = 10, username=Depends(auth_wrapper)):
    return {"skip": skip, "limit": limit, "username": username}