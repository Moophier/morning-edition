export default function DifficultyMeter({ level, compact }: { level: number; compact?: boolean }) {
  if (compact) {
    return (
      <span className="text-[10px] px-2 py-0.5 rounded-full font-mono tracking-wider"
        style={{ background: level <= 2 ? "rgba(90,158,122,.85)" : "rgba(200,162,78,.85)", color: "#0a1a10" }}>
        {["简单", "中等", "困难", "专业"][level - 1] || "未知"}
      </span>
    );
  }
  return (
    <div className="flex gap-[3px]">
      {[1, 2, 3, 4].map(i => (
        <div key={i} className={`flex-1 h-2 rounded-[4px] transition-all ${i <= level ? "bg-[#c9a24e]" : "bg-[rgba(255,255,255,.05)]"} ${i > 2 && i <= level ? "bg-[#b86b4a]" : ""}`} />
      ))}
    </div>
  );
}
