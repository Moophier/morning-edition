from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel


# --- Auth ---
class UserRegister(BaseModel):
    email: str
    name: str
    password: str


class UserLogin(BaseModel):
    email: str
    password: str


class UserOut(BaseModel):
    id: str
    email: str
    name: str
    avatar: str
    created_at: datetime

    class Config:
        from_attributes = True


class TokenOut(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: UserOut


# --- Tags ---
class TagOut(BaseModel):
    id: str
    name: str
    name_en: str
    category: str
    color_hex: str
    bg_rgba: str

    class Config:
        from_attributes = True


class TagCategory(BaseModel):
    category: str
    tags: List[TagOut]


# --- Routes ---
class RouteCreate(BaseModel):
    name: str
    description: str = ""
    difficulty: int = 1
    cost_level: int = 1
    region: str = ""
    season_calendar: List[int] = []
    route_coords: List[List[float]] = []
    elevation_profile: List[dict] = []
    days: List[dict] = []
    gallery: List[str] = []
    duration_days: str = ""
    distance_km: float = 0
    cumulative_climb: int = 0
    max_elevation: int = 0
    hero_image: str = ""
    tag_ids: List[str] = []


class RouteUpdate(RouteCreate):
    pass


class RouteListItem(BaseModel):
    id: str
    name: str
    slug: str
    difficulty: int
    cost_level: int
    region: str
    duration_days: str
    distance_km: float
    hero_image: str
    tags: List[TagOut]
    author_name: str = ""
    created_at: datetime

    class Config:
        from_attributes = True


class RouteDetail(BaseModel):
    id: str
    name: str
    slug: str
    description: str
    difficulty: int
    cost_level: int
    region: str
    season_calendar: List[int]
    route_coords: List[List[float]]
    elevation_profile: List[dict]
    days: List[dict]
    gallery: List[str]
    duration_days: str
    distance_km: float
    cumulative_climb: int
    max_elevation: int
    hero_image: str
    tags: List[TagOut]
    author: Optional[UserOut] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class RoutePage(BaseModel):
    items: List[RouteListItem]
    total: int
    page: int
    page_size: int
