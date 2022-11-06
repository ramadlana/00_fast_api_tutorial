from pydantic import BaseModel
from typing import Union


# for request Auth model
class AuthDetailsRequest(BaseModel):
    username: str = "your_username"
    password: str = "your_password"
    role: Union[str,int, None] = None

# custom model for open api response docs
class AuthDetailsResponse(BaseModel):
    message: Union[str, None]
class SchemaError4xx(BaseModel):
    detail: str

# custom open api responses (for swagger)
custom_response_schema_1 = {
    200: {
        "model": AuthDetailsResponse,
        "description": "Successfully created",
        "content": {
            "application/json": {
                "example": {
                    "message": "successfully created"
                }
            }
        }
    },
    201: {
        "model": AuthDetailsResponse,
        "description": "Successfully created",
        "content": {
            "application/json": {
                "example": {
                    "message": "successfully created"
                }
            }
        }
    },
    302: {
        "model": AuthDetailsResponse, 
        "description": "The item was moved",
        "content": {
            "application/json": {
                "example": {
                    "message": "successfully created"
                }
            }
        }
    },
    403: {
        "model": SchemaError4xx,
        "description": "Not Authorized",
        "content": {
            "application/json": {
                "example": {
                    "detail": "Not Authorized"
                }
            }
        }
    },
    404: {
        "model": SchemaError4xx,
        "description": "Item Not Found",
        "content": {
            "application/json": {
                "example": {
                    "detail": "username not found"
                }
            }
        }
    },
    400: {
         "model": SchemaError4xx,
        "description": "username already taken",
        "content": {
            "application/json": {
                "example": {
                    "detail": "sorry username already taken."
                }
            }
        }
    }
}