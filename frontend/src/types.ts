export type Status = "healthy" | "warning" | "critical" | "down";

export interface Metric {
  id: number;
  device_id: number;
  cpu_usage: number;
  memory_usage: number;
  disk_usage: number;
  latency_ms: number;
  packet_loss: number;
  bytes_in: number;
  bytes_out: number;
  status: Status;
  timestamp: string;
}

export interface Device {
  id: number;
  hostname: string;
  device_type: string;
  ip_address: string;
  location: string;
  status: Status;
  last_seen: string | null;
  created_at: string;
}

export interface DeviceWithLatestMetric extends Device {
  latest_metric: Metric | null;
}

export interface Alert {
  id: number;
  device_id: number;
  severity: "info" | "warning" | "critical";
  alert_type: string;
  message: string;
  status: "active" | "resolved";
  created_at: string;
  resolved_at: string | null;
}

export interface LogEvent {
  id: number;
  service: string;
  level: string;
  message: string;
  device_id: number | null;
  timestamp: string;
}

export interface DashboardSummary {
  total_devices: number;
  healthy_devices: number;
  warning_devices: number;
  critical_devices: number;
  down_devices: number;
  active_alerts: number;
  average_cpu_usage: number;
  average_memory_usage: number;
  bytes_in_total: number;
  bytes_out_total: number;
  last_event_received: string | null;
}

export interface DeviceDetail {
  device: Device;
  latest_metric: Metric | null;
  recent_metrics: Metric[];
  recent_alerts: Alert[];
  recent_logs: LogEvent[];
}
