import React, { useState, useEffect, useCallback } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import api from '../api/client';
import TaskCard from '../components/TaskCard';
import TaskForm from '../components/TaskForm';

function debounce(fn, delay) {
  let timer;
  return function (...args) {
    clearTimeout(timer);
    timer = setTimeout(() => fn.apply(this, args), delay);
  };
}

function ProjectPage() {
  const { projectId } = useParams();
  const navigate = useNavigate();

  const [project, setProject] = useState(null);
  const [tasks, setTasks] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  const [searchQuery, setSearchQuery] = useState('');
  const [statusFilter, setStatusFilter] = useState('');
  const [priorityFilter, setPriorityFilter] = useState('');
  const [sortBy, setSortBy] = useState('createdAt');
  const [sortOrder, setSortOrder] = useState('desc');

  const [page, setPage] = useState(1);
  const [pagination, setPagination] = useState(null);

  const [showTaskForm, setShowTaskForm] = useState(false);

  useEffect(() => {
    setLoading(true);
    api.get(`/api/projects/${projectId}`)
      .then((res) => {
        setProject(res.data);
      })
      .catch(() => {
        setError('Failed to load project');
      })
      .finally(() => {
        setLoading(false);
      });
  }, [projectId]);

  const fetchTasks = useCallback(() => {
    const params = {
      page,
      limit: 10,
      status: statusFilter,
      priority: priorityFilter,
      search: searchQuery,
      sortBy,
      sortOrder,
    };

    api.get(`/api/projects/${projectId}/tasks`, { params })
      .then((res) => {
        setTasks(res.data.tasks);
        setPagination(res.data.pagination);
      })
      .catch(() => {
        setError('Failed to load tasks');
      });
  }, [projectId, page, statusFilter, priorityFilter, searchQuery, sortBy, sortOrder]);

  useEffect(() => {
    fetchTasks();
  }, [fetchTasks]);

  const debouncedSearch = useCallback(
    debounce((query) => {
      api.get(`/api/projects/${projectId}/tasks`, {
        params: {
          search: query,
          page: 1,
          limit: 10,
          status: statusFilter,
          priority: priorityFilter,
          sortBy,
          sortOrder,
        },
      }).then((res) => {
        setTasks(res.data.tasks);
        setPagination(res.data.pagination);
        setPage(1);
      });
    }, 300),
    []
  );

  const handleSearchChange = (e) => {
    const value = e.target.value;
    setSearchQuery(value);
    debouncedSearch(value);
  };

  const handleStatusChange = async (taskId, newStatus) => {
    try {
      await api.patch(`/api/tasks/${taskId}`, { status: newStatus });
      setTasks((prev) =>
        prev.map((t) => (t.id === taskId ? { ...t, status: newStatus } : t))
      );
    } catch {
      setError('Failed to update task status');
    }
  };

  const handleDeleteTask = async (taskId) => {
    try {
      await api.delete(`/api/tasks/${taskId}`);
      setTasks((prev) => prev.filter((t) => t.id !== taskId));
    } catch {
      setError('Failed to delete task');
    }
  };

  const handleTaskCreated = (newTask) => {
    setTasks((prev) => [newTask, ...prev]);
    setShowTaskForm(false);
  };

  const handleFilterChange = (setter) => (e) => {
    setter(e.target.value);
    setPage(1);
  };

  const handleSortChange = (field) => {
    if (sortBy === field) {
      setSortOrder((prev) => (prev === 'asc' ? 'desc' : 'asc'));
    } else {
      setSortBy(field);
      setSortOrder('desc');
    }
    setPage(1);
  };

  if (loading && !project) {
    return (
      <div style={styles.loadingState}>
        <p>Loading project...</p>
      </div>
    );
  }

  if (error && !project) {
    return (
      <div style={styles.errorState}>
        <p>{error}</p>
        <button onClick={() => navigate('/')} style={styles.backButton}>
          Back to Dashboard
        </button>
      </div>
    );
  }

  const filteredTasks = tasks;

  return (
    <div>
      <div style={styles.breadcrumb}>
        <button onClick={() => navigate('/')} style={styles.breadcrumbLink}>
          Dashboard
        </button>
        <span style={styles.breadcrumbSep}>/</span>
        <span style={styles.breadcrumbCurrent}>{project?.name}</span>
      </div>

      <div style={styles.projectHeader}>
        <div>
          <h1 style={styles.projectTitle}>{project?.name}</h1>
          <p style={styles.projectDescription}>
            {project?.description || 'No description provided'}
          </p>
        </div>
        <button
          onClick={() => setShowTaskForm(true)}
          style={styles.addButton}
        >
          + Add Task
        </button>
      </div>

      {error && <div style={styles.errorBanner}>{error}</div>}

      <div style={styles.toolbar}>
        <div style={styles.searchWrapper}>
          <input
            type="text"
            placeholder="Search tasks..."
            value={searchQuery}
            onChange={handleSearchChange}
            style={styles.searchInput}
          />
        </div>

        <div style={styles.filters}>
          <select
            value={statusFilter}
            onChange={handleFilterChange(setStatusFilter)}
            style={styles.filterSelect}
          >
            <option value="">All Statuses</option>
            <option value="todo">To Do</option>
            <option value="in_progress">In Progress</option>
            <option value="in_review">In Review</option>
            <option value="done">Done</option>
          </select>

          <select
            value={priorityFilter}
            onChange={handleFilterChange(setPriorityFilter)}
            style={styles.filterSelect}
          >
            <option value="">All Priorities</option>
            <option value="low">Low</option>
            <option value="medium">Medium</option>
            <option value="high">High</option>
            <option value="critical">Critical</option>
          </select>

          <div style={styles.sortButtons}>
            <button
              onClick={() => handleSortChange('createdAt')}
              style={{
                ...styles.sortButton,
                ...(sortBy === 'createdAt' ? styles.sortButtonActive : {}),
              }}
            >
              Date {sortBy === 'createdAt' && (sortOrder === 'asc' ? '\u2191' : '\u2193')}
            </button>
            <button
              onClick={() => handleSortChange('priority')}
              style={{
                ...styles.sortButton,
                ...(sortBy === 'priority' ? styles.sortButtonActive : {}),
              }}
            >
              Priority {sortBy === 'priority' && (sortOrder === 'asc' ? '\u2191' : '\u2193')}
            </button>
          </div>
        </div>
      </div>

      <div style={styles.taskList}>
        {filteredTasks.length === 0 ? (
          <div style={styles.emptyState}>
            <p style={styles.emptyText}>
              {searchQuery || statusFilter || priorityFilter
                ? 'No tasks match your filters.'
                : 'No tasks yet. Create one to get started!'}
            </p>
          </div>
        ) : (
          filteredTasks.map((task, index) => (
            <TaskCard
              key={index}
              task={task}
              onStatusChange={handleStatusChange}
              onDelete={handleDeleteTask}
            />
          ))
        )}
      </div>

      {pagination && pagination.total > 10 && (
        <div style={styles.pagination}>
          <button
            onClick={() => setPage((p) => Math.max(1, p - 1))}
            disabled={page <= 1}
            style={{
              ...styles.pageButton,
              opacity: page <= 1 ? 0.5 : 1,
            }}
          >
            Previous
          </button>
          <span style={styles.pageInfo}>
            Page {pagination.page} of {Math.ceil(pagination.total / pagination.limit)}
          </span>
          <button
            onClick={() => setPage((p) => p + 1)}
            disabled={page >= Math.ceil(pagination.total / pagination.limit)}
            style={{
              ...styles.pageButton,
              opacity:
                page >= Math.ceil(pagination.total / pagination.limit) ? 0.5 : 1,
            }}
          >
            Next
          </button>
        </div>
      )}

      {showTaskForm && (
        <TaskForm
          projectId={projectId}
          onTaskCreated={handleTaskCreated}
          onClose={() => setShowTaskForm(false)}
        />
      )}
    </div>
  );
}

