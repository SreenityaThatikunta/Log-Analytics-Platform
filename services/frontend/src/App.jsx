import { useEffect, useState } from "react";

function resolveApiUrl() {
  const configured = import.meta.env.VITE_QUERY_API_URL;
  const hostname = window.location.hostname;

  if (hostname === "localhost" || hostname === "127.0.0.1") {
    return "http://localhost:8000";
  }

  if (configured) {
    return configured;
  }

  return `${window.location.origin}/api`;
}

const API_URL = resolveApiUrl();

const initialFilters = {
  service: "auth",
  level: "error",
};

function formatHit(hit) {
  const source = hit._source ?? {};
  const timestamp = source.timestamp
    ? new Date(source.timestamp * 1000).toLocaleString()
    : "Unknown";

  return {
    id: hit._id,
    service: source.service ?? "unknown",
    level: source.level ?? "unknown",
    message: source.message ?? "",
    timestamp,
  };
}

export default function App() {
  const [filters, setFilters] = useState(initialFilters);
  const [logs, setLogs] = useState([]);
  const [status, setStatus] = useState("Idle");
  const [error, setError] = useState("");

  useEffect(() => {
    void fetchLogs();
  }, []);

  async function fetchLogs() {
    setStatus("Loading");
    setError("");

    const params = new URLSearchParams(filters);

    try {
      const response = await fetch(`${API_URL}/logs?${params.toString()}`);
      if (!response.ok) {
        throw new Error(`Query service returned ${response.status}`);
      }

      const data = await response.json();
      const hits = data.hits?.hits ?? [];
      setLogs(hits.map(formatHit));
      setStatus(`Loaded ${hits.length} log(s)`);
    } catch (err) {
      setLogs([]);
      setStatus("Error");
      setError(err.message);
    }
  }

  function onSubmit(event) {
    event.preventDefault();
    void fetchLogs();
  }

  return (
    <main className="page-shell">
      <section className="hero-card">
        <p className="eyebrow">Phase 2 Local Dashboard</p>
        <h1>Log Analytics Platform</h1>
        <p className="hero-copy">
          Query indexed logs by service and level while the collector, processor,
          and Elasticsearch run in Docker.
        </p>
      </section>

      <section className="panel">
        <form className="filters" onSubmit={onSubmit}>
          <label>
            <span>Service</span>
            <input
              value={filters.service}
              onChange={(event) =>
                setFilters((current) => ({
                  ...current,
                  service: event.target.value,
                }))
              }
            />
          </label>
          <label>
            <span>Level</span>
            <input
              value={filters.level}
              onChange={(event) =>
                setFilters((current) => ({
                  ...current,
                  level: event.target.value,
                }))
              }
            />
          </label>
          <button type="submit">Search Logs</button>
        </form>

        <div className="status-row">
          <span>{status}</span>
          {error ? <span className="error-text">{error}</span> : null}
        </div>

        <div className="results">
          {logs.length === 0 ? (
            <div className="empty-state">No logs found for the current filters.</div>
          ) : (
            logs.map((log) => (
              <article key={log.id} className="log-card">
                <div className="log-topline">
                  <strong>{log.service}</strong>
                  <span className="pill">{log.level}</span>
                </div>
                <p>{log.message}</p>
                <time>{log.timestamp}</time>
              </article>
            ))
          )}
        </div>
      </section>
    </main>
  );
}
