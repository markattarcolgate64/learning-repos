const express = require('express');
const cors = require('cors');
const jwt = require('jsonwebtoken');
const { v4: uuidv4 } = require('uuid');

const app = express();
const PORT = 3001;
const JWT_SECRET = 'taskflow-secret-key-do-not-expose';
const TOKEN_TTL_SECONDS = 3600;

// ---------------------------------------------------------------------------
// Middleware
// ---------------------------------------------------------------------------
app.use(cors({ origin: 'http://localhost:5173' }));
app.use(express.json());

// ---------------------------------------------------------------------------
// In-memory data
// ---------------------------------------------------------------------------

const users = [
  {
    id: 'user-1',
    username: 'alice',
    password: 'password123',
    name: 'Alice Johnson',
    avatarUrl: 'https://api.dicebear.com/7.x/avataaars/svg?seed=alice',
  },
  {
    id: 'user-2',
    username: 'bob',
    password: 'password456',
    name: 'Bob Martinez',
    avatarUrl: 'https://api.dicebear.com/7.x/avataaars/svg?seed=bob',
  },
  {
    id: 'user-3',
    username: 'carol',
    password: 'password789',
    name: 'Carol Chen',
    avatarUrl: 'https://api.dicebear.com/7.x/avataaars/svg?seed=carol',
  },
];

const projects = [
  {
    id: 'proj-1',
    name: 'Website Redesign',
    description: 'Complete overhaul of the company marketing website with modern design system.',
    ownerId: 'user-1',
    createdAt: '2025-11-01T09:00:00.000Z',
  },
  {
    id: 'proj-2',
    name: 'Mobile App v2',
    description: 'Second major release of the iOS/Android app with offline support.',
    ownerId: 'user-2',
    createdAt: '2025-11-15T14:30:00.000Z',
  },
  {
    id: 'proj-3',
    name: 'API Migration',
    description: 'Migrate legacy REST endpoints to GraphQL while maintaining backward compatibility.',
    ownerId: 'user-1',
    createdAt: '2025-12-01T08:00:00.000Z',
  },
  {
    id: 'proj-4',
    name: 'Q1 Marketing Campaign',
    description: 'Plan and execute the Q1 2026 digital marketing campaign across all channels.',
    ownerId: 'user-3',
    createdAt: '2026-01-05T10:00:00.000Z',
  },
];