const styles = {
  breadcrumb: {
    display: 'flex',
    alignItems: 'center',
    gap: 8,
    marginBottom: 20,
    fontSize: 13,
  },
  breadcrumbLink: {
    background: 'none',
    border: 'none',
    color: '#3b82f6',
    cursor: 'pointer',
    fontSize: 13,
    padding: 0,
  },
  breadcrumbSep: {
    color: '#94a3b8',
  },
  breadcrumbCurrent: {
    color: '#64748b',
  },
  projectHeader: {
    display: 'flex',
    justifyContent: 'space-between',
    alignItems: 'flex-start',
    marginBottom: 24,
    padding: '20px 24px',
    backgroundColor: '#ffffff',
    borderRadius: 10,
    boxShadow: '0 1px 3px rgba(0,0,0,0.06)',
  },
  projectTitle: {
    fontSize: 22,
    fontWeight: 700,
    color: '#1e293b',
    marginBottom: 4,
  },
  projectDescription: {
    fontSize: 14,
    color: '#64748b',
    maxWidth: 600,
  },
  addButton: {
    padding: '9px 18px',
    backgroundColor: '#3b82f6',
    color: '#ffffff',
    border: 'none',
    borderRadius: 8,
    fontSize: 14,
    fontWeight: 600,
    cursor: 'pointer',
    whiteSpace: 'nowrap',
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
  toolbar: {
    display: 'flex',
    flexDirection: 'column',
    gap: 12,
    marginBottom: 20,
    padding: '16px 20px',
    backgroundColor: '#ffffff',
    borderRadius: 10,
    boxShadow: '0 1px 3px rgba(0,0,0,0.06)',
  },
  searchWrapper: {
    width: '100%',
  },
  searchInput: {
    width: '100%',
    padding: '9px 14px',
    border: '1px solid #d1d5db',
    borderRadius: 8,
    fontSize: 14,
    outline: 'none',
  },
  filters: {
    display: 'flex',
    alignItems: 'center',
    gap: 10,
    flexWrap: 'wrap',
  },
  filterSelect: {
    padding: '7px 12px',
    border: '1px solid #d1d5db',
    borderRadius: 8,
    fontSize: 13,
    backgroundColor: '#ffffff',
    cursor: 'pointer',
    outline: 'none',
  },
  sortButtons: {
    display: 'flex',
    gap: 6,
    marginLeft: 'auto',
  },
  sortButton: {
    padding: '6px 12px',
    backgroundColor: '#f1f5f9',
    color: '#475569',
    border: '1px solid #e2e8f0',
    borderRadius: 6,
    fontSize: 12,
    fontWeight: 500,
    cursor: 'pointer',
  },
  sortButtonActive: {
    backgroundColor: '#eff6ff',
    color: '#3b82f6',
    borderColor: '#bfdbfe',
  },
  taskList: {
    display: 'flex',
    flexDirection: 'column',
    gap: 10,
  },
  emptyState: {
    textAlign: 'center',
    padding: '48px 20px',
    backgroundColor: '#ffffff',
    borderRadius: 10,
    boxShadow: '0 1px 3px rgba(0,0,0,0.06)',
  },
  emptyText: {
    fontSize: 14,
    color: '#64748b',
  },
  pagination: {
    display: 'flex',
    alignItems: 'center',
    justifyContent: 'center',
    gap: 16,
    marginTop: 20,
    padding: '14px 20px',
    backgroundColor: '#ffffff',
    borderRadius: 10,
    boxShadow: '0 1px 3px rgba(0,0,0,0.06)',
  },
  pageButton: {
    padding: '7px 16px',
    backgroundColor: '#f1f5f9',
    color: '#374151',
    border: '1px solid #e2e8f0',
    borderRadius: 6,
    fontSize: 13,
    fontWeight: 500,
    cursor: 'pointer',
  },
  pageInfo: {
    fontSize: 13,
    color: '#64748b',
  },
  loadingState: {
    textAlign: 'center',
    padding: 60,
    color: '#64748b',
    fontSize: 14,
  },
  errorState: {
    textAlign: 'center',
    padding: 60,
    display: 'flex',
    flexDirection: 'column',
    alignItems: 'center',
    gap: 16,
    color: '#dc2626',
  },
  backButton: {
    padding: '8px 18px',
    backgroundColor: '#f1f5f9',
    color: '#374151',
    border: '1px solid #e2e8f0',
    borderRadius: 8,
    fontSize: 14,
    cursor: 'pointer',
  },
};

export default ProjectPage;
