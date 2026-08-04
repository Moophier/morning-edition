import uuid
from datetime import datetime
from sqlalchemy import (
    Column,
    String,
    Text,
    Integer,
    Float,
    DateTime,
    ForeignKey,
    Table,
    JSON,
)
from sqlalchemy.orm import relationship
from database import Base

# Association table: route <-> tag
route_tag = Table(
    "route_tag",
    Base.metadata,
    Column(
        "route_id",
        String(36),
        ForeignKey("routes.id", ondelete="CASCADE"),
        primary_key=True,
    ),
    Column(
        "tag_id",
        String(36),
        ForeignKey("tags.id", ondelete="CASCADE"),
        primary_key=True,
    ),
)


class User(Base):
    __tablename__ = "users"
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    email = Column(String(255), unique=True, nullable=False, index=True)
    name = Column(String(100), nullable=False)
    hashed_password = Column(String(255), nullable=False)
    avatar = Column(String(500), default="")
    created_at = Column(DateTime, default=datetime.utcnow)
    routes = relationship("Route", back_populates="author")


class Tag(Base):
    __tablename__ = "tags"
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    name = Column(String(50), nullable=False)
    name_en = Column(String(50), default="")
    category = Column(String(10), nullable=False, index=True)  # ls/et/fd/ar/pl/pr/hi/mu
    color_hex = Column(String(7), nullable=False)
    bg_rgba = Column(String(30), nullable=False)


class Route(Base):
    __tablename__ = "routes"
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    name = Column(String(200), nullable=False)
    slug = Column(String(200), unique=True, nullable=False, index=True)
    description = Column(Text, default="")
    difficulty = Column(Integer, default=1)  # 1-4
    cost_level = Column(Integer, default=1)  # 1-3
    region = Column(String(50), default="")
    season_calendar = Column(JSON, default=list)  # [0|1|2] x 12 months
    route_coords = Column(JSON, default=list)  # [[lat,lng],...]
    elevation_profile = Column(JSON, default=list)  # [{name, elev},...]
    days = Column(JSON, default=list)  # [{title, desc, ...}]
    gallery = Column(JSON, default=list)  # [url, ...]
    duration_days = Column(String(20), default="")
    distance_km = Column(Float, default=0)
    cumulative_climb = Column(Integer, default=0)
    max_elevation = Column(Integer, default=0)
    hero_image = Column(String(500), default="")
    author_id = Column(String(36), ForeignKey("users.id"), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    author = relationship("User", back_populates="routes")
    tags = relationship("Tag", secondary=route_tag, lazy="selectin")
