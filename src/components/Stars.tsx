// 星星展示：完成即奖励，不惩罚
export function Stars({ count }: { count: number }) {
  return (
    <span className="inline-flex items-center gap-1 font-semibold text-amber-500">
      ⭐ {count}
    </span>
  );
}
