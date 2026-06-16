import { useEffect, useState } from "react";
import { useParams } from "react-router-dom";
import { Activity, Cpu, HardDrive, RadioTower } from "lucide-react";
import { ApiUnavailable } from "../components/ApiUnavailable";
import { MetricCard } from "../components/MetricCard";
import { MetricLineChart } from "../components/MetricLineChart";
import { StateBlock } from "../components/StateBlock";
import { StatusBadge } from "../components/StatusBadge";
import { getDevice } from "../services/api";
import type { DeviceDetail as Detail } from "../types";
import { percent, shortDate } from "../utils/format";

export function DeviceDetail() {
  const { hostname = "" } = useParams();
  const [detail, setDetail] = useState<Detail | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const load = () => {
    setLoading(true);
    setError(null);

    getDevice(hostname)
      .then(setDetail)
      .catch((err) => setError(err instanceof Error ? err.message : "Unable to load device detail."))
      .finally(() => setLoading(false));
  };

  useEffect(() => {
    load();
  }, [hostname]);

  if (loading) return <StateBlock title="Loading device" message="Fetching device detail and recent telemetry." />;
  if (error) return <ApiUnavailable onRetry={load} />;
  if (!detail) return <StateBlock title="Device not found" message="The API did not return this hostname." />;

  return (
    <div className="space-y-6">
      <div className="flex flex-wrap items-center justify-between gap-3">
        <div>
          <h1 className="text-2xl font-semibold">{detail.device.hostname}</h1>
          <p className="mt-1 text-sm text-slate-500">
            {detail.device.device_type} / {detail.device.ip_address} / {detail.device.location}
          </p>
        </div>
        <StatusBadge value={detail.device.status} />
      </div>

      <div className="grid gap-4 sm:grid-cols-2 xl:grid-cols-4">
        <MetricCard label="CPU" value={percent(detail.latest_metric?.cpu_usage)} icon={Cpu} />
        <MetricCard label="Memory" value={percent(detail.latest_metric?.memory_usage)} icon={HardDrive} />
        <MetricCard label="Latency" value={`${detail.latest_metric?.latency_ms?.toFixed(1) ?? "0.0"} ms`} icon={RadioTower} />
        <MetricCard label="Last Seen" value={shortDate(detail.device.last_seen)} icon={Activity} />
      </div>

      {detail.recent_metrics.length ? (
        <div className="grid gap-4 xl:grid-cols-2">
          <MetricLineChart metrics={detail.recent_metrics} dataKey="cpu_usage" color="#2563eb" label="CPU Usage" />
          <MetricLineChart metrics={detail.recent_metrics} dataKey="memory_usage" color="#7c3aed" label="Memory Usage" />
          <MetricLineChart metrics={detail.recent_metrics} dataKey="latency_ms" color="#0f766e" label="Latency" />
          <MetricLineChart metrics={detail.recent_metrics} dataKey="packet_loss" color="#dc2626" label="Packet Loss" />
        </div>
      ) : (
        <StateBlock title="No recent metrics" message="This device exists, but no recent telemetry has been stored yet." />
      )}

      <section className="rounded border border-line bg-white">
        <div className="border-b border-line px-4 py-3">
          <h2 className="font-semibold">Recent Alerts</h2>
        </div>
        <div className="divide-y divide-line">
          {detail.recent_alerts.length ? (
            detail.recent_alerts.map((alert) => (
              <div key={alert.id} className="flex flex-wrap items-center justify-between gap-3 px-4 py-3 text-sm">
                <div>
                  <p className="font-medium">{alert.message}</p>
                  <p className="text-slate-500">{shortDate(alert.created_at)}</p>
                </div>
                <StatusBadge value={alert.severity} />
              </div>
            ))
          ) : (
            <p className="px-4 py-5 text-sm text-slate-500">No alerts for this device.</p>
          )}
        </div>
      </section>
    </div>
  );
}
