# TaskFlow — Solution Guide

## Bug 1: Authentication Fails Immediately
**File:** `backend/server.js` (auth middleware)
**Root cause:** Unit mismatch in token expiry check

The auth middleware compares `decoded.iat + TOKEN_TTL_SECONDS` against
`Date.now()`. JWT's `iat` (issued-at) is in **seconds** since epoch, and
`TOKEN_TTL_SECONDS` is also in seconds. But `Date.now()` returns
**milliseconds**. The sum `iat + 3600` is approximately 1,700,003,600, while
`Date.now()` is approximately 1,700,000,000,000. The token always appears
expired.

**Fix:**
```javascript
// Before (buggy):
if (decoded.iat + TOKEN_TTL_SECONDS < Date.now()) {

// After (fixed):
if (decoded.iat + TOKEN_TTL_SECONDS < Math.floor(Date.now() / 1000)) {
```

---

## Bug 2: First Page of Tasks Missing
**File:** `backend/server.js` (GET /api/projects/:id/tasks)
**Root cause:** Off-by-one in pagination offset

The offset is calculated as `page * limit` instead of `(page - 1) * limit`.
When the client requests page 1, the offset is `1 * 10 = 10`, skipping the
first 10 items. Page 1 effectively shows what should be page 2.

**Fix:**
```javascript
// Before (buggy):
const offset = parseInt(page) * parseInt(limit);

// After (fixed):
const offset = (parseInt(page) - 1) * parseInt(limit);
```

---

## Bug 3: Dashboard Shows Stale Data
**File:** `frontend/src/pages/DashboardPage.jsx`
**Root cause:** Missing request cancellation in useEffect

When `selectedProject` changes, the effect fires two API calls (stats +
tasks). If the user switches projects quickly, a slow response from the old
project can arrive after the fast response from the new project, overwriting
correct data with stale data. The useEffect has no cleanup function and no
AbortController.

**Fix:**
```jsx
useEffect(() => {
  if (!selectedProject) return;
  const controller = new AbortController();
  setLoading(true);

  Promise.all([
    api.get(`/api/projects/${selectedProject}/tasks?limit=5`,
      { signal: controller.signal }),
    api.get(`/api/dashboard/stats?projectId=${selectedProject}`,
      { signal: controller.signal })
  ]).then(([tasksRes, statsRes]) => {
    setRecentTasks(tasksRes.data.tasks);
    setStats(statsRes.data);
    setLoading(false);
  }).catch(err => {
    if (!controller.signal.aborted) setLoading(false);
  });

  return () => controller.abort();
}, [selectedProject]);
```

---

## Bug 4: Search Breaks Across Projects
**File:** `frontend/src/pages/ProjectPage.jsx`
**Root cause:** Stale closure in useCallback with empty dependency array

The debounced search handler is wrapped in `useCallback(..., [])` with an
empty dependency array. It captures `projectId` from the closure at creation
time. When the user navigates to a different project, `projectId` changes
but the callback is never recreated — it still queries the original project.

**Fix:**
```jsx
// Before (buggy):
const debouncedSearch = useCallback(
  debounce((query) => {
    api.get(`/api/projects/${projectId}/tasks`, { params: { search: query } })
      .then(res => setTasks(res.data.tasks));
  }, 300),
  []
);

// After (fixed) — include projectId in deps:
const debouncedSearch = useCallback(
  debounce((query) => {
    api.get(`/api/projects/${projectId}/tasks`, { params: { search: query } })
      .then(res => setTasks(res.data.tasks));
  }, 300),
  [projectId]
);
```

---

## Bug 5: Task Card State Sticks to Wrong Items
**File:** `frontend/src/pages/ProjectPage.jsx`
**Root cause:** Array index used as React key on filtered/sorted list

The task list uses `key={index}` instead of `key={task.id}`. When the list
is filtered or re-sorted, React matches components by position (index) not
identity. A TaskCard's local state (like "expanded") stays at index 0 even
when the task at index 0 changes after filtering.

**Fix:**
```jsx
// Before (buggy):
{filteredTasks.map((task, index) => (
  <TaskCard key={index} task={task} ... />
))}

// After (fixed):
{filteredTasks.map((task) => (
  <TaskCard key={task.id} task={task} ... />
))}
```

---

## Bug 6: Duplicate Tasks on Slow Networks
**File:** `frontend/src/components/TaskForm.jsx`
**Root cause:** Missing submission guard despite having state variable

The component declares `const [submitting, setSubmitting] = useState(false)`
and the button text even checks `submitting` to show "Creating..." — but
the `handleSubmit` function never calls `setSubmitting(true)` at the start
or checks `if (submitting) return`. The server has an 800ms response delay,
giving the user time to click multiple times.

**Fix:**
```jsx
const handleSubmit = async (e) => {
  e.preventDefault();
  if (submitting) return;      // add guard
  setSubmitting(true);         // add this
  try {
    const res = await api.post(`/api/projects/${projectId}/tasks`, formData);
    onTaskCreated(res.data);
    onClose();
  } catch (err) {
    setError(err.response?.data?.error || 'Failed to create task');
    setSubmitting(false);      // reset on error only (onClose handles success)
  }
};
```
