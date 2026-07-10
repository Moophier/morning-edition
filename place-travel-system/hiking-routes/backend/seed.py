import asyncio
import sys

sys.path.insert(0, r"C:\Users\X\place-travel-system\hiking-routes\backend")

from database import init_db, async_session
from models import Tag, Route, User
from passlib.hash import bcrypt

TAGS = [
    # 景观 (ls)
    {
        "name": "雪山",
        "name_en": "Snow Mountain",
        "category": "ls",
        "color_hex": "#7aeaa0",
        "bg_rgba": "rgba(90,200,120,.1)",
    },
    {
        "name": "峡谷",
        "name_en": "Canyon",
        "category": "ls",
        "color_hex": "#7aeaa0",
        "bg_rgba": "rgba(90,200,120,.1)",
    },
    {
        "name": "冰川",
        "name_en": "Glacier",
        "category": "ls",
        "color_hex": "#7aeaa0",
        "bg_rgba": "rgba(90,200,120,.1)",
    },
    {
        "name": "原始森林",
        "name_en": "Forest",
        "category": "ls",
        "color_hex": "#7aeaa0",
        "bg_rgba": "rgba(90,200,120,.1)",
    },
    {
        "name": "瀑布",
        "name_en": "Waterfall",
        "category": "ls",
        "color_hex": "#7aeaa0",
        "bg_rgba": "rgba(90,200,120,.1)",
    },
    {
        "name": "高山湖泊",
        "name_en": "Alpine Lake",
        "category": "ls",
        "color_hex": "#7aeaa0",
        "bg_rgba": "rgba(90,200,120,.1)",
    },
    {
        "name": "草甸",
        "name_en": "Meadow",
        "category": "ls",
        "color_hex": "#7aeaa0",
        "bg_rgba": "rgba(90,200,120,.1)",
    },
    {
        "name": "云海",
        "name_en": "Sea of Clouds",
        "category": "ls",
        "color_hex": "#7aeaa0",
        "bg_rgba": "rgba(90,200,120,.1)",
    },
    {
        "name": "丹霞",
        "name_en": "Danxia",
        "category": "ls",
        "color_hex": "#7aeaa0",
        "bg_rgba": "rgba(90,200,120,.1)",
    },
    {
        "name": "海岸",
        "name_en": "Coast",
        "category": "ls",
        "color_hex": "#7aeaa0",
        "bg_rgba": "rgba(90,200,120,.1)",
    },
    {
        "name": "沙漠",
        "name_en": "Desert",
        "category": "ls",
        "color_hex": "#7aeaa0",
        "bg_rgba": "rgba(90,200,120,.1)",
    },
    {
        "name": "喀斯特",
        "name_en": "Karst",
        "category": "ls",
        "color_hex": "#7aeaa0",
        "bg_rgba": "rgba(90,200,120,.1)",
    },
    {
        "name": "火山",
        "name_en": "Volcanic",
        "category": "ls",
        "color_hex": "#7aeaa0",
        "bg_rgba": "rgba(90,200,120,.1)",
    },
    {
        "name": "湿地",
        "name_en": "Wetland",
        "category": "ls",
        "color_hex": "#7aeaa0",
        "bg_rgba": "rgba(90,200,120,.1)",
    },
    {
        "name": "花海",
        "name_en": "Flower Sea",
        "category": "ls",
        "color_hex": "#7aeaa0",
        "bg_rgba": "rgba(90,200,120,.1)",
    },
    # 民族 (et)
    {
        "name": "藏族",
        "name_en": "Tibetan",
        "category": "et",
        "color_hex": "#c49eff",
        "bg_rgba": "rgba(180,120,255,.12)",
    },
    {
        "name": "彝族",
        "name_en": "Yi",
        "category": "et",
        "color_hex": "#c49eff",
        "bg_rgba": "rgba(180,120,255,.12)",
    },
    {
        "name": "苗族",
        "name_en": "Miao",
        "category": "et",
        "color_hex": "#c49eff",
        "bg_rgba": "rgba(180,120,255,.12)",
    },
    {
        "name": "纳西族",
        "name_en": "Naxi",
        "category": "et",
        "color_hex": "#c49eff",
        "bg_rgba": "rgba(180,120,255,.12)",
    },
    {
        "name": "蒙古族",
        "name_en": "Mongolian",
        "category": "et",
        "color_hex": "#c49eff",
        "bg_rgba": "rgba(180,120,255,.12)",
    },
    {
        "name": "哈萨克族",
        "name_en": "Kazakh",
        "category": "et",
        "color_hex": "#c49eff",
        "bg_rgba": "rgba(180,120,255,.12)",
    },
    {
        "name": "图瓦人",
        "name_en": "Tuvan",
        "category": "et",
        "color_hex": "#c49eff",
        "bg_rgba": "rgba(180,120,255,.12)",
    },
    # 饮食 (fd)
    {
        "name": "酥油茶",
        "name_en": "Butter Tea",
        "category": "fd",
        "color_hex": "#ffc060",
        "bg_rgba": "rgba(255,190,90,.12)",
    },
    {
        "name": "牦牛肉",
        "name_en": "Yak Meat",
        "category": "fd",
        "color_hex": "#ffc060",
        "bg_rgba": "rgba(255,190,90,.12)",
    },
    {
        "name": "手抓羊肉",
        "name_en": "Hand-grabbed Lamb",
        "category": "fd",
        "color_hex": "#ffc060",
        "bg_rgba": "rgba(255,190,90,.12)",
    },
    {
        "name": "酸汤鱼",
        "name_en": "Sour Fish Soup",
        "category": "fd",
        "color_hex": "#ffc060",
        "bg_rgba": "rgba(255,190,90,.12)",
    },
    {
        "name": "烤全羊",
        "name_en": "Roast Lamb",
        "category": "fd",
        "color_hex": "#ffc060",
        "bg_rgba": "rgba(255,190,90,.12)",
    },
    # 建筑 (ar)
    {
        "name": "藏式碉房",
        "name_en": "Tibetan Tower",
        "category": "ar",
        "color_hex": "#e8e060",
        "bg_rgba": "rgba(230,220,90,.1)",
    },
    {
        "name": "蒙古包",
        "name_en": "Yurt",
        "category": "ar",
        "color_hex": "#e8e060",
        "bg_rgba": "rgba(230,220,90,.1)",
    },
    {
        "name": "吊脚楼",
        "name_en": "Stilt House",
        "category": "ar",
        "color_hex": "#e8e060",
        "bg_rgba": "rgba(230,220,90,.1)",
    },
    {
        "name": "寺庙",
        "name_en": "Temple",
        "category": "ar",
        "color_hex": "#e8e060",
        "bg_rgba": "rgba(230,220,90,.1)",
    },
    {
        "name": "风雨桥",
        "name_en": "Wind-Rain Bridge",
        "category": "ar",
        "color_hex": "#e8e060",
        "bg_rgba": "rgba(230,220,90,.1)",
    },
    # 植物 (pl)
    {
        "name": "高山杜鹃",
        "name_en": "Alpine Rhododendron",
        "category": "pl",
        "color_hex": "#60e880",
        "bg_rgba": "rgba(90,230,120,.08)",
    },
    {
        "name": "冷杉",
        "name_en": "Fir",
        "category": "pl",
        "color_hex": "#60e880",
        "bg_rgba": "rgba(90,230,120,.08)",
    },
    {
        "name": "白桦",
        "name_en": "Birch",
        "category": "pl",
        "color_hex": "#60e880",
        "bg_rgba": "rgba(90,230,120,.08)",
    },
    {
        "name": "胡杨",
        "name_en": "Populus Euphratica",
        "category": "pl",
        "color_hex": "#60e880",
        "bg_rgba": "rgba(90,230,120,.08)",
    },
    {
        "name": "银杏",
        "name_en": "Ginkgo",
        "category": "pl",
        "color_hex": "#60e880",
        "bg_rgba": "rgba(90,230,120,.08)",
    },
    # 特产 (pr)
    {
        "name": "松茸",
        "name_en": "Matsutake",
        "category": "pr",
        "color_hex": "#ff9a60",
        "bg_rgba": "rgba(255,150,90,.12)",
    },
    {
        "name": "普洱茶",
        "name_en": "Pu'er Tea",
        "category": "pr",
        "color_hex": "#ff9a60",
        "bg_rgba": "rgba(255,150,90,.12)",
    },
    {
        "name": "虫草",
        "name_en": "Caterpillar Fungus",
        "category": "pr",
        "color_hex": "#ff9a60",
        "bg_rgba": "rgba(255,150,90,.12)",
    },
    {
        "name": "苗族银饰",
        "name_en": "Miao Silver",
        "category": "pr",
        "color_hex": "#ff9a60",
        "bg_rgba": "rgba(255,150,90,.12)",
    },
    # 历史人物 (hi)
    {
        "name": "约瑟夫·洛克",
        "name_en": "Joseph Rock",
        "category": "hi",
        "color_hex": "#ff8080",
        "bg_rgba": "rgba(255,120,120,.12)",
    },
    {
        "name": "徐霞客",
        "name_en": "Xu Xiake",
        "category": "hi",
        "color_hex": "#ff8080",
        "bg_rgba": "rgba(255,120,120,.12)",
    },
    {
        "name": "玄奘",
        "name_en": "Xuanzang",
        "category": "hi",
        "color_hex": "#ff8080",
        "bg_rgba": "rgba(255,120,120,.12)",
    },
    {
        "name": "成吉思汗",
        "name_en": "Genghis Khan",
        "category": "hi",
        "color_hex": "#ff8080",
        "bg_rgba": "rgba(255,120,120,.12)",
    },
    {
        "name": "文成公主",
        "name_en": "Princess Wencheng",
        "category": "hi",
        "color_hex": "#ff8080",
        "bg_rgba": "rgba(255,120,120,.12)",
    },
    # 博物馆 (mu)
    {
        "name": "敦煌莫高窟",
        "name_en": "Mogao Caves",
        "category": "mu",
        "color_hex": "#80b0ff",
        "bg_rgba": "rgba(120,170,255,.12)",
    },
    {
        "name": "博物馆",
        "name_en": "Museum",
        "category": "mu",
        "color_hex": "#80b0ff",
        "bg_rgba": "rgba(120,170,255,.12)",
    },
]

SAMPLE_ROUTES = [
    {
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
        "tag_ids": [],
    }
]


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
