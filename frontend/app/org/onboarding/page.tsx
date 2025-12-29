"use client";

import { useEffect, useState } from "react";
import Link from "next/link";

export default function OrgOnboardingPage() {
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const checkAuth = async () => {
      try {
        const res = await fetch(
          `${process.env.NEXT_PUBLIC_API_BASE_URL}/auth/me`,
          { credentials: "include" }
        );

        if (!res.ok) {
          window.location.href = "/login";
          return;
        }

        const user = await res.json();

        if (user.org_id !== null) {
          window.location.href = "/dashboard";
          return;
        }

        setLoading(false);
      } catch {
        window.location.href = "/login";
      }
    };

    checkAuth();
  }, []);

  if (loading) {
    return (
      <>
        <div className="scanline-bg" />
        <div className="vignette" />
        <main className="container">
          <h1>asyncGuard</h1>
          <div style={{ textAlign: "center", opacity: 0.7 }}>
            Loading…
          </div>
        </main>
      </>
    );
  }

  return (
    <>
      <div className="scanline-bg" />
      <div className="vignette" />

      <main className="container">
        <h1>asyncGuard</h1>

        <div
          style={{
            textAlign: "center",
            marginBottom: "2rem",
            color: "#b6ff00",
            opacity: 0.8,
            fontSize: "1rem",
          }}
        >
          Organization Setup
        </div>

        <div className="stats">
          <div className="stat-box">
            <Link href="/org/create">
              <button className="start-btn">CREATE ORG</button>
            </Link>
          </div>

          <div className="stat-box">
            <Link href="/org/join">
              <button className="start-btn">JOIN ORG</button>
            </Link>
          </div>
        </div>
      </main>
    </>
  );
}
