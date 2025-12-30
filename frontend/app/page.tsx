import Link from "next/link";
import { fetchOverviewStats } from "../features/stats/stats.api";

export default async function HomePage() {
  const stats = await fetchOverviewStats();
  
  // If stats is null, the backend is down
  const isBackendDown = !stats;

  // Default values to render if down
  const safeStats = stats || { apis_registered: 0, audits_performed: 0 };

  return (
    <>
      <div className="scanline-bg" />
      <div className="vignette" />

      <main className="container">
        {/* Top HUD */}
        <div className="hud-bar">
          <span>Home</span>
          <div className="icons auth-links">
            <Link href="/login">[Login]</Link>
            <Link href="/signup">[Signup]</Link>
          </div>
        </div>

        {/* Title */}
        <h1>asyncGuard</h1>

        {/* Stats Section */}
        <div className="stats">
          <div className="stat-box">
            <span className="stat-number" style={{ color: isBackendDown ? '#ff4d4d' : undefined }}>
              {isBackendDown ? "SERVER UNREACHABLE" : safeStats.apis_registered}
            </span>
            <span className="stat-label">APIs Registered</span>
          </div>

          <div className="stat-box">
            <span className="stat-number" style={{ color: isBackendDown ? '#ff4d4d' : undefined }}>
              {isBackendDown ? "SERVER UNREACHABLE" : safeStats.audits_performed}
            </span>
            <span className="stat-label">Audits Performed</span>
          </div>
        </div>
      </main>
    </>
  );
}