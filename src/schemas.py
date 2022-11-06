from pydantic import BaseModel
from typing import Union


class AuthDetails(BaseModel):
    username: str
    password: str
    role: Union[str,int, None] = None

# custom model for open api response docs
class ExampleResponseModel(BaseModel):
    foo: Union[str, None]
    message: Union[str, None]

# custom open api responses
custom_response_schema_1 = {
    201: {
        "model": ExampleResponseModel,
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
    403: {
        "model": ExampleResponseModel,
        "description": "Not Authorized",
        "content": {
            "application/json": {
                "example": {
                    "status": "Error",
                    "message": "Not Authorized"
                }
            }
        }
    },
    404: {
        "model": ExampleResponseModel,
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
    302: {"model": ExampleResponseModel,"description": "The item was moved"},
    400: {
         "model": ExampleResponseModel,
        "description": "username already taken",
        "content": {
            "application/json": {
                "example": {
                    "foo": "bar",
                    "message": "sorry username already taken."
                }
            }
        }
    }
}