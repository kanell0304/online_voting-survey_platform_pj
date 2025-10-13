# backend/app/core/settings.py
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field
from datetime import timedelta

class Settings(BaseSettings):
    # DB
    db_user: str = Field(..., alias="DB_USER")
    db_password: str = Field(..., alias="DB_PASSWORD")
    db_host: str = Field("localhost", alias="DB_HOST")
    db_port: str = Field("3306", alias="DB_PORT")
    db_name: str = Field(..., alias="DB_NAME")

    # JWT / 보안
    secret_key: str = Field(..., alias="SECRET_KEY")
    jwt_algo: str = Field("HS256", alias="JWT_ALGORITHM")
    access_token_expire_sec: int = Field(900, alias="ACCESS_TOKEN_EXPIRE")
    refresh_token_expire_sec: int = Field(604800, alias="REFRESH_TOKEN_EXPIRE")

    # ⭐ pydantic-settings v2 스타일 설정
    # 루트에서 실행 시 backend/.env 를 보도록 고정
    model_config = SettingsConfigDict(
        env_file="backend/.env",          # backend 폴더에 .env 두는 현재 구조에 맞춤
        env_file_encoding="utf-8",
        case_sensitive=True,
        extra="ignore",
        populate_by_name=True,
    )

    # ------ 편의 프로퍼티들 ------
    @property
    def tmp_db(self) -> str:
        return f"{self.db_user}:{self.db_password}@{self.db_host}:{self.db_port}/{self.db_name}"

    @property
    def database_url(self) -> str:
        return f"mysql+asyncmy://{self.tmp_db}"

    @property
    def sync_database_url(self) -> str:
        return f"mysql+pymysql://{self.tmp_db}"

    @property
    def access_token_expire(self) -> timedelta:
        return timedelta(seconds=self.access_token_expire_sec)

    @property
    def refresh_token_expire(self) -> timedelta:
        return timedelta(seconds=self.refresh_token_expire_sec)


settings = Settings()
