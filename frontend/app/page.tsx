import Link from "next/link";

export default function HomePage() {
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
            <span className="stat-number">128</span>
            <span className="stat-label">APIs Registered</span>
          </div>

          <div className="stat-box">
            <span className="stat-number">2,431</span>
            <span className="stat-label">Audits Performed</span>
          </div>
        </div>
      </main>
    </>
  );
}
