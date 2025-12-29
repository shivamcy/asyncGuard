"use client";

import { useState } from "react";
import Link from "next/link";

export default function LoginPage() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");

  const validateEmail = (email: string) =>
    /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email);

  const validatePassword = (password: string) =>
    password.length >= 8 &&
    /[A-Z]/.test(password) &&
    /[a-z]/.test(password) &&
    /[0-9]/.test(password) &&
    /[^A-Za-z0-9]/.test(password);

  const handleLogin = async () => {
  setError("");

  if (!validateEmail(email)) {
    setError("Invalid email address");
    return;
  }

  // if (!validatePassword(password)) {
  //   setError("Weak password");
  //   return;
  // }

  try {
    const res = await fetch(`${process.env.NEXT_PUBLIC_API_BASE_URL}/auth/login`, {
      method: "POST",
      credentials: "include", // 🔥 critical (cookie auth)
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ email, password }),
    });

    if (!res.ok) {
      const data = await res.json();
      throw new Error(data.detail || "Login failed");
    }

    // Login success → go to dashboard later
    window.location.href = "/";
  } catch (err: any) {
    setError(err.message);
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
          <Link href="/signup">[Signup]</Link>
          </div>
        </div>

        {/* Title */}
        <h1>asyncGuard</h1>

        {/* Login Inputs */}
        <div className="stats">
          <div className="stat-box">
            <span className="stat-label">Email</span>
            <input
              type="email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              placeholder="user@example.com"
            />
          </div>

          <div className="stat-box">
            <span className="stat-label">Password</span>
            <input
              type="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              placeholder="••••••••"
            />
          </div>
        </div>

        {/* START Button */}
        <div className="start-wrapper">
          <button onClick={handleLogin}>Login</button>
          {error && <div className="error-text">{error}</div>}
        </div>
      </main>
    </>
  );
}
