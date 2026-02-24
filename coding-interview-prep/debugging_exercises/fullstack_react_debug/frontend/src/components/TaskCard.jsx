import React, { useState } from 'react';

const priorityColors = {
  low: { bg: '#f0fdf4', text: '#16a34a', border: '#bbf7d0' },
  medium: { bg: '#fffbeb', text: '#d97706', border: '#fde68a' },
  high: { bg: '#fef2f2', text: '#dc2626', border: '#fecaca' },
  critical: { bg: '#f5f3ff', text: '#7c3aed', border: '#ddd6fe' },
};

const statusOptions = [
  { value: 'todo', label: 'To Do' },
  { value: 'in_progress', label: 'In Progress' },
  { value: 'in_review', label: 'In Review' },
  { value: 'done', label: 'Done' },
];

function TaskCard({ task, onStatusChange, onDelete }) {
  const [expanded, setExpanded] = useState(false);
  const [statusUpdating, setStatusUpdating] = useState(false);

  const colors = priorityColors[task.priority] || priorityColors.medium;

  const handleStatusChange = async (e) => {
    const newStatus = e.target.value;
    if (newStatus === task.status) return;

    setStatusUpdating(true);
    try {
      await onStatusChange(task.id, newStatus);
    } finally {
      setStatusUpdating(false);
    }
  };

  const formatDate = (dateStr) => {
    if (!dateStr) return '';
    const date = new Date(dateStr);
    return date.toLocaleDateString('en-US', {
      month: 'short',
      day: 'numeric',
      year: 'numeric',
    });
  };

  return (
    <div style={styles.card}>
      <div style={styles.cardHeader}>
        <div style={styles.titleRow}>
          <button
            onClick={() => setExpanded(!expanded)}
            style={styles.expandButton}
            aria-label={expanded ? 'Collapse' : 'Expand'}
          >
            {expanded ? '\u25BC' : '\u25B6'}
          </button>
          <h4 style={styles.title}>{task.title}</h4>
          <span
            style={{
              ...styles.priorityBadge,
              backgroundColor: colors.bg,
              color: colors.text,
              borderColor: colors.border,
            }}
          >
            {task.priority}
          </span>
        </div>

        <div style={styles.actions}>
          <select
            value={task.status}
            onChange={handleStatusChange}
            disabled={statusUpdating}
            style={{
              ...styles.statusSelect,
              opacity: statusUpdating ? 0.6 : 1,
            }}
          >
            {statusOptions.map((opt) => (
              <option key={opt.value} value={opt.value}>
                {opt.label}
              </option>
            ))}
          </select>

          <button
            onClick={() => onDelete(task.id)}
            style={styles.deleteButton}
            title="Delete task"
          >
            Delete
          </button>
        </div>
      </div>

      {expanded && (
        <div style={styles.cardBody}>
          <p style={styles.description}>
            {task.description || 'No description provided.'}
          </p>
          <div style={styles.meta}>
            {task.assignee && (
              <span style={styles.metaItem}>
                Assigned to: <strong>{task.assignee}</strong>
              </span>
            )}
            <span style={styles.metaItem}>
              Created: {formatDate(task.createdAt)}
            </span>
            {task.updatedAt && (
              <span style={styles.metaItem}>
                Updated: {formatDate(task.updatedAt)}
              </span>
            )}
          </div>
        </div>
      )}
    </div>
  );
}

const styles = {
  card: {
    backgroundColor: '#ffffff',
    borderRadius: 10,
    boxShadow: '0 1px 3px rgba(0,0,0,0.06)',
    overflow: 'hidden',
    border: '1px solid #f1f5f9',
  },
  cardHeader: {
    display: 'flex',
    justifyContent: 'space-between',
    alignItems: 'center',
    padding: '14px 18px',
    gap: 12,
  },
  titleRow: {
    display: 'flex',
    alignItems: 'center',
    gap: 10,
    flex: 1,
    minWidth: 0,
  },
  expandButton: {
    background: 'none',
    border: 'none',
    cursor: 'pointer',
    fontSize: 11,
    color: '#94a3b8',
    padding: '2px 4px',
    flexShrink: 0,
  },
  title: {
    fontSize: 14,
    fontWeight: 600,
    color: '#1e293b',
    margin: 0,
    overflow: 'hidden',
    textOverflow: 'ellipsis',
    whiteSpace: 'nowrap',
  },
  priorityBadge: {
    padding: '2px 9px',
    borderRadius: 10,
    fontSize: 11,
    fontWeight: 600,
    textTransform: 'capitalize',
    border: '1px solid',
    whiteSpace: 'nowrap',
    flexShrink: 0,
  },
  actions: {
    display: 'flex',
    alignItems: 'center',
    gap: 8,
    flexShrink: 0,
  },
  statusSelect: {
    padding: '5px 10px',
    border: '1px solid #d1d5db',
    borderRadius: 6,
    fontSize: 12,
    backgroundColor: '#ffffff',
    cursor: 'pointer',
    outline: 'none',
  },
  deleteButton: {
    padding: '5px 10px',
    backgroundColor: '#fef2f2',
    color: '#dc2626',
    border: '1px solid #fecaca',
    borderRadius: 6,
    fontSize: 12,
    fontWeight: 500,
    cursor: 'pointer',
  },
  cardBody: {
    padding: '0 18px 16px 42px',
    borderTop: '1px solid #f1f5f9',
  },
  description: {
    fontSize: 13,
    color: '#475569',
    lineHeight: 1.5,
    marginTop: 12,
    marginBottom: 10,
  },
  meta: {
    display: 'flex',
    flexWrap: 'wrap',
    gap: 16,
  },
  metaItem: {
    fontSize: 12,
    color: '#94a3b8',
  },
};

export default TaskCard;
