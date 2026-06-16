import { useEffect, useState } from "react";
import { ApiUnavailable } from "../components/ApiUnavailable";
import { PageHeader } from "../components/PageHeader";
import { RefreshButton } from "../components/RefreshButton";
import { StateBlock } from "../components/StateBlock";
import { getRecentLogs } from "../services/api";
import type { LogEvent } from "../types";
import { shortDate } from "../utils/format";

export function Logs() {
  const [logs, setLogs] = useState<LogEvent[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  async function load() {
    setError("");
    try {
      setLogs(await getRecentLogs());
    } catch {
      setError("Backend API is not reachable yet.");
    } finally {
      setLoading(false);
    }
  }

  useEffect(() => {
    load();
  }, []);

  if (loading) return <StateBlock title="Loading logs" message="Reading recent structured application events." />;
  if (error) return <ApiUnavailable onRetry={load} />;
  if (!logs.length) return <StateBlock title="No logs yet" message="Logs will appear after telemetry events are processed." />;

  return (
    <div className="space-y-5">
      <PageHeader
        title="Logs"
        description="Recent structured events from backend and telemetry services."
        actions={<RefreshButton onClick={load} loading={loading} />}
      />
      <section className="rounded border border-line bg-white">
        <div className="divide-y divide-line">
          {logs.map((log) => (
            <div key={log.id} className="grid gap-2 px-4 py-3 text-sm md:grid-cols-[160px_100px_1fr_120px]">
              <span className="text-slate-500">{shortDate(log.timestamp)}</span>
              <span className={log.level === "WARNING" || log.level === "ERROR" ? "font-semibold text-rose-700" : "font-semibold text-slate-700"}>{log.level}</span>
              <span>{log.message}</span>
              <span className="text-slate-500">{log.service}</span>
            </div>
          ))}
        </div>
      </section>
    </div>
  );
}
