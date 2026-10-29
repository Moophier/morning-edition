"use client";

import { useEffect, useState } from "react";
import { useParams } from "next/navigation";
import { api } from "@/lib/api";
import MapView from "@/components/MapView";
import SeasonCalendar from "@/components/SeasonCalendar";
import DifficultyMeter from "@/components/DifficultyMeter";
import CostStars from "@/components/CostStars";
import TagBadge from "@/components/TagBadge";

interface RouteDetail {
  id: string; name: string; slug: string; description: string;
  difficulty: number; cost_level: number; region: string;
  season_calendar: number[]; route_coords: number[][];
  elevation_profile: any[]; days: any[]; gallery: string[];
  duration_days: string; distance_km: number;
  cumulative_climb: number; max_elevation: number;
  hero_image: string;
  tags: Array<{ id: string; name: string; category: string; color_hex: string; bg_rgba: string }>;
  author: { name: string } | null;
  created_at: string; updated_at: string;
}

export default function RouteDetailPage() {
  const { id } = useParams();
  const [route, setRoute] = useState<RouteDetail | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    if (!id) return;
    api.getRoute(id as string).then(setRoute).catch(console.error).finally(() => setLoading(false));
  }, [id]);

  if (loading) return (
    <div className="min-h-screen flex items-center justify-center" style={{ background: "#060a08" }}>
      <div className="text-center">
        <div className="w-8 h-8 border-2 border-[#1c2e22] border-t-[#c9a24e] rounded-full animate-spin mx-auto mb-4" />
        <p className="font-mono text-xs text-text-muted tracking-widest">LOADING</p>
      </div>
    </div>
  );
  if (!route) return (
    <div className="min-h-screen flex items-center justify-center" style={{ background: "#060a08" }}>
      <p className="text-text-dim">路线未找到</p>
    </div>
  );

  const coords = route.route_coords as [number, number][];

  return (
    <main style={{ background: "#060a08", minHeight: "100vh" }}>
      {/* Hero */}
      <div className="relative h-[70vh] min-h-[420px] overflow-hidden">
        {route.hero_image ? (
          <img src={route.hero_image} alt={route.name} className="w-full h-[115%] object-cover object-center brightness-[.55] saturate-[1.15] -mt-[7.5%]" />
        ) : (
          <div className="w-full h-full bg-gradient-to-br from-[#2a1008] via-[#5a2a18] to-[#a05030]" />
        )}
        <div className="absolute inset-0 bg-gradient-to-b from-[rgba(0,0,0,.25)] via-transparent via-55% to-[#060a08]" />
        <div className="absolute bottom-[12%] left-0 right-0 px-6 md:px-12 max-w-[860px] z-[3]">
          <div className="flex flex-wrap gap-2 mb-4">
            <span className="font-mono text-[11px] text-[#c9a24e] tracking-[4px] uppercase flex items-center gap-3">
              <span className="w-11 h-px bg-[#c9a24e]" />{route.region}
            </span>
          </div>
          <h1 className="font-display text-[clamp(40px,7vw,80px)] font-bold leading-[1] text-white mb-3">{route.name}</h1>
          <p className="text-base md:text-lg text-[rgba(255,255,255,.65)] font-light tracking-wider mb-5">{route.description}</p>
          <div className="flex flex-wrap gap-2">
            <DifficultyMeter level={route.difficulty} compact />
            <CostStars level={route.cost_level} compact />
            <span className="font-mono text-[11px] px-3 py-1 rounded-full bg-[rgba(104,136,204,.12)] text-[#6888cc] border border-[rgba(104,136,204,.2)]">
              {route.region}
            </span>
          </div>
        </div>
      </div>

      <div className="max-w-[1100px] mx-auto px-6 pb-20">
        {/* Overview */}
        <div className="my-8 grid grid-cols-2 sm:grid-cols-3 md:grid-cols-6 gap-3">
          {[
            { label: "天数", value: route.duration_days },
            { label: "距离", value: `${route.distance_km}km` },
            { label: "爬升", value: `${route.cumulative_climb}m` },
            { label: "最高", value: `${route.max_elevation}m` },
            { label: "难度", value: `${route.difficulty}/4` },
            { label: "消费", value: `${route.cost_level}/3` },
          ].map(item => (
            <div key={item.label} className="p-4 text-center rounded-[8px] border border-[#1c2e22] bg-[#121c16] hover:border-[rgba(200,162,78,.3)] hover:translate-y-[-3px] transition-all">
              <div className="font-display text-2xl font-bold text-[#c9a24e] leading-tight">{item.value}</div>
              <div className="font-mono text-[10px] text-text-muted tracking-widest uppercase mt-1">{item.label}</div>
            </div>
          ))}
        </div>

        {/* Season */}
        <div className="mb-8">
          <div className="flex items-center gap-3 pb-3 mb-4 border-b border-[#1c2e22]">
            <span className="text-lg">🌸</span>
            <h2 className="font-display text-2xl font-bold">最佳季节</h2>
          </div>
          <SeasonCalendar data={route.season_calendar} />
        </div>

        {/* Tags */}
        {route.tags.length > 0 && (
          <div className="mb-8">
            <div className="flex items-center gap-3 pb-3 mb-4 border-b border-[#1c2e22]">
              <span className="text-lg">🏷</span>
              <h2 className="font-display text-2xl font-bold">标签</h2>
            </div>
            <div className="flex flex-wrap gap-1.5">
              {route.tags.map(t => (
                <TagBadge key={t.id} name={t.name} category={t.category} colorHex={t.color_hex} bgRgba={t.bg_rgba} />
              ))}
            </div>
          </div>
        )}

        {/* Map */}
        <div className="mb-8">
          <div className="flex items-center gap-3 pb-3 mb-4 border-b border-[#1c2e22]">
            <span className="text-lg">🗺</span>
            <h2 className="font-display text-2xl font-bold">路线地图</h2>
          </div>
          <div className="rounded-[14px] border border-[#1c2e22] overflow-hidden">
            <div className="p-2" style={{ background: "#121c16" }}>
              <MapView coords={coords} height={420} />
            </div>
          </div>
        </div>

        {/* Elevation */}
        {route.elevation_profile.length > 0 && (
          <div className="mb-8">
            <div className="flex items-center gap-3 pb-3 mb-4 border-b border-[#1c2e22]">
              <span className="text-lg">📊</span>
              <h2 className="font-display text-2xl font-bold">海拔剖面</h2>
            </div>
            <div className="p-5 rounded-[8px] border border-[#1c2e22]" style={{ background: "#121c16" }}>
              <div className="flex gap-1 h-28 items-end" style={{ minHeight: 112 }}>
                {route.elevation_profile.map((ep: any, i: number) => {
                  const max = Math.max(...route.elevation_profile.map((e: any) => e.elev || 0));
                  const h = max > 0 ? ((ep.elev || 0) / max) * 100 : 0;
                  return (
                    <div key={i} className="flex-1 flex flex-col items-center">
                      <div className="text-[9px] text-text-muted font-mono mb-1">{ep.elev || 0}m</div>
                      <div style={{ height: `${h}%`, width: "100%", minHeight: 4, borderRadius: "4px 4px 0 0", background: i === 0 || i === route.elevation_profile.length - 1 ? "rgba(90,158,122,.5)" : "rgba(200,162,78,.45)" }} />
                      <div className="text-[9px] text-text-dim mt-1 font-mono">{ep.name || ""}</div>
                    </div>
                  );
                })}
              </div>
            </div>
          </div>
        )}

        {/* Itinerary */}
        {route.days && route.days.length > 0 && (
          <div className="mb-8">
            <div className="flex items-center gap-3 pb-3 mb-4 border-b border-[#1c2e22]">
              <span className="text-lg">📅</span>
              <h2 className="font-display text-2xl font-bold">行程详情</h2>
            </div>
            <div className="space-y-4">
              {route.days.map((day: any, i: number) => (
                <div key={i} className="rounded-[14px] border border-[#1c2e22] overflow-hidden hover:border-[rgba(200,162,78,.25)] hover:translate-y-[-4px] transition-all" style={{ background: "#121c16" }}>
                  <div className="h-48 relative overflow-hidden">
                    {day.image ? (
                      <img src={day.image} alt={day.title} className="w-full h-full object-cover transition-transform duration-700 hover:scale-105" />
                    ) : (
                      <div className="w-full h-full bg-gradient-to-br from-[#1a0a08] to-[#3a2a18]" />
                    )}
                    <div className="absolute inset-0 bg-gradient-to-b from-transparent via-transparent to-[#121c16]" />
                    <div className="absolute bottom-3 right-5 font-display text-5xl font-bold text-[rgba(255,255,255,.1)] leading-none">
                      {String(i + 1).padStart(2, "0")}
                    </div>
                  </div>
                  <div className="p-5">
                    <h3 className="text-lg font-bold mb-1">{day.title}</h3>
                    {day.duration && <p className="font-mono text-[11px] text-text-muted mb-3">{day.duration}</p>}
                    <div className="text-sm text-text-dim leading-relaxed whitespace-pre-line">{day.description}</div>
                    {day.tip && (
                      <div className="mt-3 p-2.5 text-xs text-[#5a9e7a] rounded-[8px] border border-[rgba(90,158,122,.12)]" style={{ background: "rgba(90,158,122,.05)" }}>
                        💡 {day.tip}
                      </div>
                    )}
                  </div>
                </div>
              ))}
            </div>
          </div>
        )}

        {/* Gallery */}
        {route.gallery && route.gallery.length > 0 && (
          <div className="mb-8">
            <div className="flex items-center gap-3 pb-3 mb-4 border-b border-[#1c2e22]">
              <span className="text-lg">🖼</span>
              <h2 className="font-display text-2xl font-bold">影像画廊</h2>
            </div>
            <div className="grid grid-cols-2 md:grid-cols-3 gap-1.5 rounded-[14px] overflow-hidden">
              {route.gallery.map((url, i) => (
                <div key={i} className="relative overflow-hidden cursor-pointer aspect-[4/3] group">
                  <img src={url} alt="" className="w-full h-full object-cover transition-transform duration-600 group-hover:scale-105" />
                  <div className="absolute inset-x-0 bottom-0 pt-8 pb-2 px-3 text-xs text-white bg-gradient-to-b from-transparent to-[rgba(0,0,0,.55)] opacity-0 group-hover:opacity-100 transition-opacity" />
                </div>
              ))}
            </div>
          </div>
        )}

        {/* Author & Meta */}
        <div className="text-center py-8 font-mono text-[11px] text-text-muted tracking-wider border-t border-[#1c2e22] leading-loose">
          {route.author && <p>创建者: {route.author.name}</p>}
          <p>路线 ID: {route.id}</p>
        </div>
      </div>
    </main>
  );
}
