# Plan: Rebuild To-Do App (Multi-Model Workflow)

## Context
Rebuilding the to-do app from scratch using the multi-model workflow: Claude plans, Antigravity designs, GLM codes. Reusing the existing Supabase project (duthigzpybplibavuvvs.supabase.co).

## Workflow Handoff

| Phase | Who | Deliverable |
|-------|-----|-------------|
| 1. Plan | Claude (this session) | This plan document |
| 2. Design | Antigravity project | UI mockups, page layouts, dashboard specs |
| 3. Code | GLM | All source files based on plan + design |
| 4. Review | Claude | Code review, commit, push |

---

## Architecture

### Tech Stack
- **Backend:** Python Flask
- **Database:** Supabase PostgreSQL (existing project)
- **HTTP Client:** httpx (calls Supabase REST API)
- **Config:** python-dotenv (.env file)
- **Frontend:** HTML/CSS/JS (Jinja2 templates — separate from Python)

### File Structure
```
ToDoTasks Rebuild Project/
  app.py              <- Flask app, routes, Supabase client
  templates/
    base.html         <- shared layout (head, nav, footer)
    index.html        <- task list page
    dashboard.html    <- stats/overview page
  static/
    style.css         <- all styles in one file
  .env                <- Supabase credentials
  .gitignore
  requirements.txt
```

---

## Database

### Reuse Existing Supabase Project
- URL: `https://duthigzpybplibavuvvs.supabase.co`
- Existing `tasks` table schema:

```sql
tasks (
  id          BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
  title       TEXT NOT NULL,
  done        BOOLEAN DEFAULT FALSE,
  created_at  TIMESTAMPTZ DEFAULT NOW()
)
```

---

## Pages & Routes

### Page 1: Task List (index.html)
**Route:** `GET /`
- Shows all tasks ordered by id
- Add task form at top
- Each task: checkbox (toggle) + title + delete button
- Counter: "X/Y completed"

### Page 2: Dashboard (dashboard.html)
**Route:** `GET /dashboard`
- Total tasks count
- Completed vs pending breakdown
- Recently added tasks (last 5)
- Quick stats cards layout

### API Routes
- `POST /add` -> insert task, redirect to /
- `POST /toggle/<id>` -> flip done, redirect to /
- `POST /delete/<id>` -> remove task, redirect to /

---

## Design Specs (for Antigravity Phase)

### Task List Page Layout
```
+------------------------------------------+
|  [Tasks]  [Dashboard]          <- nav bar |
+------------------------------------------+
|                                          |
|  To-Do List                              |
|  3/5 completed                           |
|                                          |
|  [_________________________] [+ Add]     |
|                                          |
|  [ ] Buy groceries                   [x] |
|  [v] Learn Flask                     [x] |
|  [ ] Setup Supabase                  [x] |
|  [v] Write guide                     [x] |
|  [ ] Deploy app                      [x] |
|                                          |
|         Powered by Supabase              |
+------------------------------------------+
```

### Dashboard Page Layout
```
+------------------------------------------+
|  [Tasks]  [Dashboard]          <- nav bar |
+------------------------------------------+
|                                          |
|  Dashboard                               |
|                                          |
|  +----------+  +----------+  +--------+  |
|  | Total    |  | Done     |  | Pending|  |
|  |    5     |  |    3     |  |    2   |  |
|  +----------+  +----------+  +--------+  |
|                                          |
|  Recently Added:                         |
|  - Deploy app         (2 min ago)        |
|  - Write guide        (1 hour ago)       |
|  - Setup Supabase     (3 hours ago)      |
|                                          |
+------------------------------------------+
```

### Design Tokens
- Font: -apple-system, sans-serif
- Primary color: #4a90d9
- Danger/delete: #e74c3c
- Success/done: #27ae60
- Background: #f5f5f5
- Card background: white
- Border radius: 12px
- Max width: 600px, centered

---

## Code Specs (for GLM Phase)

### app.py (~80 lines)
```
Imports: os, flask (Flask, request, redirect, url_for, render_template), dotenv, httpx

Setup:
  - load_dotenv()
  - SUPABASE_URL, SUPABASE_KEY from env
  - REST_URL = f"{SUPABASE_URL}/rest/v1"
  - HEADERS dict with apikey, Authorization, Content-Type, Prefer

Helper:
  - get_tasks() -> GET /tasks?order=id.asc -> return json

Routes:
  - GET /           -> tasks = get_tasks(), render index.html
  - GET /dashboard  -> tasks = get_tasks(), compute stats, render dashboard.html
  - POST /add       -> get title from form, POST to /tasks, redirect /
  - POST /toggle/id -> GET task, flip done, PATCH, redirect /
  - POST /delete/id -> DELETE task, redirect /

Main:
  - app.run(debug=True, port=5000)
```

### templates/base.html
```
Standard HTML5 boilerplate
Link to /static/style.css
Nav bar with links to / and /dashboard
{% block content %}{% endblock %}
Footer: "Powered by Supabase"
```

### templates/index.html
```
{% extends "base.html" %}
{% block content %}
  H1: To-Do List
  Stats: done/total completed
  Add form: text input + submit button
  Task list: loop through tasks
    - checkbox (form POST to /toggle/id, onchange submit)
    - title (strikethrough if done)
    - delete button (form POST to /delete/id)
  Empty state if no tasks
{% endblock %}
```

### templates/dashboard.html
```
{% extends "base.html" %}
{% block content %}
  H1: Dashboard
  3 stat cards in a row: Total, Done, Pending
  Recent tasks list (last 5 by created_at desc)
{% endblock %}
```

### static/style.css (~80 lines)
All styles from design tokens above. Nav, cards, task list, responsive.

### Other files
- `.env` -> SUPABASE_URL and SUPABASE_KEY
- `.gitignore` -> .env, __pycache__/, *.pyc, tasks.json
- `requirements.txt` -> flask, httpx, python-dotenv

---

## Verification

1. `pip install -r requirements.txt`
2. `python app.py`
3. Open http://localhost:5000 -> add tasks, toggle, delete
4. Open http://localhost:5000/dashboard -> verify stats
5. Check Supabase Dashboard Table Editor -> data matches
6. Init git, commit, push to GitHub
