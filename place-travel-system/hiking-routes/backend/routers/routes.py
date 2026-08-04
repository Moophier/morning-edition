import uuid
import re
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import select, func, or_
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from database import get_db
from models import Route, Tag
from schemas import (
    RouteCreate,
    RouteUpdate,
    RouteListItem,
    RouteDetail,
    RoutePage,
    TagOut,
)
from routers.auth import get_current_user

router = APIRouter(prefix="/api/routes", tags=["routes"])


def slugify(name: str) -> str:
    s = name.lower().strip()
    s = re.sub(r"[^\w\s-]", "", s)
    s = re.sub(r"[\s_]+", "-", s)
    return s[:200] or "route"


@router.get("", response_model=RoutePage)
async def list_routes(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    difficulty: int | None = Query(None),
    cost_level: int | None = Query(None),
    region: str | None = Query(None),
    search: str | None = Query(None),
    tag_ids: str | None = Query(None),
    sort: str = Query("newest", pattern="^(newest|oldest|difficulty|distance)$"),
    db: AsyncSession = Depends(get_db),
):
    query = select(Route).options(selectinload(Route.tags), selectinload(Route.author))

    if difficulty:
        query = query.where(Route.difficulty == difficulty)
    if cost_level:
        query = query.where(Route.cost_level == cost_level)
    if region:
        query = query.where(Route.region == region)
    if search:
        like = f"%{search}%"
        query = query.where(
            or_(
                Route.name.ilike(like),
                Route.description.ilike(like),
                Route.region.ilike(like),
            )
        )
    if tag_ids:
        ids = [t.strip() for t in tag_ids.split(",") if t.strip()]
        if ids:
            for tid in ids:
                query = query.where(Route.tags.any(Tag.id == tid))

    count_query = select(func.count()).select_from(query.subquery())
    total_result = await db.execute(count_query)
    total = total_result.scalar() or 0

    if sort == "oldest":
        query = query.order_by(Route.created_at.asc())
    elif sort == "difficulty":
        query = query.order_by(Route.difficulty.desc())
    elif sort == "distance":
        query = query.order_by(Route.distance_km.desc())
    else:
        query = query.order_by(Route.created_at.desc())

    offset = (page - 1) * page_size
    query = query.offset(offset).limit(page_size)
    result = await db.execute(query)
    routes = result.scalars().all()

    items = []
    for r in routes:
        author_name = r.author.name if r.author else ""
        items.append(
            RouteListItem(
                id=r.id,
                name=r.name,
                slug=r.slug,
                difficulty=r.difficulty,
                cost_level=r.cost_level,
                region=r.region,
                duration_days=r.duration_days,
                distance_km=r.distance_km,
                hero_image=r.hero_image,
                tags=[TagOut.model_validate(t) for t in r.tags],
                author_name=author_name,
                created_at=r.created_at,
            )
        )

    return RoutePage(items=items, total=total, page=page, page_size=page_size)


@router.get("/{route_id}", response_model=RouteDetail)
async def get_route(route_id: str, db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(Route)
        .options(selectinload(Route.tags), selectinload(Route.author))
        .where(Route.id == route_id)
    )
    route = result.scalar_one_or_none()
    if not route:
        raise HTTPException(status_code=404, detail="Route not found")
    return RouteDetail.model_validate(route)


@router.get("/slug/{slug}", response_model=RouteDetail)
async def get_route_by_slug(slug: str, db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(Route)
        .options(selectinload(Route.tags), selectinload(Route.author))
        .where(Route.slug == slug)
    )
    route = result.scalar_one_or_none()
    if not route:
        raise HTTPException(status_code=404, detail="Route not found")
    return RouteDetail.model_validate(route)


@router.post("", response_model=RouteDetail, status_code=201)
async def create_route(
    data: RouteCreate,
    user=Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    slug = slugify(data.name)
    slug_exists = await db.execute(select(Route).where(Route.slug == slug))
    if slug_exists.scalar_one_or_none():
        slug = f"{slug}-{uuid.uuid4().hex[:6]}"
    route = Route(
        id=str(uuid.uuid4()),
        slug=slug,
        name=data.name,
        description=data.description,
        difficulty=data.difficulty,
        cost_level=data.cost_level,
        region=data.region,
        season_calendar=data.season_calendar,
        route_coords=data.route_coords,
        elevation_profile=data.elevation_profile,
        days=data.days,
        gallery=data.gallery,
        duration_days=data.duration_days,
        distance_km=data.distance_km,
        cumulative_climb=data.cumulative_climb,
        max_elevation=data.max_elevation,
        hero_image=data.hero_image,
        author_id=user.id,
    )
    if data.tag_ids:
        result = await db.execute(select(Tag).where(Tag.id.in_(data.tag_ids)))
        route.tags = list(result.scalars().all())
    db.add(route)
    await db.commit()
    await db.refresh(route)
    result = await db.execute(
        select(Route)
        .options(selectinload(Route.tags), selectinload(Route.author))
        .where(Route.id == route.id)
    )
    route = result.scalar_one()
    return RouteDetail.model_validate(route)


@router.put("/{route_id}", response_model=RouteDetail)
async def update_route(
    route_id: str,
    data: RouteUpdate,
    user=Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(
        select(Route)
        .options(selectinload(Route.tags), selectinload(Route.author))
        .where(Route.id == route_id)
    )
    route = result.scalar_one_or_none()
    if not route:
        raise HTTPException(status_code=404, detail="Route not found")
    if route.author_id != user.id:
        raise HTTPException(status_code=403, detail="Not authorized")

    for field, value in data.model_dump(exclude={"tag_ids"}).items():
        setattr(route, field, value)
    new_slug = slugify(data.name)
    slug_exists = await db.execute(
        select(Route).where(Route.slug == new_slug, Route.id != route.id)
    )
    if slug_exists.scalar_one_or_none():
        new_slug = f"{new_slug}-{uuid.uuid4().hex[:6]}"
    route.slug = new_slug

    if data.tag_ids is not None:
        tag_result = await db.execute(select(Tag).where(Tag.id.in_(data.tag_ids)))
        route.tags = list(tag_result.scalars().all())

    await db.commit()
    await db.refresh(route)
    return RouteDetail.model_validate(route)


@router.delete("/{route_id}", status_code=204)
async def delete_route(
    route_id: str,
    user=Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    route = await db.get(Route, route_id)
    if not route:
        raise HTTPException(status_code=404, detail="Route not found")
    if route.author_id != user.id:
        raise HTTPException(status_code=403, detail="Not authorized")
    await db.delete(route)
    await db.commit()
