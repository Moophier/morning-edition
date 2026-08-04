"use client";

import { useEffect, useState } from "react";
import { useParams, useRouter } from "next/navigation";
import { api } from "@/lib/api";
import { useAuth } from "@/lib/auth";

export default function EditRoutePage() {
  const { id } = useParams();
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
  const [selectedTagIds, setSelectedTagIds] = useState<string[]>([]);
  const [categories, setCategories] = useState<any[]>([]);
  const [saving, setSaving] = useState(false);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    if (!user) { router.push("/auth/login"); return; }
    Promise.all([
      api.getRoute(id as string),
      api.listCategories(),
    ]).then(([route, cats]) => {
      setName(route.name);
      setDescription(route.description);
      setDifficulty(route.difficulty);
      setCostLevel(route.cost_level);
      setRegion(route.region);
      setDurationDays(route.duration_days);
      setDistanceKm(route.distance_km);
      setCumulativeClimb(route.cumulative_climb);
      setMaxElevation(route.max_elevation);
      setHeroImage(route.hero_image);
      setSelectedTagIds(route.tags.map((t: any) => t.id));
      setCategories(cats);
    }).catch(console.error).finally(() => setLoading(false));
  }, [id, user, router]);

  const toggleTag = (tagId: string) => {
    setSelectedTagIds(prev => prev.includes(tagId) ? prev.filter(t => t !== tagId) : [...prev, tagId]);
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setSaving(true);
    try {
      await api.updateRoute(id as string, {
        name, description, difficulty, cost_level: costLevel, region,
        season_calendar: [], duration_days: durationDays,
        distance_km: distanceKm, cumulative_climb: cumulativeClimb,
        max_elevation: maxElevation, hero_image: heroImage,
        route_coords: [], elevation_profile: [], days: [], gallery: [],
        tag_ids: selectedTagIds,
      });
      router.push(`/routes/${id}`);
    } catch (err: any) {
      setError(err.message);
    } finally {
      setSaving(false);
    }
  };

  if (loading) return <div className="min-h-screen flex items-center justify-center"><p className="text-text-muted font-mono text-xs tracking-widest">LOADING</p></div>;

  return (
    <main className="pt-20 pb-20 px-6" style={{ background: "#060a08", minHeight: "100vh" }}>
      <div className="max-w-[700px] mx-auto">
        <h1 className="font-display text-3xl font-bold mb-8">编辑路线</h1>
        <form onSubmit={handleSubmit} className="space-y-6">
          <div>
            <label className="block font-mono text-[10px] text-text-muted tracking-widest uppercase mb-2">路线名称</label>
            <input type="text" value={name} onChange={e => setName(e.target.value)}
              className="w-full px-4 py-2.5 rounded-[8px] border border-[#1c2e22] bg-[#0f1713] text-text text-sm outline-none focus:border-[#c9a24e] transition-colors" required />
          </div>
          <div>
            <label className="block font-mono text-[10px] text-text-muted tracking-widest uppercase mb-2">描述</label>
            <textarea value={description} onChange={e => setDescription(e.target.value)} rows={3}
              className="w-full px-4 py-2.5 rounded-[8px] border border-[#1c2e22] bg-[#0f1713] text-text text-sm outline-none focus:border-[#c9a24e] transition-colors resize-none" />
          </div>
          <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
            <div>
              <label className="block font-mono text-[10px] text-text-muted tracking-widest uppercase mb-2">天数</label>
              <input type="text" value={durationDays} onChange={e => setDurationDays(e.target.value)}
                className="w-full px-3 py-2 rounded-[8px] border border-[#1c2e22] bg-[#0f1713] text-text text-sm outline-none focus:border-[#c9a24e] transition-colors" />
            </div>
            <div>
              <label className="block font-mono text-[10px] text-text-muted tracking-widest uppercase mb-2">距离(km)</label>
              <input type="number" value={distanceKm || ""} onChange={e => setDistanceKm(Number(e.target.value))}
                className="w-full px-3 py-2 rounded-[8px] border border-[#1c2e22] bg-[#0f1713] text-text text-sm outline-none focus:border-[#c9a24e] transition-colors" />
            </div>
            <div>
              <label className="block font-mono text-[10px] text-text-muted tracking-widest uppercase mb-2">难度</label>
              <select value={difficulty} onChange={e => setDifficulty(Number(e.target.value))}
                className="w-full px-3 py-2.5 rounded-[8px] border border-[#1c2e22] bg-[#0f1713] text-text text-sm outline-none focus:border-[#c9a24e] transition-colors">
                {[{v:1,l:"简单"},{v:2,l:"中等"},{v:3,l:"困难"},{v:4,l:"专业"}].map(o => <option key={o.v} value={o.v}>{o.l}</option>)}
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
            <label className="block font-mono text-[10px] text-text-muted tracking-widest uppercase mb-3">标签</label>
            <div className="space-y-3">
              {categories.map((cat: any) => (
                <div key={cat.category} className="flex flex-wrap gap-1.5 items-center">
                  <span className="font-mono text-[10px] text-text-muted w-10 shrink-0">{cat.category}</span>
                  {cat.tags.map((t: any) => (
                    <button key={t.id} type="button" onClick={() => toggleTag(t.id)}
                      className={`text-[11px] px-2 py-0.5 rounded-[10px] transition-all ${selectedTagIds.includes(t.id) ? "ring-2 ring-[#c9a24e] scale-105" : ""}`}
                      style={{ background: t.bg_rgba, color: t.color_hex }}>
                      {t.name}
                    </button>
                  ))}
                </div>
              ))}
            </div>
          </div>
          {error && <p className="text-sm text-[#cc4444]">{error}</p>}
          <div className="flex gap-3">
            <button type="submit" disabled={saving}
              className="flex-1 py-3 rounded-[8px] bg-[#c9a24e] text-[#060a08] font-semibold text-sm hover:bg-[#e0b85c] transition-all disabled:opacity-50">
              {saving ? "保存中..." : "保存修改"}
            </button>
            <button type="button" onClick={() => router.push(`/routes/${id}`)}
              className="px-6 py-3 rounded-[8px] border border-[#1c2e22] text-text-dim text-sm hover:border-[#c9a24e] transition-all">
              取消
            </button>
          </div>
        </form>
      </div>
    </main>
  );
}
