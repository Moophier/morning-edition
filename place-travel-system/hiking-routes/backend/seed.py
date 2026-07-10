import asyncio
from pathlib import Path

import sys

sys.path.insert(0, str(Path(__file__).parent))

from database import init_db, async_session
from models import Tag, Route, User
from passlib.hash import bcrypt

CATEGORY_STYLES = {
    "ls": {"color_hex": "#7aeaa0", "bg_rgba": "rgba(90,200,120,.1)"},
    "et": {"color_hex": "#c49eff", "bg_rgba": "rgba(180,120,255,.12)"},
    "fd": {"color_hex": "#ffc060", "bg_rgba": "rgba(255,190,90,.12)"},
    "ar": {"color_hex": "#e8e060", "bg_rgba": "rgba(230,220,90,.1)"},
    "pl": {"color_hex": "#60e880", "bg_rgba": "rgba(90,230,120,.08)"},
    "pr": {"color_hex": "#ff9a60", "bg_rgba": "rgba(255,150,90,.12)"},
    "hi": {"color_hex": "#ff8080", "bg_rgba": "rgba(255,120,120,.12)"},
    "mu": {"color_hex": "#80b0ff", "bg_rgba": "rgba(120,170,255,.12)"},
}

TAGS_DATA = [
    ("雪山", "Snow Mountain", "ls"),
    ("峡谷", "Canyon", "ls"),
    ("冰川", "Glacier", "ls"),
    ("原始森林", "Forest", "ls"),
    ("瀑布", "Waterfall", "ls"),
    ("高山湖泊", "Alpine Lake", "ls"),
    ("草甸", "Meadow", "ls"),
    ("云海", "Sea of Clouds", "ls"),
    ("丹霞", "Danxia", "ls"),
    ("海岸", "Coast", "ls"),
    ("沙漠", "Desert", "ls"),
    ("喀斯特", "Karst", "ls"),
    ("火山", "Volcanic", "ls"),
    ("湿地", "Wetland", "ls"),
    ("花海", "Flower Sea", "ls"),
    ("藏族", "Tibetan", "et"),
    ("彝族", "Yi", "et"),
    ("苗族", "Miao", "et"),
    ("纳西族", "Naxi", "et"),
    ("蒙古族", "Mongolian", "et"),
    ("哈萨克族", "Kazakh", "et"),
    ("图瓦人", "Tuvan", "et"),
    ("酥油茶", "Butter Tea", "fd"),
    ("牦牛肉", "Yak Meat", "fd"),
    ("手抓羊肉", "Hand-grabbed Lamb", "fd"),
    ("酸汤鱼", "Sour Fish Soup", "fd"),
    ("烤全羊", "Roast Lamb", "fd"),
    ("藏式碉房", "Tibetan Tower", "ar"),
    ("蒙古包", "Yurt", "ar"),
    ("吊脚楼", "Stilt House", "ar"),
    ("寺庙", "Temple", "ar"),
    ("风雨桥", "Wind-Rain Bridge", "ar"),
    ("高山杜鹃", "Alpine Rhododendron", "pl"),
    ("冷杉", "Fir", "pl"),
    ("白桦", "Birch", "pl"),
    ("胡杨", "Populus Euphratica", "pl"),
    ("银杏", "Ginkgo", "pl"),
    ("松茸", "Matsutake", "pr"),
    ("普洱茶", "Pu'er Tea", "pr"),
    ("虫草", "Caterpillar Fungus", "pr"),
    ("苗族银饰", "Miao Silver", "pr"),
    ("约瑟夫·洛克", "Joseph Rock", "hi"),
    ("徐霞客", "Xu Xiake", "hi"),
    ("玄奘", "Xuanzang", "hi"),
    ("成吉思汗", "Genghis Khan", "hi"),
    ("文成公主", "Princess Wencheng", "hi"),
    ("敦煌莫高窟", "Mogao Caves", "mu"),
    ("博物馆", "Museum", "mu"),
]

TAGS: list[dict] = [
    {"name": cn, "name_en": en, "category": cat, **CATEGORY_STYLES[cat]}
    for cn, en, cat in TAGS_DATA
]

SAMPLE_ROUTE = {
    "name": "虎跳峡高路徒步",
    "slug": "tiger-leaping-gorge",
    "description": "世界最深峡谷之一，玉龙雪山与哈巴雪山之间，金沙江劈开的壮美走廊。",
    "difficulty": 2,
    "cost_level": 1,
    "region": "西南",
    "duration_days": "2-3天",
    "distance_km": 23,
    "cumulative_climb": 1500,
    "max_elevation": 2670,
    "season_calendar": [0, 0, 1, 2, 2, 1, 0, 0, 2, 2, 2, 0],
    "route_coords": [
        [27.183, 100.055],
        [27.168, 100.072],
        [27.158, 100.085],
        [27.150, 100.095],
        [27.140, 100.108],
        [27.125, 100.122],
        [27.115, 100.135],
        [27.050, 100.185],
    ],
    "gallery": [],
    "hero_image": "https://images.unsplash.com/photo-1506905925346-21bda4d32df4?auto=format&fit=crop&w=1200&q=80",
    "tag_ids": [1, 2],
}


async def seed():
    await init_db()
    async with async_session() as session:
        existing = await session.get(Tag, "1")
        if existing:
            print("DB already seeded")
            return

        for i, t in enumerate(TAGS):
            tag = Tag(id=str(i + 1), **t)
            session.add(tag)

        user = User(
            id="demo-user",
            email="demo@hiking.com",
            name="Demo User",
            hashed_password=bcrypt.hash("demo123"),
        )
        session.add(user)
        await session.flush()

        route = Route(
            id="route-tiger-leaping",
            name=SAMPLE_ROUTES[0]["name"],
            slug=SAMPLE_ROUTES[0]["slug"],
            description=SAMPLE_ROUTES[0]["description"],
            difficulty=SAMPLE_ROUTES[0]["difficulty"],
            cost_level=SAMPLE_ROUTES[0]["cost_level"],
            region=SAMPLE_ROUTES[0]["region"],
            duration_days=SAMPLE_ROUTES[0]["duration_days"],
            distance_km=SAMPLE_ROUTES[0]["distance_km"],
            cumulative_climb=SAMPLE_ROUTES[0]["cumulative_climb"],
            max_elevation=SAMPLE_ROUTES[0]["max_elevation"],
            season_calendar=SAMPLE_ROUTES[0]["season_calendar"],
            route_coords=SAMPLE_ROUTES[0]["route_coords"],
            gallery=SAMPLE_ROUTES[0]["gallery"],
            hero_image=SAMPLE_ROUTES[0]["hero_image"],
            author_id="demo-user",
        )
        tag1 = await session.get(Tag, "1")
        tag2 = await session.get(Tag, "2")
        if tag1:
            route.tags.append(tag1)
        if tag2:
            route.tags.append(tag2)
        session.add(route)

        await session.commit()
        print("Seed complete: 48 tags + 1 demo user + 1 sample route")


if __name__ == "__main__":
    asyncio.run(seed())