const tasks = [
  // ---- Website Redesign (proj-1) — 8 tasks ----
  {
    id: 'task-1',
    projectId: 'proj-1',
    title: 'Create wireframes for homepage',
    description: 'Design low-fidelity wireframes for the new homepage layout.',
    priority: 'high',
    status: 'done',
    assigneeId: 'user-1',
    createdAt: '2025-11-02T10:00:00.000Z',
    updatedAt: '2025-11-10T16:00:00.000Z',
  },
  {
    id: 'task-2',
    projectId: 'proj-1',
    title: 'Design color palette and typography',
    description: 'Establish the new brand color system and type scale.',
    priority: 'high',
    status: 'done',
    assigneeId: 'user-3',
    createdAt: '2025-11-03T09:00:00.000Z',
    updatedAt: '2025-11-12T11:30:00.000Z',
  },
  {
    id: 'task-3',
    projectId: 'proj-1',
    title: 'Build reusable component library',
    description: 'Implement buttons, cards, modals, and form elements in React.',
    priority: 'urgent',
    status: 'in_progress',
    assigneeId: 'user-1',
    createdAt: '2025-11-05T08:00:00.000Z',
    updatedAt: '2025-12-20T14:00:00.000Z',
  },
  {
    id: 'task-4',
    projectId: 'proj-1',
    title: 'Implement responsive navigation',
    description: 'Create a responsive header with mobile hamburger menu.',
    priority: 'medium',
    status: 'in_progress',
    assigneeId: 'user-2',
    createdAt: '2025-11-08T13:00:00.000Z',
    updatedAt: '2026-01-05T09:00:00.000Z',
  },
  {
    id: 'task-5',
    projectId: 'proj-1',
    title: 'Set up CI/CD pipeline for staging',
    description: 'Configure GitHub Actions to deploy preview builds on every PR.',
    priority: 'medium',
    status: 'review',
    assigneeId: 'user-2',
    createdAt: '2025-11-10T10:00:00.000Z',
    updatedAt: '2026-01-08T17:00:00.000Z',
  },
  {
    id: 'task-6',
    projectId: 'proj-1',
    title: 'Write accessibility audit checklist',
    description: 'Document WCAG 2.1 AA requirements for the redesign.',
    priority: 'low',
    status: 'todo',
    assigneeId: 'user-3',
    createdAt: '2025-11-12T09:00:00.000Z',
    updatedAt: '2025-11-12T09:00:00.000Z',
  },
  {
    id: 'task-7',
    projectId: 'proj-1',
    title: 'Migrate blog content to new CMS',
    description: 'Export existing WordPress posts and import into the new headless CMS.',
    priority: 'low',
    status: 'todo',
    assigneeId: 'user-1',
    createdAt: '2025-11-15T11:00:00.000Z',
    updatedAt: '2025-11-15T11:00:00.000Z',
  },
  {
    id: 'task-8',
    projectId: 'proj-1',
    title: 'Performance budget and Lighthouse targets',
    description: 'Define performance budgets for Core Web Vitals.',
    priority: 'medium',
    status: 'todo',
    assigneeId: 'user-2',
    createdAt: '2025-11-18T14:00:00.000Z',
    updatedAt: '2025-11-18T14:00:00.000Z',
  },

  // ---- Mobile App v2 (proj-2) — 8 tasks ----
  {
    id: 'task-9',
    projectId: 'proj-2',
    title: 'Implement offline data sync',
    description: 'Use SQLite for local storage and background sync when connectivity is restored.',
    priority: 'urgent',
    status: 'in_progress',
    assigneeId: 'user-2',
    createdAt: '2025-11-16T09:00:00.000Z',
    updatedAt: '2026-01-20T10:00:00.000Z',
  },
  {
    id: 'task-10',
    projectId: 'proj-2',
    title: 'Push notification service integration',
    description: 'Integrate Firebase Cloud Messaging for iOS and Android.',
    priority: 'high',
    status: 'review',
    assigneeId: 'user-2',
    createdAt: '2025-11-18T10:00:00.000Z',
    updatedAt: '2026-01-15T13:00:00.000Z',
  },
  {
    id: 'task-11',
    projectId: 'proj-2',
    title: 'Redesign onboarding flow',
    description: 'Create a 3-step onboarding wizard for new users.',
    priority: 'medium',
    status: 'done',
    assigneeId: 'user-3',
    createdAt: '2025-11-20T08:00:00.000Z',
    updatedAt: '2025-12-15T16:00:00.000Z',
  },
  {
    id: 'task-12',
    projectId: 'proj-2',
    title: 'Add biometric authentication',
    description: 'Support Face ID and fingerprint login.',
    priority: 'high',
    status: 'in_progress',
    assigneeId: 'user-1',
    createdAt: '2025-12-01T09:00:00.000Z',
    updatedAt: '2026-01-22T11:00:00.000Z',
  },
  {
    id: 'task-13',
    projectId: 'proj-2',
    title: 'Dark mode support',
    description: 'Implement system-aware dark mode with manual toggle.',
    priority: 'medium',
    status: 'todo',
    assigneeId: 'user-3',
    createdAt: '2025-12-05T14:00:00.000Z',
    updatedAt: '2025-12-05T14:00:00.000Z',
  },
  {
    id: 'task-14',
    projectId: 'proj-2',
    title: 'Crash reporting setup',
    description: 'Integrate Sentry for crash and error reporting.',
    priority: 'medium',
    status: 'done',
    assigneeId: 'user-2',
    createdAt: '2025-12-08T10:00:00.000Z',
    updatedAt: '2026-01-02T09:00:00.000Z',
  },
  {
    id: 'task-15',
    projectId: 'proj-2',
    title: 'App Store metadata and screenshots',
    description: 'Prepare screenshots, descriptions, and keywords for both stores.',
    priority: 'low',
    status: 'todo',
    assigneeId: 'user-3',
    createdAt: '2025-12-10T11:00:00.000Z',
    updatedAt: '2025-12-10T11:00:00.000Z',
  },
  {
    id: 'task-16',
    projectId: 'proj-2',
    title: 'Beta testing group recruitment',
    description: 'Recruit 50 beta testers from existing user base via email.',
    priority: 'low',
    status: 'review',
    assigneeId: 'user-1',
    createdAt: '2025-12-12T15:00:00.000Z',
    updatedAt: '2026-01-10T14:00:00.000Z',
  },

  // ---- API Migration (proj-3) — 7 tasks ----
  {
    id: 'task-17',
    projectId: 'proj-3',
    title: 'Audit existing REST endpoints',
    description: 'Document all current endpoints, request/response shapes, and usage metrics.',
    priority: 'high',
    status: 'done',
    assigneeId: 'user-1',
    createdAt: '2025-12-02T08:00:00.000Z',
    updatedAt: '2025-12-20T17:00:00.000Z',
  },
  {
    id: 'task-18',
    projectId: 'proj-3',
    title: 'Define GraphQL schema',
    description: 'Write the SDL for all types, queries, and mutations.',
    priority: 'urgent',
    status: 'in_progress',
    assigneeId: 'user-1',
    createdAt: '2025-12-10T09:00:00.000Z',
    updatedAt: '2026-01-25T10:00:00.000Z',
  },
  {
    id: 'task-19',
    projectId: 'proj-3',
    title: 'Implement resolver layer',
    description: 'Build resolvers that delegate to existing service layer.',
    priority: 'high',
    status: 'todo',
    assigneeId: 'user-2',
    createdAt: '2025-12-15T13:00:00.000Z',
    updatedAt: '2025-12-15T13:00:00.000Z',
  },
  {
    id: 'task-20',
    projectId: 'proj-3',
    title: 'Set up Apollo Server with Express',
    description: 'Mount Apollo Server middleware alongside existing REST routes.',
    priority: 'medium',
    status: 'todo',
    assigneeId: 'user-2',
    createdAt: '2025-12-18T10:00:00.000Z',
    updatedAt: '2025-12-18T10:00:00.000Z',
  },
  {
    id: 'task-21',
    projectId: 'proj-3',
    title: 'Write integration tests for GraphQL',
    description: 'Cover all queries and mutations with automated tests.',
    priority: 'medium',
    status: 'todo',
    assigneeId: 'user-3',
    createdAt: '2025-12-20T09:00:00.000Z',
    updatedAt: '2025-12-20T09:00:00.000Z',
  },
  {
    id: 'task-22',
    projectId: 'proj-3',
    title: 'Deprecation plan for v1 REST API',
    description: 'Draft timeline and communication plan for sunsetting the legacy API.',
    priority: 'low',
    status: 'todo',
    assigneeId: 'user-1',
    createdAt: '2025-12-22T14:00:00.000Z',
    updatedAt: '2025-12-22T14:00:00.000Z',
  },
  {
    id: 'task-23',
    projectId: 'proj-3',
    title: 'Rate limiting and query complexity analysis',
    description: 'Implement query cost analysis to prevent expensive queries.',
    priority: 'high',
    status: 'review',
    assigneeId: 'user-3',
    createdAt: '2025-12-28T08:00:00.000Z',
    updatedAt: '2026-01-18T12:00:00.000Z',
  },

  // ---- Q1 Marketing Campaign (proj-4) — 5 tasks ----
  {
    id: 'task-24',
    projectId: 'proj-4',
    title: 'Define target audience segments',
    description: 'Identify and document three primary audience personas.',
    priority: 'high',
    status: 'done',
    assigneeId: 'user-3',
    createdAt: '2026-01-06T09:00:00.000Z',
    updatedAt: '2026-01-15T11:00:00.000Z',
  },
  {
    id: 'task-25',
    projectId: 'proj-4',
    title: 'Create ad creatives for social media',
    description: 'Design image and video assets for Instagram, LinkedIn, and Twitter.',
    priority: 'urgent',
    status: 'in_progress',
    assigneeId: 'user-3',
    createdAt: '2026-01-10T10:00:00.000Z',
    updatedAt: '2026-02-01T15:00:00.000Z',
  },
  {
    id: 'task-26',
    projectId: 'proj-4',
    title: 'Set up analytics tracking',
    description: 'Configure UTM parameters and conversion tracking in GA4.',
    priority: 'medium',
    status: 'todo',
    assigneeId: 'user-1',
    createdAt: '2026-01-12T08:00:00.000Z',
    updatedAt: '2026-01-12T08:00:00.000Z',
  },
  {
    id: 'task-27',
    projectId: 'proj-4',
    title: 'Draft email nurture sequence',
    description: 'Write 5-email drip campaign for new leads from the campaign.',
    priority: 'medium',
    status: 'in_progress',
    assigneeId: 'user-1',
    createdAt: '2026-01-15T13:00:00.000Z',
    updatedAt: '2026-01-28T10:00:00.000Z',
  },
  {
    id: 'task-28',
    projectId: 'proj-4',
    title: 'Budget allocation spreadsheet',
    description: 'Break down the $50k budget across channels and timeline.',
    priority: 'high',
    status: 'review',
    assigneeId: 'user-2',
    createdAt: '2026-01-08T11:00:00.000Z',
    updatedAt: '2026-01-20T16:00:00.000Z',
  },
];

