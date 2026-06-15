import { CartesianGrid, Line, LineChart, ResponsiveContainer, Tooltip, XAxis, YAxis } from "recharts";
import type { Metric } from "../types";
import { shortDate } from "../utils/format";

export function MetricLineChart({ metrics, dataKey, color, label }: { metrics: Metric[]; dataKey: keyof Metric; color: string; label: string }) {
  return (
    <div className="h-72 rounded border border-line bg-white p-4">
      <div className="mb-3 flex items-center justify-between">
        <h2 className="text-sm font-semibold text-ink">{label}</h2>
      </div>
      <ResponsiveContainer width="100%" height="88%">
        <LineChart data={metrics}>
          <CartesianGrid strokeDasharray="3 3" stroke="#e5e7eb" />
          <XAxis dataKey="timestamp" tickFormatter={shortDate} minTickGap={28} tick={{ fontSize: 12 }} />
          <YAxis tick={{ fontSize: 12 }} />
          <Tooltip labelFormatter={(value) => shortDate(String(value))} />
          <Line type="monotone" dataKey={dataKey as string} stroke={color} strokeWidth={2} dot={false} />
        </LineChart>
      </ResponsiveContainer>
    </div>
  );
}
