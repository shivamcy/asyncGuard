"use client";

import { useState } from "react";
import Link from "next/link";

export default function SignupPage() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [confirmPassword, setConfirmPassword] = useState("");
  const [error, setError] = useState("");
  const [success, setSuccess] = useState("");
  const [loading, setLoading] = useState(false);

  const handleSignup = async () => {
    setError("");
    setSuccess("");
    setLoading(true);

    try {
      const res = await fetch("http://localhost:8000/auth/signup", {
        method: "POST",
        credentials: "include", // cookie-based auth
        headers: {
          "Content-Type": "application/json",
        },
        // IMPORTANT: backend expects ONLY { email, password }
        body: JSON.stringify({ email, password }),
      });

      if (!res.ok) {
        const data = await res.json();
        throw new Error(data.detail || "Signup failed");
      }

      // Success UX (no redirect forced)
      setSuccess("Signup successful. You can now log in.");
      setEmail("");
      setPassword("");
      setConfirmPassword("");
    } catch (err: any) {
      setError(err.message || "Something went wrong");
    } finally {
      setLoading(false);
    }
  };

  return (
    <>
      <div className="scanline-bg" />
      <div className="vignette" />

      <main className="container">
        {/* HUD */}
        <div className="hud-bar">
          <Link href="/">Home</Link>
          <div className="icons auth-links">
            <Link href="/login">[Login]</Link>
          </div>
        </div>

        {/* Title */}
        <h1>asyncGuard</h1>

        {/* Signup Inputs */}
        <div className="stats">
          <div className="stat-box">
            <span className="stat-label">Email</span>
            <input
              type="email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              placeholder="user@example.com"
              disabled={loading}
            />
          </div>

          <div className="stat-box">
            <span className="stat-label">Password</span>
            <input
              type="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              placeholder="••••••••"
              disabled={loading}
            />
          </div>

          <div className="stat-box">
            <span className="stat-label">Confirm Password</span>
            <input
              type="password"
              value={confirmPassword}
              onChange={(e) => setConfirmPassword(e.target.value)}
              placeholder="••••••••"
              disabled={loading}
            />
          </div>
        </div>

        {/* Button */}
        <div className="start-wrapper">
          <button onClick={handleSignup} disabled={loading}>
            {loading ? "CREATING ACCOUNT" : "SIGNUP"}
          </button>

          {error && <div className="error-text">{error}</div>}
          {success && <div className="success-text">{success}</div>}
        </div>
      </main>
    </>
  );
}