// Track recent activity for the dashboard
const recentActivity = [];

function recordActivity(action, task) {
  recentActivity.unshift({
    id: uuidv4(),
    action,
    taskId: task.id,
    taskTitle: task.title,
    projectId: task.projectId,
    userId: task.assigneeId,
    timestamp: new Date().toISOString(),
  });
  if (recentActivity.length > 50) {
    recentActivity.length = 50;
  }
}

// ---------------------------------------------------------------------------
// Auth middleware
// ---------------------------------------------------------------------------
function authenticate(req, res, next) {
  const authHeader = req.headers.authorization;
  if (!authHeader?.startsWith('Bearer ')) {
    return res.status(401).json({ error: 'No token provided' });
  }

  try {
    const token = authHeader.split(' ')[1];
    const decoded = jwt.verify(token, JWT_SECRET);

    if (decoded.iat + TOKEN_TTL_SECONDS < Date.now()) {
      return res.status(401).json({ error: 'Token expired' });
    }

    req.user = users.find(u => u.id === decoded.userId);
    if (!req.user) {
      return res.status(401).json({ error: 'User not found' });
    }
    next();
  } catch (err) {
    return res.status(401).json({ error: 'Invalid token' });
  }
}

// ---------------------------------------------------------------------------
// Auth routes
// ---------------------------------------------------------------------------
app.post('/api/auth/login', (req, res) => {
  const { username, password } = req.body;

  if (!username || !password) {
    return res.status(400).json({ error: 'Username and password are required' });
  }

  const user = users.find(u => u.username === username && u.password === password);
  if (!user) {
    return res.status(401).json({ error: 'Invalid credentials' });
  }

  const token = jwt.sign({ userId: user.id }, JWT_SECRET);
  const { password: _, ...safeUser } = user;

  res.json({ token, user: safeUser });
});

