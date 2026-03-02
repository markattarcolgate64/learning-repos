import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import api from '../api/client';

function DashboardPage() {
  const navigate = useNavigate();
  const [projects, setProjects] = useState([]);
  const [selectedProject, setSelectedProject] = useState('');
  const [stats, setStats] = useState(null);
  const [recentTasks, setRecentTasks] = useState([]);
  const [loading, setLoading] = useState(false);
  const [projectsLoading, setProjectsLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    api.get('/api/projects')
      .then((res) => {
        setProjects(res.data);
      })
      .catch(() => {
        setError('Failed to load projects');
      })
      .finally(() => {
        setProjectsLoading(false);
      });
  }, []);

  useEffect(() => {
    if (!selectedProject) return;

    setLoading(true);

    api.get(`/api/projects/${selectedProject}/tasks?limit=5`)
      .then((res) => {
        setRecentTasks(res.data.tasks);
        setLoading(false);
      })
      .catch(() => setLoading(false));

    api.get(`/api/dashboard/stats?projectId=${selectedProject}`)
      .then((res) => setStats(res.data))
      .catch(() => {});
  }, [selectedProject]);

  const handleProjectChange = (e) => {
    setSelectedProject(e.target.value);
    setStats(null);
    setRecentTasks([]);
  };

  const priorityColors = {
    low: '#22c55e',
    medium: '#f59e0b',
    high: '#ef4444',
    critical: '#7c3aed',
  };

  const statusLabels = {
    todo: 'To Do',
    in_progress: 'In Progress',
    in_review: 'In Review',
    done: 'Done',
  };

  return (
    <div>
      <div style={styles.pageHeader}>
        <h1 style={styles.pageTitle}>Dashboard</h1>
        <p style={styles.pageSubtitle}>Overview of your projects and tasks</p>
      </div>

      <div style={styles.selectorRow}>
        <label style={styles.selectorLabel} htmlFor="project-select">
          Select Project
        </label>
        <select
          id="project-select"
          value={selectedProject}
          onChange={handleProjectChange}
          style={styles.select}
          disabled={projectsLoading}
        >
          <option value="">
            {projectsLoading ? 'Loading projects...' : '-- Choose a project --'}
          </option>
          {projects.map((project) => (
            <option key={project.id} value={project.id}>
              {project.name} ({project.taskCount} tasks)
            </option>
          ))}
        </select>
      </div>

      {error && <div style={styles.errorBanner}>{error}</div>}

      {selectedProject && !loading && stats && (
        <>
          <div style={styles.statsGrid}>
            <div style={styles.statCard}>
              <span style={styles.statValue}>{stats.totalTasks}</span>
              <span style={styles.statLabel}>Total Tasks</span>
            </div>
            <div style={styles.statCard}>
              <span style={styles.statValue}>{stats.totalProjects}</span>
              <span style={styles.statLabel}>Total Projects</span>
            </div>
            {stats.byStatus && Object.entries(stats.byStatus).map(([status, count]) => (
              <div key={status} style={styles.statCard}>
                <span style={styles.statValue}>{count}</span>
                <span style={styles.statLabel}>{statusLabels[status] || status}</span>
              </div>
            ))}
          </div>

          {stats.byPriority && (
            <div style={styles.section}>
              <h3 style={styles.sectionTitle}>By Priority</h3>
              <div style={styles.priorityBar}>
                {Object.entries(stats.byPriority).map(([priority, count]) => (
                  <div key={priority} style={styles.priorityItem}>
                    <span
                      style={{
                        ...styles.priorityDot,
                        backgroundColor: priorityColors[priority] || '#94a3b8',
                      }}
                    />
                    <span style={styles.priorityLabel}>
                      {priority}: {count}
                    </span>
                  </div>
                ))}
              </div>
            </div>
          )}
        </>
      )}

      {selectedProject && loading && (
        <div style={styles.loadingState}>
          <p>Loading project data...</p>
        </div>
      )}

      {selectedProject && !loading && recentTasks.length > 0 && (
        <div style={styles.section}>
          <div style={styles.sectionHeader}>
            <h3 style={styles.sectionTitle}>Recent Tasks</h3>
            <button
              onClick={() => navigate(`/projects/${selectedProject}`)}
              style={styles.viewAllButton}
            >
              View All Tasks
            </button>
          </div>
          <div style={styles.taskList}>
            {recentTasks.map((task) => (
              <div key={task.id} style={styles.taskRow}>
                <div style={styles.taskInfo}>
                  <span style={styles.taskTitle}>{task.title}</span>
                  <span style={styles.taskMeta}>
                    {statusLabels[task.status] || task.status}
                  </span>
                </div>
                <span
                  style={{
                    ...styles.priorityBadge,
                    backgroundColor: priorityColors[task.priority] || '#94a3b8',
                  }}
                >
                  {task.priority}
                </span>
              </div>
            ))}
          </div>
        </div>
      )}

      {!selectedProject && !projectsLoading && (
        <div style={styles.emptyState}>
          <h3 style={styles.emptyTitle}>Select a project to get started</h3>
          <p style={styles.emptyText}>
            Choose a project from the dropdown above to view its stats and recent tasks.
          </p>
        </div>
      )}

      {projects.length > 0 && (
        <div style={styles.section}>
          <h3 style={styles.sectionTitle}>All Projects</h3>
          <div style={styles.projectGrid}>
            {projects.map((project) => (
              <div
                key={project.id}
                style={styles.projectCard}
                onClick={() => navigate(`/projects/${project.id}`)}
              >
                <h4 style={styles.projectName}>{project.name}</h4>
                <p style={styles.projectDescription}>
                  {project.description || 'No description'}
                </p>
                <span style={styles.projectTaskCount}>
                  {project.taskCount} tasks
                </span>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
}

const styles = {
  pageHeader: {
    marginBottom: 24,
  },
  pageTitle: {
    fontSize: 24,
    fontWeight: 700,
    color: '#1e293b',
    marginBottom: 4,
  },
  pageSubtitle: {
    fontSize: 14,
    color: '#64748b',
  },
  selectorRow: {
    display: 'flex',
    alignItems: 'center',
    gap: 12,
    marginBottom: 24,
    padding: '16px 20px',
    backgroundColor: '#ffffff',
    borderRadius: 10,
    boxShadow: '0 1px 3px rgba(0,0,0,0.06)',
  },
  selectorLabel: {
    fontSize: 14,
    fontWeight: 600,
    color: '#374151',
    whiteSpace: 'nowrap',
  },
  select: {
    flex: 1,
    padding: '9px 12px',
    border: '1px solid #d1d5db',
    borderRadius: 8,
    fontSize: 14,
    backgroundColor: '#ffffff',
    cursor: 'pointer',
    outline: 'none',
  },
  errorBanner: {
    padding: '10px 14px',
    backgroundColor: '#fef2f2',
    color: '#dc2626',
    border: '1px solid #fecaca',
    borderRadius: 8,
    fontSize: 13,
    marginBottom: 16,
  },
  statsGrid: {
    display: 'grid',
    gridTemplateColumns: 'repeat(auto-fill, minmax(160px, 1fr))',
    gap: 14,
    marginBottom: 24,
  },
  statCard: {
    display: 'flex',
    flexDirection: 'column',
    alignItems: 'center',
    padding: '20px 16px',
    backgroundColor: '#ffffff',
    borderRadius: 10,
    boxShadow: '0 1px 3px rgba(0,0,0,0.06)',
    gap: 4,
  },
  statValue: {
    fontSize: 28,
    fontWeight: 700,
    color: '#1e293b',
  },
  statLabel: {
    fontSize: 12,
    color: '#64748b',
    textTransform: 'uppercase',
    letterSpacing: '0.5px',
    fontWeight: 500,
  },
  section: {
    marginBottom: 24,
  },
  sectionHeader: {
    display: 'flex',
    justifyContent: 'space-between',
    alignItems: 'center',
    marginBottom: 12,
  },
  sectionTitle: {
    fontSize: 16,
    fontWeight: 600,
    color: '#1e293b',
    marginBottom: 12,
  },
  viewAllButton: {
    padding: '6px 14px',
    backgroundColor: '#eff6ff',
    color: '#3b82f6',
    border: '1px solid #bfdbfe',
    borderRadius: 6,
    fontSize: 13,
    fontWeight: 500,
    cursor: 'pointer',
  },
  priorityBar: {
    display: 'flex',
    gap: 20,
    padding: '14px 20px',
    backgroundColor: '#ffffff',
    borderRadius: 10,
    boxShadow: '0 1px 3px rgba(0,0,0,0.06)',
  },
  priorityItem: {
    display: 'flex',
    alignItems: 'center',
    gap: 6,
  },
  priorityDot: {
    display: 'inline-block',
    width: 10,
    height: 10,
    borderRadius: '50%',
  },
  priorityLabel: {
    fontSize: 13,
    color: '#475569',
    textTransform: 'capitalize',
  },
  taskList: {
    display: 'flex',
    flexDirection: 'column',
    gap: 8,
  },
  taskRow: {
    display: 'flex',
    justifyContent: 'space-between',
    alignItems: 'center',
    padding: '12px 16px',
    backgroundColor: '#ffffff',
    borderRadius: 8,
    boxShadow: '0 1px 2px rgba(0,0,0,0.04)',
  },
  taskInfo: {
    display: 'flex',
    flexDirection: 'column',
    gap: 2,
  },
  taskTitle: {
    fontSize: 14,
    fontWeight: 500,
    color: '#1e293b',
  },
  taskMeta: {
    fontSize: 12,
    color: '#64748b',
  },
  priorityBadge: {
    padding: '3px 10px',
    borderRadius: 12,
    color: '#ffffff',
    fontSize: 11,
    fontWeight: 600,
    textTransform: 'uppercase',
    letterSpacing: '0.3px',
  },
  loadingState: {
    textAlign: 'center',
    padding: 40,
    color: '#64748b',
    fontSize: 14,
  },
  emptyState: {
    textAlign: 'center',
    padding: '60px 20px',
    backgroundColor: '#ffffff',
    borderRadius: 10,
    boxShadow: '0 1px 3px rgba(0,0,0,0.06)',
    marginBottom: 24,
  },
  emptyTitle: {
    fontSize: 18,
    fontWeight: 600,
    color: '#374151',
    marginBottom: 8,
  },
  emptyText: {
    fontSize: 14,
    color: '#64748b',
  },
  projectGrid: {
    display: 'grid',
    gridTemplateColumns: 'repeat(auto-fill, minmax(280px, 1fr))',
    gap: 14,
  },
  projectCard: {
    padding: '18px 20px',
    backgroundColor: '#ffffff',
    borderRadius: 10,
    boxShadow: '0 1px 3px rgba(0,0,0,0.06)',
    cursor: 'pointer',
    transition: 'box-shadow 0.15s',
    border: '1px solid transparent',
  },
  projectName: {
    fontSize: 15,
    fontWeight: 600,
    color: '#1e293b',
    marginBottom: 6,
  },
  projectDescription: {
    fontSize: 13,
    color: '#64748b',
    marginBottom: 10,
    lineHeight: 1.4,
  },
  projectTaskCount: {
    fontSize: 12,
    color: '#3b82f6',
    fontWeight: 500,
  },
};

export default DashboardPage;
