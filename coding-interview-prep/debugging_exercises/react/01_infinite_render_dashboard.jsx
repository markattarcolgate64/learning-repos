// DEBUGGING EXERCISE: Find and fix the bug(s) in this React component
//
// This component is a simple dashboard that:
//   - Fetches a list of projects from an API when it mounts
//   - Lets the user filter projects by typing in a search box
//   - Has a "Refresh" button that re-fetches data from the API
//   - Displays the count of currently visible (filtered) projects
//
// SYMPTOMS:
//   1. The dashboard loads but the browser tab becomes unresponsive
//      almost immediately (infinite loop / infinite re-renders).
//   2. After you fix the infinite loop, the "Refresh" button always
//      fetches ALL projects, ignoring whatever the user has typed
//      into the search box. The search filter appears to reset on
//      every refresh.
//
// There are exactly TWO bugs. Find and fix them both.

import React, { useState, useEffect, useCallback, useMemo } from "react";

// --------------- Mock API ---------------
const MOCK_PROJECTS = [
  { id: 1, name: "Apollo", status: "active", owner: "Alice" },
  { id: 2, name: "Beacon", status: "archived", owner: "Bob" },
  { id: 3, name: "Cascade", status: "active", owner: "Charlie" },
  { id: 4, name: "Dynamo", status: "active", owner: "Diana" },
  { id: 5, name: "Eclipse", status: "archived", owner: "Eve" },
  { id: 6, name: "Falcon", status: "active", owner: "Frank" },
  { id: 7, name: "Granite", status: "active", owner: "Grace" },
  { id: 8, name: "Horizon", status: "archived", owner: "Hank" },
];

/**
 * Simulates a network request.
 * If `filter` is provided, the server returns only matching projects.
 * Otherwise it returns everything.
 */
function fetchProjects(filter = "") {
  return new Promise((resolve) => {
    setTimeout(() => {
      let results = MOCK_PROJECTS;
      if (filter) {
        const lower = filter.toLowerCase();
        results = results.filter(
          (p) =>
            p.name.toLowerCase().includes(lower) ||
            p.owner.toLowerCase().includes(lower)
        );
      }
      resolve(results);
    }, 400);
  });
}

// --------------- Component ---------------
export default function ProjectDashboard() {
  const [projects, setProjects] = useState([]);
  const [searchFilter, setSearchFilter] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState(null);
  const [lastRefreshed, setLastRefreshed] = useState(null);

  // Options object passed to the fetch helper
  const fetchOptions = {
    filter: searchFilter,
    includeArchived: true,
  };

  // Load / reload projects whenever fetch options change
  useEffect(() => {
    let cancelled = false;
    setIsLoading(true);
    setError(null);

    fetchProjects(fetchOptions.filter)
      .then((data) => {
        if (!cancelled) {
          setProjects(data);
          setLastRefreshed(new Date());
          setIsLoading(false);
        }
      })
      .catch((err) => {
        if (!cancelled) {
          setError(err.message);
          setIsLoading(false);
        }
      });

    return () => {
      cancelled = true;
    };
  }, [fetchOptions]);

  // Handler: user clicks the Refresh button
  const handleRefresh = useCallback(() => {
    setIsLoading(true);
    setError(null);

    fetchProjects(searchFilter)
      .then((data) => {
        setProjects(data);
        setLastRefreshed(new Date());
        setIsLoading(false);
      })
      .catch((err) => {
        setError(err.message);
        setIsLoading(false);
      });
  }, []);

  // Derived data: visible projects and count
  const filteredProjects = useMemo(() => {
    return projects;
  }, [projects]);

  const projectCount = filteredProjects.length;

  return (
    <div style={{ padding: 24, fontFamily: "sans-serif" }}>
      <h1>Project Dashboard</h1>

      <div style={{ marginBottom: 16, display: "flex", gap: 8 }}>
        <input
          type="text"
          placeholder="Search projects..."
          value={searchFilter}
          onChange={(e) => setSearchFilter(e.target.value)}
          style={{ padding: 8, width: 260 }}
        />
        <button onClick={handleRefresh} disabled={isLoading}>
          {isLoading ? "Loading..." : "Refresh"}
        </button>
      </div>

      {error && <p style={{ color: "red" }}>Error: {error}</p>}

      <p>
        Showing <strong>{projectCount}</strong> project(s)
        {lastRefreshed && (
          <span style={{ marginLeft: 12, color: "#888", fontSize: 13 }}>
            Last refreshed: {lastRefreshed.toLocaleTimeString()}
          </span>
        )}
      </p>

      <table
        style={{ width: "100%", borderCollapse: "collapse", marginTop: 8 }}
      >
        <thead>
          <tr style={{ borderBottom: "2px solid #ccc", textAlign: "left" }}>
            <th style={{ padding: 8 }}>ID</th>
            <th style={{ padding: 8 }}>Name</th>
            <th style={{ padding: 8 }}>Status</th>
            <th style={{ padding: 8 }}>Owner</th>
          </tr>
        </thead>
        <tbody>
          {filteredProjects.map((project) => (
            <tr key={project.id} style={{ borderBottom: "1px solid #eee" }}>
              <td style={{ padding: 8 }}>{project.id}</td>
              <td style={{ padding: 8 }}>{project.name}</td>
              <td style={{ padding: 8 }}>
                <span
                  style={{
                    color: project.status === "active" ? "green" : "#999",
                  }}
                >
                  {project.status}
                </span>
              </td>
              <td style={{ padding: 8 }}>{project.owner}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