app.post('/api/auth/me', authenticate, (req, res) => {
  const { password: _, ...safeUser } = req.user;
  res.json({ user: safeUser });
});

// ---------------------------------------------------------------------------
// Project routes
// ---------------------------------------------------------------------------
app.get('/api/projects', authenticate, (req, res) => {
  const projectsWithCounts = projects.map(project => {
    const projectTasks = tasks.filter(t => t.projectId === project.id);
    return {
      ...project,
      taskCount: projectTasks.length,
      completedTaskCount: projectTasks.filter(t => t.status === 'done').length,
    };
  });

  res.json({ projects: projectsWithCounts });
});

app.get('/api/projects/:id', authenticate, (req, res) => {
  const project = projects.find(p => p.id === req.params.id);
  if (!project) {
    return res.status(404).json({ error: 'Project not found' });
  }

  const projectTasks = tasks.filter(t => t.projectId === project.id);
  res.json({
    ...project,
    taskCount: projectTasks.length,
    completedTaskCount: projectTasks.filter(t => t.status === 'done').length,
  });
});

// ---------------------------------------------------------------------------
// Task routes
// ---------------------------------------------------------------------------
app.get('/api/projects/:id/tasks', authenticate, (req, res) => {
  const { id } = req.params;
  const {
    page = 1,
    limit = 10,
    status,
    priority,
    search,
    sortBy = 'createdAt',
    sortOrder = 'desc',
  } = req.query;

  const project = projects.find(p => p.id === id);
  if (!project) {
    return res.status(404).json({ error: 'Project not found' });
  }

  let filtered = tasks.filter(t => t.projectId === id);

  // Apply filters
  if (status) {
    filtered = filtered.filter(t => t.status === status);
  }
  if (priority) {
    filtered = filtered.filter(t => t.priority === priority);
  }
  if (search) {
    const term = search.toLowerCase();
    filtered = filtered.filter(
      t =>
        t.title.toLowerCase().includes(term) ||
        t.description.toLowerCase().includes(term)
    );
  }

  // Sort
  const validSortFields = ['createdAt', 'updatedAt', 'priority', 'title', 'status'];
  const field = validSortFields.includes(sortBy) ? sortBy : 'createdAt';
  const order = sortOrder === 'asc' ? 1 : -1;

  const priorityOrder = { urgent: 0, high: 1, medium: 2, low: 3 };
  const statusOrder = { todo: 0, in_progress: 1, review: 2, done: 3 };

  filtered.sort((a, b) => {
    let comparison = 0;
    if (field === 'priority') {
      comparison = priorityOrder[a.priority] - priorityOrder[b.priority];
    } else if (field === 'status') {
      comparison = statusOrder[a.status] - statusOrder[b.status];
    } else {
      comparison = a[field] < b[field] ? -1 : a[field] > b[field] ? 1 : 0;
    }
    return comparison * order;
  });

  // Paginate
  const totalItems = filtered.length;
  const totalPages = Math.ceil(totalItems / parseInt(limit));
  const offset = parseInt(page) * parseInt(limit);
  const paginated = filtered.slice(offset, offset + parseInt(limit));

  // Attach assignee info
  const tasksWithAssignees = paginated.map(task => {
    const assignee = users.find(u => u.id === task.assigneeId);
    return {
      ...task,
      assignee: assignee
        ? { id: assignee.id, name: assignee.name, avatarUrl: assignee.avatarUrl }
        : null,
    };
  });

  res.json({
    tasks: tasksWithAssignees,
    pagination: {
      page: parseInt(page),
      limit: parseInt(limit),
      totalItems,
      totalPages,
    },
  });
});

