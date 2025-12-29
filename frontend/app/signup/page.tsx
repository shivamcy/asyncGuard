
"use client";

import { useState } from "react";
import Link from "next/link";

export default function SignupPage() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [confirmPassword, setConfirmPassword] = useState("");
  const [error, setError] = useState("");

  const validateEmail = (email: string) =>
    /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email);

  const validatePassword = (password: string) =>
    password.length >= 8 &&
    /[A-Z]/.test(password) &&
    /[a-z]/.test(password) &&
    /[0-9]/.test(password) &&
    /[^A-Za-z0-9]/.test(password);

  const handleSignup = () => {
    if (!validateEmail(email)) {
      setError("Invalid email address");
      return;
    }

    if (!validatePassword(password)) {
      setError(
        "Password must be at least 8 characters and include uppercase, lowercase, number, and special character"
      );
      return;
    }

    if (password !== confirmPassword) {
      setError("Passwords do not match");
      return;
    }

    setError("");
    console.log("Signup valid");
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

          <div className="stat-box">
            <span className="stat-label">Confirm Password</span>
            <input
              type="password"
              value={confirmPassword}
              onChange={(e) => setConfirmPassword(e.target.value)}
              placeholder="••••••••"
            />
          </div>
        </div>

        {/* START Button */}
        <div className="start-wrapper">
          <button onClick={handleSignup}>Signup</button>
          {error && <div className="error-text">{error}</div>}
        </div>
      </main>
    </>
  );
}
