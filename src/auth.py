import jwt

from fastapi import HTTPException, Security, Cookie
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from passlib.context import CryptContext
from datetime import datetime, timedelta

secret_string = 'SECRET'

class AuthHandler():
    security = HTTPBearer()
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    secret = secret_string
    def get_password_hash(self, password):
        return self.pwd_context.hash(password)

    def verify_password(self, plain_password, hashed_password):
        return self.pwd_context.verify(plain_password, hashed_password)

    def encode_token(self, user_id):
        payload = {
            'exp': datetime.utcnow() + timedelta(days=0, minutes=60, seconds=10),
            'iat': datetime.utcnow(),
            'username': user_id
        }
        return jwt.encode(
            payload,
            self.secret,
            algorithm='HS256',
        )

    def decode_token(self, token):
        try:
            decoded_payload = jwt.decode(token, self.secret, algorithms=['HS256'])
            return decoded_payload
        except jwt.ExpiredSignatureError:
            raise HTTPException(status_code=401, detail='Expired token')
        except:
            raise HTTPException(status_code=401, detail='Invalid token')

    def auth_wrapper(self, auth: HTTPAuthorizationCredentials = Security(security)):
        return self.decode_token(auth.credentials)
    
    def auth_wrapper_secure(self, token: str = Cookie(None)):
        print(token)
        return self.decode_token(token)
