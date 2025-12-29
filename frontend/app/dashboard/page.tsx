"use client";

import { useEffect, useState } from "react";

type User = {
  id: number;
  email: string;
  role: "admin" | "viewer" | "auditor";
  org_id: number | null;
};

type Api = {
  id: number;
  name: string;
  url: string;
  is_active: boolean;
  created_at: string;
  audit_score?: number | null;
};

export default function DashboardPage() {
  const [user, setUser] = useState<User | null>(null);
  const [apis, setApis] = useState<Api[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  /* -------- Create API Modal -------- */
  const [showModal, setShowModal] = useState(false);
  const [apiName, setApiName] = useState("");
  const [apiUrl, setApiUrl] = useState("");

  /* -------- INIT -------- */
  useEffect(() => {
    const init = async () => {
      try {
        const meRes = await fetch(
          `${process.env.NEXT_PUBLIC_API_BASE_URL}/auth/me`,
          { credentials: "include" }
        );

        if (!meRes.ok) {
          window.location.href = "/login";
          return;
        }

        const me: User = await meRes.json();

        if (me.org_id === null) {
          window.location.href = "/org/onboarding";
          return;
        }

        setUser(me);

        const apiRes = await fetch(
          `${process.env.NEXT_PUBLIC_API_BASE_URL}/apis/list`,
          { credentials: "include" }
        );

        if (!apiRes.ok) throw new Error("Failed to load APIs");

        const apiList = await apiRes.json();
        setApis(apiList);
      } catch (err: any) {
        setError(err.message);
      } finally {
        setLoading(false);
      }
    };

    init();
  }, []);

  /* -------- ACTIONS -------- */

  const handleLogout = async () => {
    try {
      await fetch(
        `${process.env.NEXT_PUBLIC_API_BASE_URL}/auth/logout`,
        { method: "POST", credentials: "include" }
      );
    } finally {
      window.location.href = "/login";
    }
  };

  const handleDeleteOrganisation = async () => {
    if (!confirm("Delete organisation and all APIs?")) return;

    try {
      const res = await fetch(
        `${process.env.NEXT_PUBLIC_API_BASE_URL}/organizations/delete`,
        { method: "DELETE", credentials: "include" }
      );

      if (!res.ok) {
        const data = await res.json();
        throw new Error(data.detail || "Delete failed");
      }

      window.location.href = "/org/onboarding";
    } catch (err: any) {
      alert(err.message);
    }
  };

  const handleCreateApi = async () => {
    if (!apiName || !apiUrl) return;

    try {
      const res = await fetch(
        `${process.env.NEXT_PUBLIC_API_BASE_URL}/apis/create`,
        {
          method: "POST",
          credentials: "include",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ name: apiName, url: apiUrl }),
        }
      );

      if (!res.ok) {
        const data = await res.json();
        throw new Error(data.detail || "Create failed");
      }

      const newApi = await res.json();
      setApis((prev) => [...prev, newApi]);

      setShowModal(false);
      setApiName("");
      setApiUrl("");
    } catch (err: any) {
      alert(err.message);
    }
  };

  const handleDeleteApi = async (apiId: number) => {
    if (!confirm("Delete this API?")) return;

    try {
      const res = await fetch(
        `${process.env.NEXT_PUBLIC_API_BASE_URL}/apis/delete/${apiId}`,
        {
          method: "DELETE",
          credentials: "include",
        }
      );

      if (!res.ok) {
        const data = await res.json();
        throw new Error(data.detail || "Delete failed");
      }

      setApis((prev) => prev.filter((api) => api.id !== apiId));
    } catch (err: any) {
      alert(err.message);
    }
  };

  /* -------- STATES -------- */
  if (loading) return <p style={{ textAlign: "center" }}>Loading…</p>;
  if (error) return <p className="error-text">{error}</p>;

  /* -------- RENDER -------- */
  return (
    <>
      <div className="scanline-bg" />
      <div className="vignette" />

      {/* HEADER */}
      <div
        style={{
          position: "fixed",
          top: 0,
          left: 0,
          right: 0,
          padding: "1.2rem 2rem",
          display: "flex",
          justifyContent: "space-between",
          color: "#b6ff00",
          zIndex: 100,
        }}
      >
        <div style={{ fontWeight: 700, letterSpacing: "0.15em" }}>
          ASYNCGUARD
        </div>

        <div style={{ position: "absolute", left: "50%", transform: "translateX(-50%)" }}>
          <h1 style={{ margin: 0, fontSize: "2.8rem", letterSpacing: "0.3em" }}>
            DASHBOARD
          </h1>
        </div>

        <div style={{ textAlign: "right", fontSize: "0.75rem", letterSpacing: "0.12em" }}>
          <div style={{ display: "flex", gap: "1.2rem" }}>
            <span>[help]</span>

            {user?.role === "admin" ? (
              <>
                <span>[manage users]</span>
                <span onClick={handleDeleteOrganisation} style={{ cursor: "pointer" }}>
                  [delete organisation]
                </span>
              </>
            ) : (
              <span>[leave organisation]</span>
            )}

            <span onClick={handleLogout} style={{ cursor: "pointer" }}>
              [logout]
            </span>
          </div>

          {user?.role === "admin" && (
            <button
              className="start-btn"
              style={{ marginTop: "0.8rem" }}
              onClick={() => setShowModal(true)}
            >
              CREATE NEW API
            </button>
          )}
        </div>
      </div>

      {/* TABLE */}
      <main style={{ paddingTop: "6rem", padding: "0 4rem" }}>
        <table style={{ width: "100%", marginTop: "2rem", borderCollapse: "collapse" }}>
          <thead>
            <tr>
              <th>Name</th>
              <th>URL</th>
              <th>Created</th>
              <th>Status</th>
              <th>Audit Score</th>
              {user?.role === "admin" && <th>Actions</th>}
            </tr>
          </thead>

          <tbody>
            {apis.length === 0 && (
              <tr>
                <td colSpan={user?.role === "admin" ? 6 : 5} style={{ textAlign: "center", opacity: 0.7 }}>
                  No APIs registered yet
                </td>
              </tr>
            )}

            {apis.map((api) => (
              <tr key={api.id}>
                <td>{api.name}</td>
                <td>{api.url}</td>
                <td>{new Date(api.created_at).toLocaleDateString()}</td>
                <td>{api.is_active ? "Active" : "Inactive"}</td>
                <td>{api.audit_score ?? "—"}</td>

                {user?.role === "admin" && (
                  <td>
                    <span
                      style={{ color: "#ff4d4d", cursor: "pointer" }}
                      onClick={() => handleDeleteApi(api.id)}
                    >
                      Delete
                    </span>
                  </td>
                )}
              </tr>
            ))}
          </tbody>
        </table>
      </main>

      {/* CREATE API MODAL */}
      {showModal && (
        <div className="modal-overlay">
          <div className="modal">
            <h3>Create API</h3>

            <input
              placeholder="API Name"
              value={apiName}
              onChange={(e) => setApiName(e.target.value)}
            />
            <input
              placeholder="API URL"
              value={apiUrl}
              onChange={(e) => setApiUrl(e.target.value)}
            />

            <div style={{ marginTop: "1rem" }}>
              <button onClick={handleCreateApi}>Create</button>
              <button onClick={() => setShowModal(false)}>Cancel</button>
            </div>
          </div>
        </div>
      )}
    </>
  );
}
