import Link from "next/link";
import DifficultyMeter from "./DifficultyMeter";
import CostStars from "./CostStars";

interface RouteCardItem {
  id: string;
  name: string;
  slug: string;
  difficulty: number;
  cost_level: number;
  region: string;
  duration_days: string;
  distance_km: number;
  hero_image: string;
  tags: Array<{ id: string; name: string; category: string; color_hex: string; bg_rgba: string }>;
  author_name?: string;
}

export default function RouteCard({ route }: { route: RouteCardItem }) {
  return (
    <Link href={`/routes/${route.id}`} className="block group">
      <div className="rounded-[14px] border border-[#1c2e22] overflow-hidden transition-all duration-350 hover:border-[rgba(200,162,78,.3)] hover:translate-y-[-3px] hover:shadow-[0_12px_40px_rgba(0,0,0,.3)]" style={{ background: "#121c16" }}>
        <div className="h-44 relative overflow-hidden">
          <div className="absolute inset-0 bg-gradient-to-b from-transparent via-transparent to-[#121c16] z-[1]" />
          {route.hero_image ? (
            <img src={route.hero_image} alt={route.name} className="w-full h-full object-cover transition-transform duration-700 group-hover:scale-105" />
          ) : (
            <div className="w-full h-full bg-gradient-to-br from-[#2a1008] via-[#5a2a18] to-[#a05030]" />
          )}
          <div className="absolute top-3 right-3 flex gap-1.5 z-[2]">
            <DifficultyMeter level={route.difficulty} compact />
            <CostStars level={route.cost_level} compact />
          </div>
        </div>
        <div className="p-4">
          <h3 className="font-display text-xl font-bold leading-tight mb-1">{route.name}</h3>
          <p className="font-mono text-[11px] text-text-muted mb-3">
            {route.region} · {route.duration_days} · {route.distance_km}km
          </p>
          {route.tags.length > 0 && (
            <div className="flex flex-wrap gap-1">
              {route.tags.slice(0, 5).map(t => (
                <span key={t.id} className="text-[10px] px-2 py-0.5 rounded-[8px]" style={{ background: t.bg_rgba, color: t.color_hex }}>
                  {t.name}
                </span>
              ))}
              {route.tags.length > 5 && (
                <span className="text-[10px] px-2 py-0.5 rounded-[8px] text-text-muted" style={{ background: "rgba(255,255,255,.04)" }}>
                  +{route.tags.length - 5}
                </span>
              )}
            </div>
          )}
        </div>
      </div>
    </Link>
  );
}
