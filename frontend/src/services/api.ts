import axios from "axios";
import type { Alert, DashboardSummary, DeviceDetail, DeviceWithLatestMetric, LogEvent, Metric } from "../types";

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL ?? "http://localhost:8000";

export const api = axios.create({
  baseURL: API_BASE_URL,
  timeout: 10000,
});

export async function getSummary(): Promise<DashboardSummary> {
  const { data } = await api.get<DashboardSummary>("/api/dashboard/summary");
  return data;
}

export async function getDevices(): Promise<DeviceWithLatestMetric[]> {
  const { data } = await api.get<DeviceWithLatestMetric[]>("/api/devices");
  return data;
}

export async function getDevice(hostname: string): Promise<DeviceDetail> {
  const { data } = await api.get<DeviceDetail>(`/api/devices/${hostname}`);
  return data;
}

export async function getRecentMetrics(): Promise<Metric[]> {
  const { data } = await api.get<Metric[]>("/api/metrics/recent");
  return data.reverse();
}

export async function getAlerts(params?: { severity?: string; status?: string }): Promise<Alert[]> {
  const { data } = await api.get<Alert[]>("/api/alerts", { params });
  return data;
}

export async function resolveAlert(alertId: number): Promise<Alert> {
  const { data } = await api.patch<Alert>(`/api/alerts/${alertId}/resolve`);
  return data;
}

export async function getRecentLogs(): Promise<LogEvent[]> {
  const { data } = await api.get<LogEvent[]>("/api/logs/recent");
  return data;
}
