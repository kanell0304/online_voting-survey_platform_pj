# backend/app/routers/user.py
from fastapi import APIRouter, Depends, Response, Request
from sqlalchemy.ext.asyncio import AsyncSession

from backend.app.database.crud.user import UserCrud
from backend.app.database.schemas.user import UserCreate, UserUpdate, UserLogin, UserRead
from backend.app.service.user import UserService
from backend.app.database.database import get_db
from backend.app.core.auth import set_auth_cookies, get_user_id

# scheme(user.py) / crud -> service -> router(controller) -> front
router = APIRouter(prefix="/users", tags=["User"])

@router.post("/register", response_model=UserRead)
async def register(user: UserCreate, db: AsyncSession = Depends(get_db)):
    db_user = await UserService.register(db, user)
    return db_user

@router.post("/login", response_model=UserRead)
async def login(user: UserLogin, response: Response, db: AsyncSession = Depends(get_db)):
    updated_user, access_token, refresh_token = await UserService.login(db, user)
    set_auth_cookies(response, access_token, refresh_token)
    return updated_user

@router.post("/logout", response_model=bool)
async def logout(response: Response, request: Request, db: AsyncSession = Depends(get_db)):
    # DB의 해당 refresh_token을 제거하고 쿠키도 삭제
    refresh_token = request.cookies.get("refresh_token")
    if refresh_token:
        await UserCrud.delete_refresh_token(db, refresh_token)
        await db.commit()

    response.delete_cookie(key="access_token", path="/")
    response.delete_cookie(key="refresh_token", path="/")
    return True

@router.get("/userme", response_model=UserRead)
async def get_user(user_id: int = Depends(get_user_id), db: AsyncSession = Depends(get_db)):
    return await UserService.get_user(db, user_id)
