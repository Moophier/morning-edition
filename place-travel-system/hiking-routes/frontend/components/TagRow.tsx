import TagBadge from "./TagBadge";

interface TagRowProps {
  tags: Array<{ id: string; name: string; category: string; color_hex: string; bg_rgba: string }>;
  selectedIds?: string[];
  onToggle?: (id: string) => void;
}

export default function TagRow({ tags, selectedIds = [], onToggle }: TagRowProps) {
  return (
    <div className="flex flex-wrap gap-1.5">
      {tags.map(t => (
        <TagBadge
          key={t.id}
          name={t.name}
          category={t.category}
          colorHex={t.color_hex}
          bgRgba={t.bg_rgba}
          onClick={onToggle ? () => onToggle(t.id) : undefined}
          selected={selectedIds.includes(t.id)}
        />
      ))}
    </div>
  );
}
