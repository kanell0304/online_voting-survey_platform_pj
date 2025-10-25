# backend/app/router/user.py
from typing import List
from fastapi import APIRouter, Depends, Response, Request, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from ..database.crud.user import UserCrud
from ..database.schemas.user import (UserCreate, UserUpdate, UserLogin, UserRead, UserReadWithRoles)
from ..service.user import UserService
from ..database.database import get_db
from ..core.auth import set_auth_cookies, get_user_id
from ..database.schemas.user import ForgotPasswordRequest, ResetPasswordWithCode

router = APIRouter(prefix="/users", tags=["User"])

# --------------------------
# 회원가입 / 로그인 / 로그아웃 / 내 정보
# --------------------------

@router.post("/register", response_model=UserRead, summary="회원가입")
async def register(user: UserCreate, db: AsyncSession = Depends(get_db)):
    db_user = await UserService.register(db, user, role_name=user.role)
    return db_user

@router.post("/login", response_model=UserRead, summary="로그인")
async def login(user: UserLogin, response: Response, db: AsyncSession = Depends(get_db)):
    updated_user, access_token, refresh_token = await UserService.login(db, user)
    set_auth_cookies(response, access_token, refresh_token)
    return updated_user

@router.post("/logout", response_model=bool, summary="로그아웃")
async def logout(response: Response, request: Request, db: AsyncSession = Depends(get_db)):
    refresh_token = request.cookies.get("refresh_token")
    if refresh_token:
        await UserCrud.delete_refresh_token(db, refresh_token)
        await db.commit()
    response.delete_cookie(key="access_token", path="/")
    response.delete_cookie(key="refresh_token", path="/")
    return True

@router.get("/userme", response_model=UserReadWithRoles, summary="내 정보 조회")
async def get_me(user_id: int = Depends(get_user_id), db: AsyncSession = Depends(get_db)):
    return await UserService.get_user_with_user_roles(db, user_id)

# --------------------------
# 사용자 목록 / 단건 조회 / 수정 / 삭제
# --------------------------

@router.get("", response_model=List[UserRead], summary="사용자 목록")
async def list_users(
    skip: int = 0,
    limit: int = 50,
    db: AsyncSession = Depends(get_db),
):
    users = await UserService.list_users(db, skip=skip, limit=limit)
    return users

@router.get("/{user_id}", response_model=UserRead, summary="특정 사용자 조회")
async def get_user(user_id: int, db: AsyncSession = Depends(get_db)):
    return await UserService.get_user_by_id(db, user_id)

@router.patch("/{user_id}", response_model=UserRead, summary="사용자 정보 수정")
async def update_user(
    user_id: int,
    payload: UserUpdate,
    db: AsyncSession = Depends(get_db),
    current_user_id: int = Depends(get_user_id),
):
    if current_user_id != user_id:
        raise HTTPException(status_code=403, detail="본인 정보만 수정할 수 있습니다.")
    return await UserService.update_user(db, user_id, payload)

@router.delete("/{user_id}", response_model=bool, summary="사용자 삭제")
async def delete_user(
    user_id: int,
    db: AsyncSession = Depends(get_db),
    current_user_id: int = Depends(get_user_id),
):
    if current_user_id != user_id:
        raise HTTPException(status_code=403, detail="본인만 계정을 삭제할 수 있습니다.")
    return await UserService.delete_user(db, user_id)

# 비밀번호 찾기 기능 추가 - 이경준
# 비밀번호 찾기 (인증코드 발송)
@router.post("/forgot-password", summary="비밀번호 찾기 (인증코드 발송)")
async def forgot_password(request: ForgotPasswordRequest, db: AsyncSession = Depends(get_db)):
    return await UserService.forgot_password(db, request.email, request.username, request.phone_number)

# 인증코드로 비밀번호 재설정
@router.post("/reset-password", summary="비밀번호 재설정 (인증코드)")
async def reset_password_with_code(request: ResetPasswordWithCode, db: AsyncSession = Depends(get_db)):
    return await UserService.reset_password_with_code(db, request.email, request.reset_code, request.new_password)