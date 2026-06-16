import { AlertTriangle, Cpu, Database, HardDrive, Network, Server } from "lucide-react";
import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import { ApiUnavailable } from "../components/ApiUnavailable";
import { MetricLineChart } from "../components/MetricLineChart";
import { MetricCard } from "../components/MetricCard";
import { PageHeader } from "../components/PageHeader";
import { RefreshButton } from "../components/RefreshButton";
import { StateBlock } from "../components/StateBlock";
import { StatusBadge } from "../components/StatusBadge";
import { getDevices, getRecentMetrics, getSummary } from "../services/api";
import type { DashboardSummary, DeviceWithLatestMetric, Metric } from "../types";
import { bytes, percent, shortDate } from "../utils/format";

export function Overview() {
  const [summary, setSummary] = useState<DashboardSummary | null>(null);
  const [devices, setDevices] = useState<DeviceWithLatestMetric[]>([]);
  const [metrics, setMetrics] = useState<Metric[]>([]);
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(true);

  async function load() {
    setError("");
    try {
      const [summaryData, deviceData, metricData] = await Promise.all([getSummary(), getDevices(), getRecentMetrics()]);
      setSummary(summaryData);
      setDevices(deviceData);
      setMetrics(metricData);
    } catch {
      setError("Backend API is not reachable yet.");
    } finally {
      setLoading(false);
    }
  }

  useEffect(() => {
    load();
    const timer = window.setInterval(load, 5000);
    return () => window.clearInterval(timer);
  }, []);

  if (loading) return <StateBlock title="Loading dashboard" message="Waiting for InfraPulse API data." />;
  if (error) return <ApiUnavailable onRetry={load} />;

  return (
    <div className="space-y-6">
      <PageHeader
        title="Infrastructure Overview"
        description="Live telemetry from simulated network devices, services, and Linux hosts."
        actions={<RefreshButton onClick={load} loading={loading} />}
      />

      <div className="grid gap-4 sm:grid-cols-2 xl:grid-cols-4">
        <MetricCard label="Devices" value={summary?.total_devices ?? 0} detail={`${summary?.healthy_devices ?? 0} healthy`} icon={Server} />
        <MetricCard label="Active Alerts" value={summary?.active_alerts ?? 0} detail="warning and critical" icon={AlertTriangle} />
        <MetricCard label="Average CPU" value={percent(summary?.average_cpu_usage)} detail="latest aggregate" icon={Cpu} />
        <MetricCard label="Average Memory" value={percent(summary?.average_memory_usage)} detail="latest aggregate" icon={HardDrive} />
      </div>

      <div className="grid gap-4 sm:grid-cols-2 xl:grid-cols-4">
        <MetricCard label="Warning Devices" value={summary?.warning_devices ?? 0} icon={AlertTriangle} />
        <MetricCard label="Critical Devices" value={summary?.critical_devices ?? 0} icon={AlertTriangle} />
        <MetricCard label="Traffic In" value={bytes(summary?.bytes_in_total ?? 0)} icon={Network} />
        <MetricCard label="Last Event" value={shortDate(summary?.last_event_received)} icon={Database} />
      </div>

      {metrics.length ? (
        <div className="grid gap-4 xl:grid-cols-2">
          <MetricLineChart metrics={metrics} dataKey="cpu_usage" color="#2563eb" label="Recent CPU Usage" />
          <MetricLineChart metrics={metrics} dataKey="latency_ms" color="#0f766e" label="Recent Latency" />
        </div>
      ) : (
        <StateBlock title="No metrics yet" message="Telemetry is starting. Refresh in a few seconds or run the demo reset script." />
      )}

      <section className="rounded border border-line bg-white">
        <div className="border-b border-line px-4 py-3">
          <h2 className="font-semibold text-ink">Device Snapshot</h2>
        </div>
        <div className="overflow-x-auto">
          <table className="min-w-full divide-y divide-line text-sm">
            <thead className="bg-slate-50 text-left text-xs uppercase tracking-wide text-slate-500">
              <tr>
                <th className="px-4 py-3">Hostname</th>
                <th className="px-4 py-3">Type</th>
                <th className="px-4 py-3">Status</th>
                <th className="px-4 py-3">CPU</th>
                <th className="px-4 py-3">Memory</th>
                <th className="px-4 py-3">Last Seen</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-line">
              {devices.map((device) => (
                <tr key={device.id}>
                  <td className="px-4 py-3 font-medium">
                    <Link className="text-blue-700 hover:underline" to={`/devices/${device.hostname}`}>
                      {device.hostname}
                    </Link>
                  </td>
                  <td className="px-4 py-3 text-slate-600">{device.device_type}</td>
                  <td className="px-4 py-3">
                    <StatusBadge value={device.status} />
                  </td>
                  <td className="px-4 py-3">{percent(device.latest_metric?.cpu_usage)}</td>
                  <td className="px-4 py-3">{percent(device.latest_metric?.memory_usage)}</td>
                  <td className="px-4 py-3 text-slate-600">{shortDate(device.last_seen)}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
        {!devices.length ? <p className="px-4 py-5 text-sm text-slate-500">No devices are available yet.</p> : null}
      </section>
    </div>
  );
}