app.post('/api/projects/:id/tasks', authenticate, (req, res) => {
  const { id } = req.params;
  const { title, description, priority, assigneeId } = req.body;

  const project = projects.find(p => p.id === id);
  if (!project) {
    return res.status(404).json({ error: 'Project not found' });
  }

  if (!title || !title.trim()) {
    return res.status(400).json({ error: 'Task title is required' });
  }

  const validPriorities = ['low', 'medium', 'high', 'urgent'];
  if (priority && !validPriorities.includes(priority)) {
    return res.status(400).json({ error: 'Invalid priority value' });
  }

  if (assigneeId && !users.find(u => u.id === assigneeId)) {
    return res.status(400).json({ error: 'Assignee not found' });
  }

  const now = new Date().toISOString();
  const newTask = {
    id: `task-${uuidv4().slice(0, 8)}`,
    projectId: id,
    title: title.trim(),
    description: description?.trim() || '',
    priority: priority || 'medium',
    status: 'todo',
    assigneeId: assigneeId || req.user.id,
    createdAt: now,
    updatedAt: now,
  };

  // Simulate realistic server processing time
  setTimeout(() => {
    tasks.push(newTask);
    recordActivity('created', newTask);

    const assignee = users.find(u => u.id === newTask.assigneeId);
    res.status(201).json({
      ...newTask,
      assignee: assignee
        ? { id: assignee.id, name: assignee.name, avatarUrl: assignee.avatarUrl }
        : null,
    });
  }, 800);
});

