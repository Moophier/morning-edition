# Hiking World Routes MVP - Design Specification

**Date**: 2025-06-23  
**Project**: 世界徒步路线图鉴 MVP  
**Status**: Approved

---

## 1. Overview

从零到一构建世界徒步路线展示与创建平台。用户可以浏览、搜索、创建徒步路线，支持 8 大类标签系统、实时地图、季节日历等功能。

**技术栈**: Next.js 15 (前端) + FastAPI (后端) + SQLite (数据库) + NextAuth.js (认证)

---

## 2. Architecture

```
hiking-world-routes/
├── frontend/              # Next.js 15 App Router
│   ├── app/
│   │   ├── page.tsx           # 首页 - 路线列表/搜索
│   │   ├── routes/[id]/       # 路线详情页
│   │   ├── create/            # 创建路线
│   │   ├── edit/[id]/         # 编辑路线
│   │   └── auth/              # 登录/注册
│   ├── components/
│   │   ├── ui/                # shadcn/ui 组件
│   │   ├── TagSystem/         # 8类标签组件
│   │   ├── RouteCard/         # 路线卡片
│   │   ├── MapView/           # Leaflet 地图
│   │   └── SeasonCalendar/   # 季节日历
│   └── lib/
│       └── api.ts             # API 调用封装
│
├── backend/               # FastAPI
│   ├── main.py
│   ├── models/            # Pydantic 模型
│   ├── routers/
│   │   ├── routes.py          # 路线 CRUD
│   │   ├── tags.py           # 标签查询
│   │   └── auth.py           # 认证
│   └── db/
│       ├── schema.prisma     # 数据模型
│       └── sqlite.db         # SQLite 数据库
```

---

## 3. Data Model

### Route (路线)
| Field | Type | Description |
|-------|------|-------------|
| id | string (UUID) | 主键 |
| name | string | 路线名称 |
| slug | string | URL-friendly 标识 |
| description | text | 路线描述 |
| difficulty | int (1-4) | 难度等级 |
| cost_level | int (1-3) | 消费水平 |
| region | string | 所属大区 |
| season_calendar | json | 12个月份最佳/良好标记 |
| route_coords | json | 经纬度坐标数组 |
| elevation_profile | json | 海拔剖面数据 |
| tags | relation (many-to-many) | 关联标签 |
| days | json | 每天行程数组 |
| gallery | json | 图片URL数组 |
| author_id | string → User | 作者 |
| created_at | datetime | 创建时间 |
| updated_at | datetime | 更新时间 |

### Tag (标签)
| Field | Type | Description |
|-------|------|-------------|
| id | string | 主键 |
| name | string | 中文名称 |
| name_en | string | 英文名称 |
| category | enum | ls/et/fd/ar/pl/pr/hi/mu |
| color_hex | string | 前景色 |
| bg_rgba | string | 背景色 |

**Category 分类**:
- `ls` - 景观 (Landscape)
- `et` - 民族 (Ethnic)
- `fd` - 饮食 (Food)
- `ar` - 建筑 (Architecture)
- `pl` - 植物 (Plant)
- `pr` - 特产 (Product)
- `hi` - 历史人物 (Historical)
- `mu` - 博物馆 (Museum)

### User (用户)
| Field | Type | Description |
|-------|------|-------------|
| id | string (UUID) | 主键 |
| email | string | 邮箱（唯一） |
| name | string | 显示名称 |
| avatar | string | 头像URL |
| hashed_password | string | 密码哈希 |
| routes | relation (one-to-many) | 创建的路线 |
| created_at | datetime | 注册时间 |

---

## 4. API Endpoints

### Routes
| Method | Endpoint | Auth | Description |
|--------|----------|------|-------------|
| GET | `/api/routes` | No | 列表 + 筛选/分页 |
| GET | `/api/routes/{id}` | No | 路线详情 |
| GET | `/api/routes/{slug}` | No | 按 slug 获取 |
| POST | `/api/routes` | Yes | 创建路线 |
| PUT | `/api/routes/{id}` | Yes (作者) | 更新路线 |
| DELETE | `/api/routes/{id}` | Yes (作者) | 删除路线 |

**筛选参数**: `difficulty`, `cost_level`, `region`, `tags`, `season`, `search`

### Tags
| Method | Endpoint | Auth | Description |
|--------|----------|------|-------------|
| GET | `/api/tags` | No | 所有标签 |
| GET | `/api/tags/categories` | No | 按分类获取 |

