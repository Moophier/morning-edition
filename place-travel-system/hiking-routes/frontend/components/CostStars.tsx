export default function CostStars({ level, compact }: { level: number; compact?: boolean }) {
  if (compact) {
    return (
      <span className="text-[10px] px-2 py-0.5 rounded-full font-mono tracking-wider"
        style={{ background: level === 1 ? "rgba(90,158,122,.85)" : level === 2 ? "rgba(200,162,78,.75)" : "rgba(184,107,74,.8)", color: "#0a1a10" }}>
        {["低", "中", "高"][level - 1] || "未知"}
      </span>
    );
  }
  return (
    <div className="flex gap-1">
      {[1, 2, 3].map(i => (
        <span key={i} className={`text-base transition-all ${i <= level ? "text-[#c9a24e]" : "text-[rgba(255,255,255,.08)]"}`}>★</span>
      ))}
    </div>
  );
}
