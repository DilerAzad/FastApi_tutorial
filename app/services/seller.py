from app.api.schemas.seller import SellerCreate
from sqlalchemy.ext.asyncio import AsyncSession
from app.database.models import Seller
import bcrypt

class SellerService:
    def __init__(self, session: AsyncSession):
        self.session = session
    
    async def add(self, credentials: SellerCreate) -> Seller:
        # Hash Password using raw bcrypt because passlib 1.7.4 crashes with bcrypt 4.0+
        salt = bcrypt.gensalt()
        # Ensure password is max 72 bytes and convert to bytes
        password_bytes = credentials.password[:72].encode('utf-8')
        hashed_password = bcrypt.hashpw(password_bytes, salt).decode('utf-8')
        
        seller = Seller(
            **credentials.model_dump(exclude=["password"]),
            password_hash=hashed_password
        )

        self.session.add(seller)
        await self.session.commit()
        await self.session.refresh(seller)

        return seller 