### Auth
| Method | Endpoint | Auth | Description |
|--------|----------|------|-------------|
| POST | `/api/auth/register` | No | 注册 |
| POST | `/api/auth/login` | No | 登录 |
| GET | `/api/auth/me` | Yes | 当前用户 |
| POST | `/api/auth/logout` | Yes | 登出 |

---

## 5. Frontend Pages

### 首页 (/)
- 路线卡片列表（网格布局）
- 筛选器：难度/地区/消费/标签/季节
- 搜索框：全文搜索
- 排序：最新/难度/地区

### 路线详情页 (/routes/[id])
完全匹配提供的虎跳峡模板:
- Hero 大图
- 概览数据（天数/里程/难度/爬升）
- 季节日历
- 实时交互地图（Leaflet）
- 海拔剖面图
- 行程详情（每天）
- 图库画廊
- 文化/历史
- 自然生态
- 住宿餐饮
- 装备清单
- 相关标签

### 创建路线 (/create)
- 多步骤表单
- 基础信息（名称/描述/难度/消费/地区）
- 地图选点（添加途经点）
- 标签选择（8 类标签）
- 行程规划（每天描述）
- 预览发布

### 编辑路线 (/edit/[id])
- 同创建表单，预填充数据
- 仅作者可访问

### 认证 (/auth)
- 登录/注册页面
- NextAuth.js 支持邮箱+密码

---

## 6. MVP Feature Scope

### 第一版 (MVP)
- ✅ 路线列表 + 筛选（难度/地区/标签/季节）
- ✅ 路线详情页（完全匹配设计模板）
- ✅ 创建/编辑路线
- ✅ 用户注册/登录（NextAuth.js）
- ✅ 8 类标签系统
- ✅ 实时地图（Leaflet + OpenStreetMap）
- ✅ 难度仪表/消费星级
- ✅ 季节日历

### 后续版本
- ❌ 评论/收藏功能
- ❌ 用户个人主页
- ❌ 路线浏览量统计
- ❌ 图片上传（目前用 URL）
- ❌ 更多筛选维度

---

## 7. UI Design System

### 颜色变量
```css
--accent: #c9a24e        /* 主强调色 - 金色 */
--accent2: #e0b85c       /* 强调色变体 */
--accent3: #5a9e7a       /* 辅助绿 */
--accent4: #b86b4a       /* 警告色 */
--accent5: #6888cc       /* 信息蓝 */
--bg: #060a08            /* 主背景 */
--surface: #0f1713       /* 卡片背景 */
--text: #e2ddd4          /* 主文字 */
--text-dim: #8a9a8e      /* 次要文字 */
--text-muted: #4a5a4e    /* 弱化文字 */
```

### 标签配色
| Category | 背景 | 前景色 |
|----------|------|--------|
| 景观 (ls) | rgba(90,200,120,.1) | #7aeaa0 |
| 民族 (et) | rgba(180,120,255,.12) | #c49eff |
| 饮食 (fd) | rgba(255,190,90,.12) | #ffc060 |
| 建筑 (ar) | rgba(230,220,90,.1) | #e8e060 |
| 植物 (pl) | rgba(90,230,120,.08) | #60e880 |
| 特产 (pr) | rgba(255,150,90,.12) | #ff9a60 |
| 历史 (hi) | rgba(255,120,120,.12) | #ff8080 |
| 博物馆 (mu) | rgba(120,170,255,.12) | #80b0ff |

---

## 8. Development Timeline

**预计总周期**: 2-3 周

**第一周**: 项目初始化 + 基础架构
- Next.js + FastAPI 项目搭建
- 数据库 Schema 设计
- 基础 API CRUD
- 用户认证流程

**第二周**: 前端核心功能
- 路线列表 + 筛选
- 路线详情页
- 创建/编辑表单
- 地图组件集成

**第三周**: 完善与优化
- 标签系统完善
- 响应式适配
- 细节打磨
- 测试与修复

---

## 9. Dependencies

### Frontend
- Next.js 15
- React 19
- TailwindCSS
- shadcn/ui
- Leaflet + react-leaflet
- NextAuth.js
- Lucide Icons

### Backend
- FastAPI
- Pydantic v2
- SQLAlchemy
- SQLite (aiosqlite)
- python-jose (JWT)
- passlib[bcrypt]

---

## 10. Out of Scope (MVP)

- 评论、收藏功能
- 图片上传（暂时用 URL）
- 邮件通知
- 管理员后台
- 多语言国际化（UI）
- 离线 PWA
- 移动端原生 App