import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import { ApiUnavailable } from "../components/ApiUnavailable";
import { PageHeader } from "../components/PageHeader";
import { RefreshButton } from "../components/RefreshButton";
import { StateBlock } from "../components/StateBlock";
import { StatusBadge } from "../components/StatusBadge";
import { getDevices } from "../services/api";
import type { DeviceWithLatestMetric } from "../types";
import { percent, shortDate } from "../utils/format";

export function Devices() {
  const [devices, setDevices] = useState<DeviceWithLatestMetric[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  async function load() {
    setError("");
    try {
      setDevices(await getDevices());
    } catch {
      setError("Backend API is not reachable yet.");
    } finally {
      setLoading(false);
    }
  }

  useEffect(() => {
    load();
  }, []);

  if (loading) return <StateBlock title="Loading devices" message="Reading device inventory from the API." />;
  if (error) return <ApiUnavailable onRetry={load} />;
  if (!devices.length) return <StateBlock title="No devices yet" message="Start Docker Compose and wait for telemetry events." />;

  return (
    <div className="space-y-5">
      <PageHeader
        title="Devices"
        description="Current status and latest metrics for each monitored endpoint."
        actions={<RefreshButton onClick={load} loading={loading} />}
      />
      <section className="rounded border border-line bg-white">
        <div className="overflow-x-auto">
          <table className="min-w-full divide-y divide-line text-sm">
            <thead className="bg-slate-50 text-left text-xs uppercase tracking-wide text-slate-500">
              <tr>
                <th className="px-4 py-3">Hostname</th>
                <th className="px-4 py-3">Type</th>
                <th className="px-4 py-3">IP Address</th>
                <th className="px-4 py-3">Location</th>
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
                    <Link to={`/devices/${device.hostname}`} className="text-blue-700 hover:underline">
                      {device.hostname}
                    </Link>
                  </td>
                  <td className="px-4 py-3">{device.device_type}</td>
                  <td className="px-4 py-3 font-mono text-xs">{device.ip_address}</td>
                  <td className="px-4 py-3">{device.location}</td>
                  <td className="px-4 py-3">
                    <StatusBadge value={device.status} />
                  </td>
                  <td className="px-4 py-3">{percent(device.latest_metric?.cpu_usage)}</td>
                  <td className="px-4 py-3">{percent(device.latest_metric?.memory_usage)}</td>
                  <td className="px-4 py-3">{shortDate(device.last_seen)}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </section>
    </div>
  );
}
