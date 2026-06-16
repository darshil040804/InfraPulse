import { RefreshCw } from "lucide-react";

export function RefreshButton({ onClick, loading = false }: { onClick: () => void; loading?: boolean }) {
  return (
    <button
      className="inline-flex items-center gap-2 rounded border border-line bg-white px-3 py-2 text-sm font-medium text-slate-700 hover:bg-slate-50 disabled:cursor-not-allowed disabled:opacity-50"
      onClick={onClick}
      disabled={loading}
      type="button"
    >
      <RefreshCw size={16} className={loading ? "animate-spin" : ""} aria-hidden />
      Refresh
    </button>
  );
}
