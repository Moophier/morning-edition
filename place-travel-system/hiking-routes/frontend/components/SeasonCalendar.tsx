export default function SeasonCalendar({ data }: { data: number[] }) {
  const months = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12"];
  return (
    <div className="flex gap-1">
      {months.map((m, i) => {
        const v = data[i] || 0;
        let cls = "flex-1 h-8 rounded-[6px] flex items-center justify-center font-mono text-[10px] text-text-muted border border-transparent transition-all";
        if (v === 2) cls += " bg-[rgba(200,162,78,.18)] border-[rgba(200,162,78,.3)] text-[#c9a24e] font-semibold";
        else if (v === 1) cls += " bg-[rgba(90,158,122,.1)] border-[rgba(90,158,122,.2)] text-[#5a9e7a]";
        return <div key={m} className={cls}>{m}</div>;
      })}
    </div>
  );
}
