interface TagBadgeProps {
  name: string;
  category: string;
  colorHex: string;
  bgRgba: string;
  size?: "sm" | "default" | "lg";
  onClick?: () => void;
  selected?: boolean;
}

const sizeClasses = {
  sm: "text-[10px] px-2 py-0.5 rounded-[8px]",
  default: "text-[11px] px-2.5 py-1 rounded-[10px]",
  lg: "text-[13px] px-3.5 py-1.5 rounded-[14px]",
};

export default function TagBadge({ name, category, colorHex, bgRgba, size = "default", onClick, selected }: TagBadgeProps) {
  return (
    <span
      className={`inline-flex items-center gap-1 font-normal whitespace-nowrap transition-all duration-200 ${sizeClasses[size]} ${onClick ? "cursor-pointer hover:scale-105" : ""} ${selected ? "ring-2 ring-[#c9a24e]" : ""}`}
      style={{ background: bgRgba, color: colorHex }}
      onClick={onClick}
    >
      {name}
    </span>
  );
}
