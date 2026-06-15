import type { Status } from "../types";

const classes: Record<string, string> = {
  healthy: "bg-emerald-100 text-emerald-800 ring-emerald-200",
  warning: "bg-amber-100 text-amber-800 ring-amber-200",
  critical: "bg-rose-100 text-rose-800 ring-rose-200",
  down: "bg-zinc-200 text-zinc-800 ring-zinc-300",
  active: "bg-rose-100 text-rose-800 ring-rose-200",
  resolved: "bg-slate-100 text-slate-700 ring-slate-200",
  info: "bg-sky-100 text-sky-800 ring-sky-200",
};

export function StatusBadge({ value }: { value: Status | string }) {
  return <span className={`rounded px-2 py-1 text-xs font-semibold ring-1 ${classes[value] ?? classes.info}`}>{value}</span>;
}
