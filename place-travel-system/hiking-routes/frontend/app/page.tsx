"use client";

import { useEffect, useState } from "react";
import { api } from "@/lib/api";
import RouteCard from "@/components/RouteCard";

interface Tag { id: string; name: string; name_en: string; category: string; color_hex: string; bg_rgba: string; }
interface TagCategory { category: string; tags: Tag[]; }
interface RouteItem {
  id: string; name: string; slug: string; difficulty: number; cost_level: number;
  region: string; duration_days: string; distance_km: number; hero_image: string;
  tags: Tag[]; author_name: string; created_at: string;
}

const CATEGORY_LABELS: Record<string, string> = {
  ls: "景观", et: "民族", fd: "饮食", ar: "建筑",
  pl: "植物", pr: "特产", hi: "历史", mu: "博物馆",
};
const REGIONS = ["全部", "西南", "西北", "华南", "华东", "华中", "华北", "东北"];

export default function HomePage() {
  const [routes, setRoutes] = useState<RouteItem[]>([]);
  const [total, setTotal] = useState(0);
  const [loading, setLoading] = useState(true);
  const [categories, setCategories] = useState<TagCategory[]>([]);
  const [region, setRegion] = useState("");
  const [difficulty, setDifficulty] = useState("");
  const [search, setSearch] = useState("");
  const [selectedTagIds, setSelectedTagIds] = useState<string[]>([]);
  const [sort, setSort] = useState("newest");
  const [page, setPage] = useState(1);

  useEffect(() => {
    api.listCategories().then(setCategories).catch(console.error);
  }, []);

  useEffect(() => {
    setLoading(true);
    const params: Record<string, string> = { page: String(page), sort };
    if (region) params.region = region;
    if (difficulty) params.difficulty = difficulty;
    if (search) params.search = search;
    if (selectedTagIds.length) params.tag_ids = selectedTagIds.join(",");
    api.listRoutes(params).then(data => {
      setRoutes(data.items);
      setTotal(data.total);
    }).catch(console.error).finally(() => setLoading(false));
  }, [page, region, difficulty, search, selectedTagIds, sort]);

  const toggleTag = (id: string) => {
    setSelectedTagIds(prev => prev.includes(id) ? prev.filter(t => t !== id) : [...prev, id]);
    setPage(1);
  };

  return (
    <main className="pt-16 pb-20">
      {/* Hero */}
      <div className="relative py-16 px-6 text-center overflow-hidden bg-gradient-to-b from-[#060a08] to-[#060a08]">
        <div className="absolute inset-0 pointer-events-none"
          style={{ background: "radial-gradient(ellipse at 30% 40%, rgba(90,158,122,.06) 0%, transparent 55%), radial-gradient(ellipse at 70% 60%, rgba(200,162,78,.04) 0%, transparent 55%)" }} />
        <div className="relative z-[1]">
          <span className="inline-block font-mono text-[11px] tracking-[5px] uppercase text-[#c9a24e] border border-[rgba(200,162,78,.25)] px-6 py-1.5 rounded-full mb-6">Field Guide</span>
          <h1 className="font-display text-[clamp(32px,5.5vw,64px)] font-bold leading-[1.15] mb-3">
            野径<em className="not-italic text-gradient-gold">图鉴</em>
          </h1>
          <p className="text-sm text-text-dim font-light tracking-wider">世界徒步路线 · 百条小众路线</p>
        </div>
      </div>

      <div className="max-w-[1200px] mx-auto px-6">
        {/* Filters */}
        <div className="mb-8 space-y-4">
          {/* Search + Sort */}
          <div className="flex gap-4 flex-wrap items-center">
            <input type="text" placeholder="搜索路线名 / 省份 / 关键字..."
              value={search} onChange={e => { setSearch(e.target.value); setPage(1); }}
              className="flex-1 min-w-[200px] px-4 py-2 rounded-[8px] border border-[#1c2e22] bg-[#0f1713] text-text text-sm outline-none focus:border-[#c9a24e] transition-colors placeholder:text-text-muted" />
            <select value={sort} onChange={e => setSort(e.target.value)}
              className="px-3 py-2 rounded-[8px] border border-[#1c2e22] bg-[#0f1713] text-text text-sm outline-none focus:border-[#c9a24e]">
              <option value="newest">最新</option>
              <option value="oldest">最早</option>
              <option value="difficulty">难度↓</option>
              <option value="distance">距离↓</option>
            </select>
          </div>

          {/* Region */}
          <div className="flex flex-wrap gap-1.5 items-center">
            <span className="font-mono text-[10px] tracking-widest text-text-muted uppercase mr-1">大区</span>
            {REGIONS.map(r => (
              <button key={r} onClick={() => { setRegion(r === "全部" ? "" : r); setPage(1); }}
                className={`px-3 py-1 rounded-full text-xs border transition-all ${
                  (r === "全部" && !region) || region === r
                    ? "bg-[#c9a24e] text-[#060a08] border-[#c9a24e] font-semibold"
                    : "bg-transparent text-text-dim border-[#1c2e22] hover:border-[#c9a24e] hover:text-text"
                }`}>
                {r}
              </button>
            ))}
          </div>

          {/* Difficulty */}
          <div className="flex flex-wrap gap-1.5 items-center">
            <span className="font-mono text-[10px] tracking-widest text-text-muted uppercase mr-1">难度</span>
            {["全部", "1", "2", "3", "4"].map(d => (
              <button key={d} onClick={() => { setDifficulty(d === "全部" ? "" : d); setPage(1); }}
                className={`px-3 py-1 rounded-full text-xs border transition-all ${
                  (d === "全部" && !difficulty) || difficulty === d
                    ? "bg-[#c9a24e] text-[#060a08] border-[#c9a24e] font-semibold"
                    : "bg-transparent text-text-dim border-[#1c2e22] hover:border-[#c9a24e] hover:text-text"
                }`}>
                {d === "1" ? "简单" : d === "2" ? "中等" : d === "3" ? "困难" : d === "4" ? "专业" : "全部"}
              </button>
            ))}
          </div>

          {/* Tags */}
          <div className="space-y-2">
            {categories.map(cat => (
              <div key={cat.category} className="flex flex-wrap gap-1 items-center">
                <span className="font-mono text-[10px] tracking-widest text-text-muted uppercase w-10 shrink-0">
                  {CATEGORY_LABELS[cat.category] || cat.category}
                </span>
                {cat.tags.map(t => (
                  <button key={t.id} onClick={() => toggleTag(t.id)}
                    className={`text-[11px] px-2 py-0.5 rounded-[10px] transition-all ${
                      selectedTagIds.includes(t.id) ? "ring-2 ring-[#c9a24e] scale-105" : ""
                    }`}
                    style={{ background: t.bg_rgba, color: t.color_hex }}>
                    {t.name}
                  </button>
                ))}
              </div>
            ))}
          </div>
        </div>

        {/* Route grid */}
        {loading ? (
          <div className="text-center py-20">
            <div className="w-8 h-8 border-2 border-[#1c2e22] border-t-[#c9a24e] rounded-full animate-spin mx-auto mb-4" />
            <p className="font-mono text-xs text-text-muted tracking-widest">LOADING</p>
          </div>
        ) : routes.length === 0 ? (
          <div className="text-center py-20">
            <p className="text-text-dim text-sm">暂无路线</p>
          </div>
        ) : (
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
            {routes.map(r => <RouteCard key={r.id} route={r} />)}
          </div>
        )}

        {/* Pagination */}
        {total > 20 && (
          <div className="flex justify-center gap-2 mt-10">
            {Array.from({ length: Math.ceil(total / 20) }, (_, i) => (
              <button key={i} onClick={() => setPage(i + 1)}
                className={`w-8 h-8 rounded-[8px] text-xs transition-all ${
                  page === i + 1 ? "bg-[#c9a24e] text-[#060a08] font-semibold" : "border border-[#1c2e22] text-text-dim hover:border-[#c9a24e]"
                }`}>
                {i + 1}
              </button>
            ))}
          </div>
        )}
      </div>
    </main>
  );
}
