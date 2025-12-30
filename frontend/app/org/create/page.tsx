"use client";

import { useState } from "react";
import Link from "next/link";

export default function CreateOrgPage() {
  const [orgName, setOrgName] = useState("");
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  const handleCreate = async () => {
    setError("");
    setLoading(true);

    try {
      const res = await fetch(`${process.env.NEXT_PUBLIC_API_BASE_URL}/organizations/create`, {
        method: "POST",
        credentials: "include",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ name: orgName }),
      });

      if (!res.ok) {
        const data = await res.json();
        throw new Error(data.detail || "Failed to create organization");
      }

      // re-check auth state
      const meRes = await fetch(`${process.env.NEXT_PUBLIC_API_BASE_URL}/auth/me`, {
        credentials: "include",
      });

      if (!meRes.ok) throw new Error("Auth state invalid");

      window.location.href = "/dashboard";
    } catch (err: any) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <>
      <div className="scanline-bg" />
      <div className="vignette" />

      <main className="container">
        <div className="hud-bar">
          <Link href="/org/onboarding">Back</Link>
        </div>

        <h1>asyncGuard</h1>

        <div className="stats">
          <div className="stat-box">
            <span className="stat-label">Organization Name</span>
            <input
              value={orgName}
              onChange={(e) => setOrgName(e.target.value)}
              placeholder="My Organization"
              disabled={loading}
            />
          </div>
        </div>

        <div className="start-wrapper">
          <button onClick={handleCreate} disabled={loading}>
            {loading ? "CREATING…" : "CREATE"}
          </button>
          {error && <div className="error-text">{error}</div>}
        </div>
      </main>
    </>
  );
}
