import os

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite+aiosqlite:///./hiking.db")
SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret-change-in-production")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24 * 7  # 7 days
