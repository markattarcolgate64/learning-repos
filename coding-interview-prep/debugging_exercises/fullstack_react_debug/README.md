# TaskFlow — Full-Stack Debugging Exercise

A realistic project management app with **6 hidden bugs** across the React
frontend and Express backend. Your job: find each bug, understand why it
causes the observed symptom, and fix it.

## The App

TaskFlow is a project task manager. Users log in, see a dashboard of project
stats, drill into projects to view / search / filter tasks, and create new
tasks. The backend provides a REST API with JWT authentication and an
in-memory data store seeded with sample data.

## Getting Started

```bash
# Install dependencies
cd backend && npm install && cd ..
cd frontend && npm install && cd ..

# Start backend (terminal 1)
cd backend && npm run dev

# Start frontend (terminal 2)
cd frontend && npm run dev
```

Open http://localhost:5173 and log in with:
- **alice** / password123
- **bob** / password456
- **carol** / password789

## Bug Symptoms

You'll notice these problems as you use the app:

1. **Authentication fails immediately** — After logging in successfully, the
   very next API call returns 401 Unauthorized. You can log in but can't
   actually use the app.

2. **First page of tasks is missing** — When viewing a project's tasks, the
   first page seems to skip some items. If you know there should be 25 tasks
   and you're paginating 10 per page, page 1 shows tasks 11-20 instead of
   1-10.

3. **Dashboard shows stale data** — Switch between projects quickly in the
   dashboard dropdown. Sometimes the stats or recent tasks shown belong to
   the previously selected project, not the current one.

4. **Search breaks when navigating between projects** — Search for tasks in
   Project A. Navigate to Project B. Search again — the results are still
   from Project A.

5. **Task card state sticks to wrong items** — Expand a task card to see its
   description, then filter or sort the list. The expanded state "sticks" to
   the position, not the task — a different task may now appear expanded.

6. **Duplicate tasks on slow networks** — Click "Create Task" twice quickly
   (or use network throttling). Two identical tasks appear.

## Rules

- Each bug is a **single, realistic mistake** — the kind you'd make in
  production code.
- Fix each bug with a **minimal change**. Don't rewrite large sections.
- After fixing all 6, the app should work correctly end-to-end.

## Tech Stack

| Layer    | Technology                           |
|----------|--------------------------------------|
| Frontend | React 18, Vite, React Router 6, Axios |
| Backend  | Express 4, jsonwebtoken, uuid        |
| Data     | In-memory arrays (no database)       |
