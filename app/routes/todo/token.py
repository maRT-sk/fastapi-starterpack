# from datetime import timedelta
# from typing import Annotated
#
# from fastapi import APIRouter
# from fastapi import Depends
# from fastapi import HTTPException
# from fastapi import status
# from fastapi.security import OAuth2PasswordRequestForm
# from pydantic import BaseModel
# from sqlmodel import select
# from starlette.requests import Request
#
# from app.core.auth.crypt import create_access_token
# from app.core.config import app_config
# from app.core.database import async_session_maker
# from app.models.user import User
#
#
# ACCESS_TOKEN_EXPIRE_MINUTES = 30
#
# router = APIRouter()
#
#
# class Token(BaseModel):
#     access_token: str
#     token_type: str
#
#
# @router.post("/token", response_model=Token)
# async def login_for_access_token(
#     request: Request,
#     form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
# ) -> Token:
#     """Endpoint to authenticate a user and provide an access token."""
#
#     async with async_session_maker() as session:
#         user = await session.scalar(select(User).where(User.username == form_data.username))
#
#         # system_admin login
#         if form_data.username == "system_admin" and form_data.password == str(app_config.STARLETTE_ADMIN_KEY):
#             access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
#             access_token = create_access_token(data={"sub": "system_admin"}, expires_delta=access_token_expires)
#             request.session.update({"access_token": access_token, "is_superuser": True})
#             return Token(access_token=access_token, token_type="bearer")
#
#         # User not found or invalid password
#         if not user or not verify_password(form_data.password, user.password):
#             raise HTTPException(
#                 status_code=status.HTTP_401_UNAUTHORIZED,
#                 detail="Incorrect username or password",
#                 headers={"WWW-Authenticate": "Bearer"},
#             )
#
#         # Regular user login
#         access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
#         access_token = create_access_token(data={"sub": user.username}, expires_delta=access_token_expires)
#         request.session.update({"access_token": access_token, "is_superuser": user.is_superuser})
#         return Token(access_token=access_token, token_type="bearer")