app.patch('/api/tasks/:id', authenticate, (req, res) => {
  const taskIndex = tasks.findIndex(t => t.id === req.params.id);
  if (taskIndex === -1) {
    return res.status(404).json({ error: 'Task not found' });
  }

  const allowedFields = ['title', 'description', 'priority', 'status', 'assigneeId'];
  const updates = {};

  for (const field of allowedFields) {
    if (req.body[field] !== undefined) {
      updates[field] = req.body[field];
    }
  }

  if (updates.priority) {
    const validPriorities = ['low', 'medium', 'high', 'urgent'];
    if (!validPriorities.includes(updates.priority)) {
      return res.status(400).json({ error: 'Invalid priority value' });
    }
  }

  if (updates.status) {
    const validStatuses = ['todo', 'in_progress', 'review', 'done'];
    if (!validStatuses.includes(updates.status)) {
      return res.status(400).json({ error: 'Invalid status value' });
    }
  }

  if (updates.assigneeId && !users.find(u => u.id === updates.assigneeId)) {
    return res.status(400).json({ error: 'Assignee not found' });
  }

  tasks[taskIndex] = {
    ...tasks[taskIndex],
    ...updates,
    updatedAt: new Date().toISOString(),
  };

  recordActivity('updated', tasks[taskIndex]);

  const assignee = users.find(u => u.id === tasks[taskIndex].assigneeId);
  res.json({
    ...tasks[taskIndex],
    assignee: assignee
      ? { id: assignee.id, name: assignee.name, avatarUrl: assignee.avatarUrl }
      : null,
  });
});

app.delete('/api/tasks/:id', authenticate, (req, res) => {
  const taskIndex = tasks.findIndex(t => t.id === req.params.id);
  if (taskIndex === -1) {
    return res.status(404).json({ error: 'Task not found' });
  }

  const [removed] = tasks.splice(taskIndex, 1);
  recordActivity('deleted', removed);

  res.json({ message: 'Task deleted', task: removed });
});

// ---------------------------------------------------------------------------
// Dashboard routes
// ---------------------------------------------------------------------------
app.get('/api/dashboard/stats', authenticate, (req, res) => {
  const tasksByStatus = {
    todo: tasks.filter(t => t.status === 'todo').length,
    in_progress: tasks.filter(t => t.status === 'in_progress').length,
    review: tasks.filter(t => t.status === 'review').length,
    done: tasks.filter(t => t.status === 'done').length,
  };

  const tasksByPriority = {
    low: tasks.filter(t => t.priority === 'low').length,
    medium: tasks.filter(t => t.priority === 'medium').length,
    high: tasks.filter(t => t.priority === 'high').length,
    urgent: tasks.filter(t => t.priority === 'urgent').length,
  };

  res.json({
    totalProjects: projects.length,
    totalTasks: tasks.length,
    tasksByStatus,
    tasksByPriority,
    recentActivity: recentActivity.slice(0, 10),
  });
});

// ---------------------------------------------------------------------------
// Error handling
// ---------------------------------------------------------------------------
app.use((err, req, res, next) => {
  console.error('Unhandled error:', err);
  res.status(500).json({ error: 'Internal server error' });
});

app.use((req, res) => {
  res.status(404).json({ error: 'Endpoint not found' });
});

// ---------------------------------------------------------------------------
// Start
// ---------------------------------------------------------------------------
app.listen(PORT, () => {
  console.log(`TaskFlow API running on http://localhost:${PORT}`);
});
