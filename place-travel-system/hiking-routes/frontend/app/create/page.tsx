"use client";

import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import { api } from "@/lib/api";
import { useAuth } from "@/lib/auth";

interface Tag { id: string; name: string; category: string; color_hex: string; bg_rgba: string; }
interface TagCategory { category: string; tags: Tag[]; }

const CATEGORY_LABELS: Record<string, string> = {
  ls: "景观", et: "民族", fd: "饮食", ar: "建筑",
  pl: "植物", pr: "特产", hi: "历史", mu: "博物馆",
};

const MONTHS = ["1月","2月","3月","4月","5月","6月","7月","8月","9月","10月","11月","12月"];

export default function CreateRoutePage() {
  const router = useRouter();
  const { user } = useAuth();

  const [name, setName] = useState("");
  const [description, setDescription] = useState("");
  const [difficulty, setDifficulty] = useState(2);
  const [costLevel, setCostLevel] = useState(1);
  const [region, setRegion] = useState("");
  const [durationDays, setDurationDays] = useState("");
  const [distanceKm, setDistanceKm] = useState(0);
  const [cumulativeClimb, setCumulativeClimb] = useState(0);
  const [maxElevation, setMaxElevation] = useState(0);
  const [heroImage, setHeroImage] = useState("");
  const [seasonCal, setSeasonCal] = useState<number[]>(Array(12).fill(0));
  const [selectedTagIds, setSelectedTagIds] = useState<string[]>([]);
  const [categories, setCategories] = useState<TagCategory[]>([]);
  const [saving, setSaving] = useState(false);
  const [error, setError] = useState("");

  useEffect(() => {
    if (!user) { router.push("/auth/login"); return; }
    api.listCategories().then(setCategories).catch(console.error);
  }, [user, router]);

  const toggleTag = (id: string) => {
    setSelectedTagIds(prev => prev.includes(id) ? prev.filter(t => t !== id) : [...prev, id]);
  };

  const toggleSeason = (i: number) => {
    setSeasonCal(prev => {
      const next = [...prev];
      next[i] = next[i] === 2 ? 0 : next[i] + 1;
      return next;
    });
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!name.trim()) { setError("请输入路线名称"); return; }
    setSaving(true);
    try {
      const res = await api.createRoute({
        name, description, difficulty, cost_level: costLevel, region,
        season_calendar: seasonCal, duration_days: durationDays,
        distance_km: distanceKm, cumulative_climb: cumulativeClimb,
        max_elevation: maxElevation, hero_image: heroImage,
        route_coords: [], elevation_profile: [], days: [], gallery: [],
        tag_ids: selectedTagIds,
      });
      router.push(`/routes/${res.id}`);
    } catch (err: any) {
      setError(err.message);
    } finally {
      setSaving(false);
    }
  };

  return (
    <main className="pt-20 pb-20 px-6" style={{ background: "#060a08", minHeight: "100vh" }}>
      <div className="max-w-[700px] mx-auto">
        <h1 className="font-display text-3xl font-bold mb-1">创建路线</h1>
        <p className="text-sm text-text-dim mb-8">填写路线基本信息，标签和多步行程可在创建后编辑</p>

        <form onSubmit={handleSubmit} className="space-y-6">

          <div>
            <label className="block font-mono text-[10px] text-text-muted tracking-widest uppercase mb-2">路线名称 *</label>
            <input type="text" value={name} onChange={e => setName(e.target.value)}
              className="w-full px-4 py-2.5 rounded-[8px] border border-[#1c2e22] bg-[#0f1713] text-text text-sm outline-none focus:border-[#c9a24e] transition-colors" required />
          </div>

          <div>
            <label className="block font-mono text-[10px] text-text-muted tracking-widest uppercase mb-2">描述</label>
            <textarea value={description} onChange={e => setDescription(e.target.value)} rows={3}
              className="w-full px-4 py-2.5 rounded-[8px] border border-[#1c2e22] bg-[#0f1713] text-text text-sm outline-none focus:border-[#c9a24e] transition-colors resize-none" />
          </div>

          <div>
            <label className="block font-mono text-[10px] text-text-muted tracking-widest uppercase mb-2">封面图片 URL</label>
            <input type="url" value={heroImage} onChange={e => setHeroImage(e.target.value)}
              className="w-full px-4 py-2.5 rounded-[8px] border border-[#1c2e22] bg-[#0f1713] text-text text-sm outline-none focus:border-[#c9a24e] transition-colors" placeholder="https://images.unsplash.com/..." />
          </div>

          <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
            <div>
              <label className="block font-mono text-[10px] text-text-muted tracking-widest uppercase mb-2">天数</label>
              <input type="text" value={durationDays} onChange={e => setDurationDays(e.target.value)}
                className="w-full px-3 py-2 rounded-[8px] border border-[#1c2e22] bg-[#0f1713] text-text text-sm outline-none focus:border-[#c9a24e] transition-colors" placeholder="2-3天" />
            </div>
            <div>
              <label className="block font-mono text-[10px] text-text-muted tracking-widest uppercase mb-2">距离(km)</label>
              <input type="number" value={distanceKm || ""} onChange={e => setDistanceKm(Number(e.target.value))}
                className="w-full px-3 py-2 rounded-[8px] border border-[#1c2e22] bg-[#0f1713] text-text text-sm outline-none focus:border-[#c9a24e] transition-colors" />
            </div>
            <div>
              <label className="block font-mono text-[10px] text-text-muted tracking-widest uppercase mb-2">爬升(m)</label>
              <input type="number" value={cumulativeClimb || ""} onChange={e => setCumulativeClimb(Number(e.target.value))}
                className="w-full px-3 py-2 rounded-[8px] border border-[#1c2e22] bg-[#0f1713] text-text text-sm outline-none focus:border-[#c9a24e] transition-colors" />
            </div>
            <div>
              <label className="block font-mono text-[10px] text-text-muted tracking-widest uppercase mb-2">最高海拔(m)</label>
              <input type="number" value={maxElevation || ""} onChange={e => setMaxElevation(Number(e.target.value))}
                className="w-full px-3 py-2 rounded-[8px] border border-[#1c2e22] bg-[#0f1713] text-text text-sm outline-none focus:border-[#c9a24e] transition-colors" />
            </div>
          </div>

          <div className="grid grid-cols-3 gap-4">
            <div>
              <label className="block font-mono text-[10px] text-text-muted tracking-widest uppercase mb-2">难度</label>
              <select value={difficulty} onChange={e => setDifficulty(Number(e.target.value))}
                className="w-full px-3 py-2.5 rounded-[8px] border border-[#1c2e22] bg-[#0f1713] text-text text-sm outline-none focus:border-[#c9a24e] transition-colors">
                {[{v:1,l:"简单"},{v:2,l:"中等"},{v:3,l:"困难"},{v:4,l:"专业"}].map(o => <option key={o.v} value={o.v}>{o.l}</option>)}
              </select>
            </div>
            <div>
              <label className="block font-mono text-[10px] text-text-muted tracking-widest uppercase mb-2">消费</label>
              <select value={costLevel} onChange={e => setCostLevel(Number(e.target.value))}
                className="w-full px-3 py-2.5 rounded-[8px] border border-[#1c2e22] bg-[#0f1713] text-text text-sm outline-none focus:border-[#c9a24e] transition-colors">
                {[{v:1,l:"低"},{v:2,l:"中"},{v:3,l:"高"}].map(o => <option key={o.v} value={o.v}>{o.l}</option>)}
              </select>
            </div>
            <div>
              <label className="block font-mono text-[10px] text-text-muted tracking-widest uppercase mb-2">大区</label>
              <select value={region} onChange={e => setRegion(e.target.value)}
                className="w-full px-3 py-2.5 rounded-[8px] border border-[#1c2e22] bg-[#0f1713] text-text text-sm outline-none focus:border-[#c9a24e] transition-colors">
                {["西南","西北","华南","华东","华中","华北","东北","海外"].map(r => <option key={r} value={r}>{r}</option>)}
              </select>
            </div>
          </div>

          <div>
            <label className="block font-mono text-[10px] text-text-muted tracking-widest uppercase mb-3">最佳季节（点击切换: 灰色→佳→最佳）</label>
            <div className="flex gap-1">
              {MONTHS.map((m, i) => {
                const v = seasonCal[i];
                return (
                  <button key={i} type="button" onClick={() => toggleSeason(i)}
                    className={`flex-1 h-10 rounded-[6px] text-[10px] font-mono transition-all ${
                      v === 2 ? "bg-[rgba(200,162,78,.18)] border border-[rgba(200,162,78,.3)] text-[#c9a24e] font-semibold"
                      : v === 1 ? "bg-[rgba(90,158,122,.1)] border border-[rgba(90,158,122,.2)] text-[#5a9e7a]"
                      : "bg-transparent border border-[#1c2e22] text-text-muted"
                    }`}>
                    {m}
                  </button>
                );
              })}
            </div>
          </div>

          <div>
            <label className="block font-mono text-[10px] text-text-muted tracking-widest uppercase mb-3">标签（点击选择）</label>
            <div className="space-y-3">
              {categories.map(cat => (
                <div key={cat.category} className="flex flex-wrap gap-1.5 items-center">
                  <span className="font-mono text-[10px] text-text-muted w-10 shrink-0">{CATEGORY_LABELS[cat.category] || cat.category}</span>
                  {cat.tags.map(t => (
                    <button key={t.id} type="button" onClick={() => toggleTag(t.id)}
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

          {error && <p className="text-sm text-[#cc4444]">{error}</p>}

          <button type="submit" disabled={saving}
            className="w-full py-3 rounded-[8px] bg-[#c9a24e] text-[#060a08] font-semibold text-sm hover:bg-[#e0b85c] transition-all disabled:opacity-50">
            {saving ? "保存中..." : "创建路线"}
          </button>
        </form>
      </div>
    </main>
  );
}
