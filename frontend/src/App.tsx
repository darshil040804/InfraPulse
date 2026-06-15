import { Route, Routes } from "react-router-dom";
import { Layout } from "./components/Layout";
import { Alerts } from "./pages/Alerts";
import { DeviceDetail } from "./pages/DeviceDetail";
import { Devices } from "./pages/Devices";
import { Logs } from "./pages/Logs";
import { Overview } from "./pages/Overview";

export default function App() {
  return (
    <Routes>
      <Route element={<Layout />}>
        <Route path="/" element={<Overview />} />
        <Route path="/devices" element={<Devices />} />
        <Route path="/devices/:hostname" element={<DeviceDetail />} />
        <Route path="/alerts" element={<Alerts />} />
        <Route path="/logs" element={<Logs />} />
      </Route>
    </Routes>
  );
}
