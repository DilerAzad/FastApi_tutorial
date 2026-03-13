from app.utils import generate_access_token
from fastapi import HTTPException, status
from app.api.schemas.seller import SellerCreate
from passlib.context import CryptContext

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.database.models import Seller
import hashlib
import jwt
from datetime import datetime, timedelta
from app.config import security_settings

class SellerService:
    def __init__(self, session: AsyncSession):
        self.session = session
        self.pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    
    async def add(self, credentials: SellerCreate) -> Seller:
        sha = hashlib.sha256(credentials.password.encode()).hexdigest()
        seller = Seller(
            **credentials.model_dump(exclude=["password"]),
            password_hash=self.pwd_context.hash(sha)
        )

        self.session.add(seller)
        await self.session.commit()
        await self.session.refresh(seller)

        return seller
    
    async def token(self, email, password) -> str:
        #Validate credentials
        result = await self.session.execute(select(Seller).where(Seller.email == email))

        seller = result.scalar()

        sha = hashlib.sha256(password.encode()).hexdigest()
        
        is_valid = False
        if seller:
            is_valid = self.pwd_context.verify(sha, seller.password_hash) or \
                       self.pwd_context.verify(password, seller.password_hash)
            
        if not seller or not is_valid:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Invalid credentials")
        
        token = generate_access_token(
            data={
                "user": {
                    "name": seller.name,
                    "email": seller.email
                }
            }
        )

        return token

    