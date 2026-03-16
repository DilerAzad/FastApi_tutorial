from app.database.redis import add_jti_to_blacklist
from app.api.dependencies import get_access_token
from app.database.models import Seller
from app.api.dependencies import SessionDep
from app.utils import decode_access_token
from typing import Annotated
from app.api.schemas.seller import SellerRead
from app.api.dependencies import SellerServiceDep
from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from app.core.security import oauth2_scheme
from ..schemas.seller import SellerCreate


router = APIRouter(prefix="/seller", tags=["Seller"])

@router.post("/signup", response_model=SellerRead)
async def register_seller(
    seller: SellerCreate, 
    service: SellerServiceDep
):
    return await service.add(seller) 

@router.post("/token")
async def login_seller(
    request_form: Annotated[OAuth2PasswordRequestForm, Depends()],
    service: SellerServiceDep
):
    token = await service.token(request_form.username, request_form.password)

    return {
        "access_token": token,
        "type": "jwt"
    }

@router.get("/logout")
async def logout_seller(
    token_data: Annotated[dict, Depends(get_access_token)]
):
    await add_jti_to_blacklist(token_data["jti"])
    return {
        "detail": "Logged out successfully"
    }