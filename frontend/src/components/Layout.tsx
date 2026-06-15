import { Activity, Bell, FileText, Gauge, Network } from "lucide-react";
import { NavLink, Outlet } from "react-router-dom";

const navItems = [
  { to: "/", label: "Overview", icon: Gauge },
  { to: "/devices", label: "Devices", icon: Network },
  { to: "/alerts", label: "Alerts", icon: Bell },
  { to: "/logs", label: "Logs", icon: FileText },
];

export function Layout() {
  return (
    <div className="min-h-screen bg-panel text-ink">
      <aside className="fixed inset-y-0 left-0 hidden w-64 border-r border-line bg-white p-5 md:block">
        <div className="flex items-center gap-3">
          <div className="rounded bg-ink p-2 text-white">
            <Activity size={22} aria-hidden />
          </div>
          <div>
            <h1 className="text-lg font-semibold">InfraPulse</h1>
            <p className="text-xs text-slate-500">Observability Console</p>
          </div>
        </div>
        <nav className="mt-8 space-y-1">
          {navItems.map(({ to, label, icon: Icon }) => (
            <NavLink
              key={to}
              to={to}
              className={({ isActive }) =>
                `flex items-center gap-3 rounded px-3 py-2 text-sm font-medium ${
                  isActive ? "bg-ink text-white" : "text-slate-600 hover:bg-slate-100 hover:text-ink"
                }`
              }
            >
              <Icon size={18} aria-hidden />
              {label}
            </NavLink>
          ))}
        </nav>
      </aside>
      <div className="md:pl-64">
        <header className="sticky top-0 z-10 border-b border-line bg-white/95 px-4 py-3 backdrop-blur md:hidden">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-2 font-semibold">
              <Activity size={20} aria-hidden />
              InfraPulse
            </div>
          </div>
          <nav className="mt-3 flex gap-2 overflow-x-auto">
            {navItems.map(({ to, label }) => (
              <NavLink key={to} to={to} className={({ isActive }) => `rounded px-3 py-2 text-sm ${isActive ? "bg-ink text-white" : "bg-slate-100"}`}>
                {label}
              </NavLink>
            ))}
          </nav>
        </header>
        <main className="mx-auto max-w-7xl px-4 py-6 md:px-8">
          <Outlet />
        </main>
      </div>
    </div>
  );
}
