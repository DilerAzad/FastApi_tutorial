import uuid
import jwt
from datetime import datetime, timedelta
from app.config import security_settings

def generate_access_token(
    data: dict,
    expiry: timedelta = timedelta(hours=1),
    ) -> str:
    return jwt.encode(
            payload={
                **data,
                "jti": str(uuid.uuid4()),
                "exp" : datetime.now() + expiry
            },
            key=security_settings.JWT_SECRET_KEY,
            algorithm=security_settings.JWT_ALGORITHM
        )

def decode_access_token(token: str) -> dict | None:
    try:
        return jwt.decode(
            token,
            key=security_settings.JWT_SECRET_KEY,
            algorithms=[security_settings.JWT_ALGORITHM]
        )
    except jwt.PyJWTError:
        return None