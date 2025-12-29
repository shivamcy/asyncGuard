"use client";

import { useEffect, useState } from "react";

type User = {
  id: number;
  email: string;
  role: "admin" | "viewer" | "auditor";
  org_id: number | null;
};

type OrgUser = {
  id: number;
  email: string;
  role: string;
};

// Response from /reports/results
type BackendResponseItem = {
  api: { id: number; name: string; url: string };
  latest_audit: { id: number; score: number; time_window: string } | null;
};

// Response from /apis/error/{id}
type ApiErrorResponse = {
    api_id: number;
    results: { details: any }[]; 
  };

type DashboardApi = {
  id: number;
  name: string;
  url: string;
  is_active: boolean;
  created_at: string;
  audit_score: number | null;
};

// Added "VIEW_ERRORS" to modal types
type ModalType = "CREATE_API" | "DELETE_ORG" | "LEAVE_ORG" | "DELETE_API" | "HELP" | "MANAGE_USERS" | "REMOVE_USER_CONFIRM" | "VIEW_ERRORS" | null;

export default function DashboardPage() {
  const [user, setUser] = useState<User | null>(null);
  const [apis, setApis] = useState<DashboardApi[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  /* -------- Modal States -------- */
  const [activeModal, setActiveModal] = useState<ModalType>(null);
  const [targetApiId, setTargetApiId] = useState<number | null>(null);
  
  // Create API form states
  const [apiName, setApiName] = useState("");
  const [apiUrl, setApiUrl] = useState("");
  
  // User Management states
  const [orgUsers, setOrgUsers] = useState<OrgUser[]>([]);
  const [userToRemove, setUserToRemove] = useState<OrgUser | null>(null);
  
  // Error Viewing State
  const [selectedApiErrors, setSelectedApiErrors] = useState<string[]>([]);
  const [selectedApiName, setSelectedApiName] = useState(""); // Just for display in modal
  
  const [actionLoading, setActionLoading] = useState(false);

  /* -------- INIT -------- */
  useEffect(() => {
    const init = async () => {
      try {
        const meRes = await fetch(`${process.env.NEXT_PUBLIC_API_BASE_URL}/auth/me`, { credentials: "include" });
        if (!meRes.ok) { window.location.href = "/login"; return; }
        const me: User = await meRes.json();
        if (me.org_id === null) { window.location.href = "/org/onboarding"; return; }
        setUser(me);

        const apiRes = await fetch(`${process.env.NEXT_PUBLIC_API_BASE_URL}/reports/results`, { 
            credentials: "include", cache: "no-store", 
            headers: { "Pragma": "no-cache", "Cache-Control": "no-cache" }
        });
        if (!apiRes.ok) throw new Error("Failed to load audit reports");
        const rawData: BackendResponseItem[] = await apiRes.json();

        setApis(rawData.map((item) => ({
          id: item.api.id, name: item.api.name, url: item.api.url,
          is_active: true, created_at: new Date().toISOString(),
          audit_score: item.latest_audit ? item.latest_audit.score : null,
        })));
      } catch (err: any) {
        setError(err.message);
      } finally {
        setLoading(false);
      }
    };
    init();
  }, []);

  /* -------- HELPER: Modal Management -------- */
  const closeModal = () => {
    setActiveModal(null);
    setTargetApiId(null);
    setApiName("");
    setApiUrl("");
    setUserToRemove(null);
    setSelectedApiErrors([]);
    setActionLoading(false);
  };

  const openDeleteApiModal = (id: number) => {
    setTargetApiId(id);
    setActiveModal("DELETE_API");
  };

  const openManageUsersModal = async () => {
    setActiveModal("MANAGE_USERS");
    setActionLoading(true);
    try {
      const res = await fetch(`${process.env.NEXT_PUBLIC_API_BASE_URL}/user/list`, {
        method: "PATCH", 
        credentials: "include"
      });
      if (!res.ok) throw new Error("Failed to fetch users");
      const data = await res.json();
      setOrgUsers(data);
    } catch (err: any) {
      alert("Error fetching users: " + err.message);
      closeModal();
    } finally {
      setActionLoading(false);
    }
  };

  // NEW: Fetch and Show Errors
  const handleViewErrors = async (api: DashboardApi) => {
    setSelectedApiName(api.name);
    setActiveModal("VIEW_ERRORS");
    setActionLoading(true);
    
    try {
      const res = await fetch(`${process.env.NEXT_PUBLIC_API_BASE_URL}/apis/error/${api.id}`, {
        credentials: "include"
      });

      if (!res.ok) throw new Error("Failed to fetch error logs");
      
      const data: ApiErrorResponse = await res.json();
      
      // FIX: Safely convert objects to strings
      const errorStrings = data.results.map(r => {
        if (typeof r.details === "object" && r.details !== null) {
          // formatting it to look like JSON but cleaner
          return JSON.stringify(r.details, null, 2).replace(/"/g, '').replace(/{|}/g, ''); 
        }
        return String(r.details);
      });

      setSelectedApiErrors(errorStrings);

    } catch (err: any) {
      setSelectedApiErrors([`SYSTEM ERROR: ${err.message}`]);
    } finally {
      setActionLoading(false);
    }
  };


  /* -------- USER REMOVAL LOGIC -------- */
  const initiateRemoveUser = (user: OrgUser) => { setUserToRemove(user); setActiveModal("REMOVE_USER_CONFIRM"); };
  const cancelRemoveUser = () => { setUserToRemove(null); setActiveModal("MANAGE_USERS"); };
  const executeRemoveUser = async () => {
    if (!userToRemove) return;
    setActionLoading(true);
    try {
      const res = await fetch(`${process.env.NEXT_PUBLIC_API_BASE_URL}/organizations/remove_user`, {
        method: "POST", credentials: "include", headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ user_id: userToRemove.id })
      });
      if (!res.ok) { const data = await res.json(); throw new Error(data.detail || "Failed to remove user"); }
      setOrgUsers((prev) => prev.filter((u) => u.id !== userToRemove.id));
      setActiveModal("MANAGE_USERS"); setUserToRemove(null);
    } catch (err: any) { alert(err.message); } finally { setActionLoading(false); }
  };

  /* -------- STANDARD ACTIONS -------- */
  const handleLogout = async () => { await fetch(`${process.env.NEXT_PUBLIC_API_BASE_URL}/auth/logout`, { method: "POST", credentials: "include" }); window.location.href = "/login"; };
  
  const confirmDeleteOrg = async () => {
    setActionLoading(true);
    try {
      const res = await fetch(`${process.env.NEXT_PUBLIC_API_BASE_URL}/organizations/delete`, { method: "DELETE", credentials: "include" });
      if (!res.ok) throw new Error("Delete failed");
      window.location.href = "/org/onboarding";
    } catch (err: any) { alert(err.message); setActionLoading(false); }
  };

  const confirmLeaveOrg = async () => {
    setActionLoading(true);
    try {
      const res = await fetch(`${process.env.NEXT_PUBLIC_API_BASE_URL}/organizations/leave`, { method: "POST", credentials: "include" });
      if (!res.ok) throw new Error("Leave failed");
      window.location.href = "/org/onboarding";
    } catch (err: any) { alert(err.message); setActionLoading(false); }
  };

  const confirmCreateApi = async () => {
    if (!apiName || !apiUrl) return;
    setActionLoading(true);
    try {
      const res = await fetch(`${process.env.NEXT_PUBLIC_API_BASE_URL}/apis/create`, {
          method: "POST", credentials: "include", headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ name: apiName, url: apiUrl }),
      });
      if (!res.ok) throw new Error("Create failed");
      window.location.reload();
    } catch (err: any) { alert(err.message); setActionLoading(false); }
  };

  const confirmDeleteApi = async () => {
    if (!targetApiId) return;
    setActionLoading(true);
    try {
      const res = await fetch(`${process.env.NEXT_PUBLIC_API_BASE_URL}/apis/delete/${targetApiId}`, { method: "DELETE", credentials: "include" });
      if (!res.ok) throw new Error("Delete failed");
      setApis((prev) => prev.filter((api) => api.id !== targetApiId));
      closeModal();
    } catch (err: any) { alert(err.message); } finally { setActionLoading(false); }
  };

  /* -------- RENDER -------- */
  if (loading) return <p style={{ textAlign: "center", marginTop: "20vh", color: "#b6ff00", fontSize: "1.5rem" }}>LOADING SYSTEM...</p>;
  if (error) return <p className="error-text" style={{ textAlign: "center", marginTop: "20vh", fontSize: "1.5rem" }}>{error}</p>;

  return (
    <>
      <style jsx global>{`
        .scanline-bg { position: fixed; top: 0; left: 0; width: 100vw; height: 100vh; background: linear-gradient(to bottom, rgba(255,255,255,0), rgba(255,255,255,0) 50%, rgba(0,0,0,0.1) 50%, rgba(0,0,0,0.1)); background-size: 100% 4px; opacity: 0.05; pointer-events: none; z-index: 9999; }
        ::-webkit-scrollbar { width: 8px; } ::-webkit-scrollbar-track { background: #000; } ::-webkit-scrollbar-thumb { background: #333; } ::-webkit-scrollbar-thumb:hover { background: #b6ff00; }
        
        .dashboard-table { width: 100%; border-collapse: collapse; font-family: monospace; font-size: 1.25rem; }
        .dashboard-table th { text-align: left; padding: 1.5rem; border-bottom: 2px solid #b6ff00; color: #b6ff00; text-transform: uppercase; letter-spacing: 0.1em; font-weight: 700; }
        .dashboard-table td { padding: 1.5rem; border-bottom: 1px solid #222; color: #eee; }
        .dashboard-table tr:hover td { background: rgba(182, 255, 0, 0.03); }
        .action-link:hover { text-decoration: underline; text-shadow: 0 0 5px #b6ff00; }
        
        /* Clickable API Name Style */
        .api-name-cell { cursor: pointer; transition: color 0.2s; }
        .api-name-cell:hover { color: #b6ff00; text-shadow: 0 0 8px rgba(182, 255, 0, 0.5); text-decoration: underline; }

        /* Modal General */
        .modal-overlay { position: fixed; top: 0; left: 0; right: 0; bottom: 0; background: rgba(0,0,0,0.8); display: flex; align-items: center; justify-content: center; z-index: 999; backdrop-filter: blur(2px); }
        .modal { background: #000; border: 1px solid #b6ff00; padding: 2rem; width: 500px; box-shadow: 0 0 20px rgba(182, 255, 0, 0.2); }
        
        /* Modal Variants */
        .modal-large { width: 800px; max-height: 80vh; overflow-y: auto; }
        .modal-danger { border-color: #ff4d4d; box-shadow: 0 0 20px rgba(255, 77, 77, 0.2); }
        
        /* Error List Styles */
        .error-log { font-family: monospace; background: #111; padding: 1rem; border: 1px solid #333; max-height: 400px; overflow-y: auto; }
        .error-entry { color: #ff4d4d; border-bottom: 1px dashed #333; padding: 0.5rem 0; display: flex; gap: 0.5rem; }
        .error-entry:before { content: ">>"; color: #ff4d4d; opacity: 0.5; }
        .error-entry:last-child { border-bottom: none; }
        .no-errors { color: #b6ff00; text-align: center; padding: 2rem; font-style: italic; }

        .modal input { width: 100%; margin-bottom: 1rem; padding: 1rem; background: #111; border: 1px solid #333; color: #fff; font-family: monospace; font-size: 1.1rem; }
        .modal h3 { color: #b6ff00; margin-top: 0; text-transform: uppercase; font-size: 1.5rem; margin-bottom: 1rem; }
        .modal p { color: #ccc; margin-bottom: 2rem; font-family: monospace; line-height: 1.5; }

        .btn { padding: 0.8rem 2rem; border: none; font-weight: bold; cursor: pointer; font-size: 1rem; font-family: monospace; }
        .btn-primary { background: #b6ff00; color: #000; margin-left: 1rem; }
        .btn-primary:hover { opacity: 0.8; }
        .btn-danger { background: #ff4d4d; color: #000; margin-left: 1rem; }
        .btn-danger:hover { opacity: 0.8; }
        .btn-cancel { background: #333; color: #fff; }
        .btn-cancel:hover { background: #444; }
        .btn-sm-danger { background: transparent; border: 1px solid #ff4d4d; color: #ff4d4d; padding: 0.2rem 0.5rem; font-size: 0.8rem; cursor: pointer; font-family: monospace; }
        .btn-sm-danger:hover { background: #ff4d4d; color: #000; }
        
        .user-list { width: 100%; border-collapse: collapse; font-family: monospace; }
        .user-list td { padding: 0.8rem 0; border-bottom: 1px dashed #333; color: #eee; }
        .role-badge { font-size: 0.8rem; padding: 0.2rem 0.5rem; border: 1px solid #666; color: #aaa; margin-left: 1rem; text-transform: uppercase; }
        .check-item { margin-bottom: 1.5rem; border-bottom: 1px dashed #333; padding-bottom: 1rem; }
        .check-title { color: #b6ff00; font-weight: bold; display: block; margin-bottom: 0.5rem; font-family: monospace; }
        .check-desc { color: #aaa; font-size: 0.9rem; font-family: sans-serif; }
      `}</style>

      <div className="scanline-bg" />

      {/* HEADER */}
      <div style={{ position: "fixed", top: 0, left: 0, right: 0, height: "140px", padding: "0 3rem", display: "flex", alignItems: "center", justifyContent: "space-between", color: "#b6ff00", backgroundColor: "#000", zIndex: 100, borderBottom: "1px solid #222" }}>
        <div style={{ fontWeight: 700, letterSpacing: "0.15em", fontSize: "1.5rem", width: "250px" }}>ASYNCGUARD</div>
        <div style={{ flex: 1, textAlign: "center" }}><h1 style={{ margin: 0, fontSize: "4rem", letterSpacing: "0.3em", textShadow: "0 0 10px rgba(182, 255, 0, 0.3)" }}>DASHBOARD</h1></div>
        <div style={{ width: "auto", minWidth: "250px", textAlign: "right", fontSize: "1rem", letterSpacing: "0.12em" }}>
          <div style={{ display: "flex", gap: "1.5rem", justifyContent: "flex-end", marginBottom: "0.8rem", whiteSpace: "nowrap" }}>
            <span className="action-link" onClick={() => setActiveModal("HELP")} style={{cursor: 'pointer'}}>[help]</span>
            {user?.role === "admin" ? (
              <>
                <span className="action-link" onClick={openManageUsersModal} style={{cursor: 'pointer'}}>[users]</span>
                <span className="action-link" onClick={() => setActiveModal("DELETE_ORG")} style={{ cursor: "pointer", color: '#ff6b6b' }}>[destroy org]</span>
              </>
            ) : (
              <span className="action-link" onClick={() => setActiveModal("LEAVE_ORG")} style={{ cursor: "pointer", color: '#ff6b6b' }}>[leave org]</span>
            )}
            <span className="action-link" onClick={handleLogout} style={{ cursor: "pointer" }}>[logout]</span>
          </div>
          {user?.role === "admin" && (
            <button style={{ background: "transparent", border: "1px solid #b6ff00", color: "#b6ff00", padding: "0.5rem 1.2rem", fontSize: "0.9rem", fontFamily: "monospace", cursor: "pointer", marginTop: "0.2rem" }} onClick={() => setActiveModal("CREATE_API")}>
              + CREATE NEW API
            </button>
          )}
        </div>
      </div>

      {/* MAIN CONTENT */}
      <main style={{ marginTop: "180px", paddingBottom: "4rem", width: "95%", maxWidth: "1800px", marginLeft: "auto", marginRight: "auto" }}>
        <table className="dashboard-table">
          <thead>
            <tr>
              <th style={{ width: "20%" }}>Name</th>
              <th style={{ width: "35%" }}>URL</th>
              <th style={{ width: "15%" }}>Created</th>
              <th style={{ width: "10%" }}>Status</th>
              <th style={{ width: "10%" }}>Score</th>
              {user?.role === "admin" && <th style={{ width: "10%", textAlign: "right" }}>Actions</th>}
            </tr>
          </thead>
          <tbody>
            {apis.length === 0 && (<tr><td colSpan={user?.role === "admin" ? 6 : 5} style={{ textAlign: "center", opacity: 0.5, padding: "6rem" }}>// NO APIS DETECTED IN SYSTEM</td></tr>)}
            {apis.map((api) => (
              <tr key={api.id}>
                {/* NEW: Clickable Name Cell */}
                <td 
                  className="api-name-cell"
                  style={{ fontWeight: "bold", color: "#fff", fontSize: "1.4rem" }}
                  onClick={() => handleViewErrors(api)}
                  title="Click to view failure logs"
                >
                  {api.name}
                </td>
                
                <td style={{ fontFamily: "monospace", opacity: 0.8 }}>{api.url}</td>
                <td>{new Date(api.created_at).toLocaleDateString()}</td>
                <td><span style={{ color: api.is_active ? "#b6ff00" : "#666", border: `1px solid ${api.is_active ? "#b6ff00" : "#666"}`, padding: "0.3rem 0.6rem", fontSize: "0.9rem", fontWeight: "bold" }}>{api.is_active ? "ACTIVE" : "INACTIVE"}</span></td>
                <td style={{ fontSize: "1.2rem", fontWeight: "bold" }}>
                    {api.audit_score !== null && api.audit_score !== undefined ? (
                        <span style={{ color: api.audit_score >= 90 ? "#b6ff00" : (api.audit_score >= 50 ? "#ffeb3b" : "#ff4d4d") }}>{api.audit_score}</span>
                    ) : (<span style={{ opacity: 0.3 }}>N/A</span>)}
                </td>
                {user?.role === "admin" && (
                  <td style={{ textAlign: "right" }}>
                    <span style={{ color: "#ff4d4d", cursor: "pointer", fontWeight: "bold" }} onClick={() => openDeleteApiModal(api.id)}>[DELETE]</span>
                  </td>
                )}
              </tr>
            ))}
          </tbody>
        </table>
      </main>

      {/* -------- MODALS -------- */}
      
      {/* 1. VIEW ERRORS (NEW) */}
      {activeModal === "VIEW_ERRORS" && (
        <div className="modal-overlay">
          <div className="modal modal-large">
            <h3>DIAGNOSTIC REPORT: <span style={{color: "#fff"}}>{selectedApiName}</span></h3>
            
            <div className="error-log">
              {actionLoading ? (
                <p style={{textAlign: 'center', padding: '1rem', margin: 0}}>FETCHING SYSTEM LOGS...</p>
              ) : selectedApiErrors.length > 0 ? (
                selectedApiErrors.map((err, idx) => (
                  <div key={idx} className="error-entry">{err}</div>
                ))
              ) : (
                <div className="no-errors">
                  [SYSTEM SECURE]<br/>
                  NO VULNERABILITIES DETECTED
                </div>
              )}
            </div>

            <div style={{ marginTop: "2rem", display: "flex", justifyContent: "flex-end" }}>
              <button className="btn btn-primary" onClick={closeModal}>CLOSE LOGS</button>
            </div>
          </div>
        </div>
      )}

      {/* 2. MANAGE USERS */}
      {activeModal === "MANAGE_USERS" && (
        <div className="modal-overlay">
          <div className="modal modal-large">
            <h3>ORG PERSONNEL DATABASE</h3>
            {actionLoading && !orgUsers.length ? (
              <p style={{color: "#b6ff00"}}>FETCHING RECORDS...</p>
            ) : (
              <table className="user-list">
                <tbody>
                  {orgUsers.map(orgUser => (
                    <tr key={orgUser.id}>
                      <td>{orgUser.email}<span className="role-badge">{orgUser.role}</span>{orgUser.id === user?.id && <span style={{marginLeft: "0.5rem", color: "#666"}}>(YOU)</span>}</td>
                      <td style={{ textAlign: "right" }}>
                        {orgUser.id !== user?.id && (<button className="btn-sm-danger" onClick={() => initiateRemoveUser(orgUser)}>[REMOVE]</button>)}
                      </td>
                    </tr>
                  ))}
                  {orgUsers.length === 0 && (<tr><td colSpan={2} style={{textAlign: "center", padding: "2rem"}}>NO OTHER USERS FOUND</td></tr>)}
                </tbody>
              </table>
            )}
            <div style={{ marginTop: "2rem", display: "flex", justifyContent: "flex-end" }}>
              <button className="btn btn-cancel" onClick={closeModal}>CLOSE</button>
            </div>
          </div>
        </div>
      )}

      {/* 3. REMOVE USER CONFIRM */}
      {activeModal === "REMOVE_USER_CONFIRM" && userToRemove && (
        <div className="modal-overlay">
          <div className="modal modal-danger">
            <h3 style={{ color: "#ff4d4d" }}>REVOKE ACCESS?</h3>
            <p>Are you sure you want to remove <strong>{userToRemove.email}</strong>? They will lose all access immediately.</p>
            <div style={{ marginTop: "1rem", display: "flex", justifyContent: "flex-end" }}>
              <button className="btn btn-cancel" onClick={cancelRemoveUser}>RETURN</button>
              <button className="btn btn-danger" onClick={executeRemoveUser} disabled={actionLoading}>{actionLoading ? "REVOKING..." : "CONFIRM REMOVAL"}</button>
            </div>
          </div>
        </div>
      )}

      {/* 4. CREATE API */}
      {activeModal === "CREATE_API" && (
        <div className="modal-overlay">
          <div className="modal">
            <h3>Initiate New Endpoint</h3>
            <input placeholder="API Identifier (Name)" value={apiName} onChange={(e) => setApiName(e.target.value)} autoFocus />
            <input placeholder="Endpoint URL (https://...)" value={apiUrl} onChange={(e) => setApiUrl(e.target.value)} />
            <div style={{ marginTop: "1rem", display: "flex", justifyContent: "flex-end" }}>
              <button className="btn btn-cancel" onClick={closeModal}>CANCEL</button>
              <button className="btn btn-primary" onClick={confirmCreateApi} disabled={actionLoading}>{actionLoading ? "PROCESSING..." : "INITIALIZE"}</button>
            </div>
          </div>
        </div>
      )}

      {/* 5. DELETE ORG */}
      {activeModal === "DELETE_ORG" && (
        <div className="modal-overlay">
          <div className="modal modal-danger">
            <h3 style={{ color: "#ff4d4d" }}>CRITICAL WARNING</h3>
            <p>You are about to <strong>PERMANENTLY DESTROY</strong> this organization and all associated data. This action cannot be undone.</p>
            <div style={{ marginTop: "1rem", display: "flex", justifyContent: "flex-end" }}>
              <button className="btn btn-cancel" onClick={closeModal}>ABORT</button>
              <button className="btn btn-danger" onClick={confirmDeleteOrg} disabled={actionLoading}>{actionLoading ? "DESTROYING..." : "CONFIRM DESTRUCTION"}</button>
            </div>
          </div>
        </div>
      )}

      {/* 6. LEAVE ORG */}
      {activeModal === "LEAVE_ORG" && (
        <div className="modal-overlay">
          <div className="modal" style={{ borderColor: "#ffeb3b", boxShadow: "0 0 20px rgba(255, 235, 59, 0.2)" }}>
            <h3 style={{ color: "#ffeb3b" }}>LEAVE ORGANIZATION</h3>
            <p>Are you sure you want to disconnect? You will lose access until re-invited.</p>
            <div style={{ marginTop: "1rem", display: "flex", justifyContent: "flex-end" }}>
              <button className="btn btn-cancel" onClick={closeModal}>CANCEL</button>
              <button className="btn btn-danger" style={{ background: "#ffeb3b", color: "#000" }} onClick={confirmLeaveOrg} disabled={actionLoading}>{actionLoading ? "LEAVING..." : "CONFIRM LEAVE"}</button>
            </div>
          </div>
        </div>
      )}

      {/* 7. DELETE API */}
      {activeModal === "DELETE_API" && (
        <div className="modal-overlay">
          <div className="modal" style={{ borderColor: "#ff4d4d" }}>
            <h3 style={{ color: "#ff4d4d" }}>DELETE ENDPOINT</h3>
            <p>Terminate this API endpoint monitoring? All historical audit data will be erased.</p>
            <div style={{ marginTop: "1rem", display: "flex", justifyContent: "flex-end" }}>
              <button className="btn btn-cancel" onClick={closeModal}>CANCEL</button>
              <button className="btn btn-danger" onClick={confirmDeleteApi} disabled={actionLoading}>{actionLoading ? "DELETING..." : "TERMINATE"}</button>
            </div>
          </div>
        </div>
      )}

      {/* 8. HELP MODAL */}
      {activeModal === "HELP" && (
        <div className="modal-overlay">
          <div className="modal modal-large">
            <h3>SYSTEM AUDIT PROTOCOLS</h3>
            <div className="check-item"><span className="check-title">Authentication Required Check</span><span className="check-desc">Ensures protected APIs cannot be accessed without valid authentication tokens.</span></div>
            <div className="check-item"><span className="check-title">Authorization (RBAC) Check</span><span className="check-desc">Verifies only allowed roles (admin, auditor, viewer) can access specific endpoints.</span></div>
            <div className="check-item"><span className="check-title">HTTPS Enforcement Check</span><span className="check-desc">Confirms APIs are not accessible over plain HTTP to prevent interception.</span></div>
            <div className="check-item"><span className="check-title">HTTP Method Restriction Check</span><span className="check-desc">Ensures only intended HTTP methods (GET/POST/etc.) are enabled for the resource.</span></div>
            <div className="check-item"><span className="check-title">Input Validation Check</span><span className="check-desc">Confirms APIs reject malformed or missing inputs with appropriate status codes.</span></div>
            <div className="check-item"><span className="check-title">Error Handling Consistency Check</span><span className="check-desc">Ensures error responses do not leak stack traces or sensitive infrastructure info.</span></div>
            <div className="check-item"><span className="check-title">Rate Limiting / Abuse Protection Check</span><span className="check-desc">Detects missing request throttling on sensitive endpoints to prevent DoS.</span></div>
            <div className="check-item"><span className="check-title">Sensitive Header Leakage Check</span><span className="check-desc">Ensures server version banners (Server, X-Powered-By) are hidden from response headers.</span></div>
            <div className="check-item"><span className="check-title">CORS Misconfiguration Check</span><span className="check-desc">Ensures APIs do not allow overly permissive cross-origin access.</span></div>
            <div className="check-item" style={{borderBottom: 'none'}}><span className="check-title">Idempotency Safety Check</span><span className="check-desc">Ensures retries on non-safe methods (POST/PUT) do not create duplicate resources.</span></div>
            <div style={{ marginTop: "2rem", display: "flex", justifyContent: "flex-end" }}>
              <button className="btn btn-primary" onClick={closeModal}>CLOSE TERMINAL</button>
            </div>
          </div>
        </div>
      )}
    </>
  );
}