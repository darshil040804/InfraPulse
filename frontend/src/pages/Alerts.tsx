import { CheckCircle2 } from "lucide-react";
import { useEffect, useMemo, useState } from "react";
import { ApiUnavailable } from "../components/ApiUnavailable";
import { RefreshButton } from "../components/RefreshButton";
import { StateBlock } from "../components/StateBlock";
import { StatusBadge } from "../components/StatusBadge";
import { getAlerts, resolveAlert } from "../services/api";
import type { Alert } from "../types";
import { shortDate } from "../utils/format";

export function Alerts() {
  const [alerts, setAlerts] = useState<Alert[]>([]);
  const [severity, setSeverity] = useState("");
  const [status, setStatus] = useState("active");
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  async function load() {
    setError("");
    try {
      setAlerts(await getAlerts({ severity: severity || undefined, status: status || undefined }));
    } catch {
      setError("Backend API is not reachable yet.");
    } finally {
      setLoading(false);
    }
  }

  useEffect(() => {
    load();
  }, [severity, status]);

  const activeCount = useMemo(() => alerts.filter((alert) => alert.status === "active").length, [alerts]);

  if (loading) return <StateBlock title="Loading alerts" message="Reading alert state from the backend." />;
  if (error) return <ApiUnavailable onRetry={load} />;

  return (
    <div className="space-y-5">
      <div className="flex flex-wrap items-end justify-between gap-3">
        <div>
          <h1 className="text-2xl font-semibold">Alerts</h1>
          <p className="mt-1 text-sm text-slate-500">{activeCount} active alerts in the current filter.</p>
        </div>
        <div className="flex gap-2">
          <RefreshButton onClick={load} loading={loading} />
          <select className="rounded border border-line bg-white px-3 py-2 text-sm" value={severity} onChange={(event) => setSeverity(event.target.value)}>
            <option value="">All severity</option>
            <option value="warning">Warning</option>
            <option value="critical">Critical</option>
          </select>
          <select className="rounded border border-line bg-white px-3 py-2 text-sm" value={status} onChange={(event) => setStatus(event.target.value)}>
            <option value="">All status</option>
            <option value="active">Active</option>
            <option value="resolved">Resolved</option>
          </select>
        </div>
      </div>

      <section className="rounded border border-line bg-white">
        <div className="overflow-x-auto">
          <table className="min-w-full divide-y divide-line text-sm">
            <thead className="bg-slate-50 text-left text-xs uppercase tracking-wide text-slate-500">
              <tr>
                <th className="px-4 py-3">Severity</th>
                <th className="px-4 py-3">Type</th>
                <th className="px-4 py-3">Message</th>
                <th className="px-4 py-3">Status</th>
                <th className="px-4 py-3">Created</th>
                <th className="px-4 py-3">Action</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-line">
              {alerts.map((alert) => (
                <tr key={alert.id}>
                  <td className="px-4 py-3">
                    <StatusBadge value={alert.severity} />
                  </td>
                  <td className="px-4 py-3">{alert.alert_type}</td>
                  <td className="px-4 py-3">{alert.message}</td>
                  <td className="px-4 py-3">
                    <StatusBadge value={alert.status} />
                  </td>
                  <td className="px-4 py-3">{shortDate(alert.created_at)}</td>
                  <td className="px-4 py-3">
                    <button
                      className="inline-flex items-center gap-2 rounded border border-line px-3 py-2 text-sm font-medium disabled:cursor-not-allowed disabled:opacity-40"
                      disabled={alert.status === "resolved"}
                      onClick={async () => {
                        try {
                          await resolveAlert(alert.id);
                          await load();
                        } catch {
                          setError("Backend API is not reachable yet.");
                        }
                      }}
                    >
                      <CheckCircle2 size={16} aria-hidden />
                      Resolve
                    </button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
        {!alerts.length ? <p className="px-4 py-5 text-sm text-slate-500">No alerts match this filter.</p> : null}
      </section>
    </div>
  );
}
