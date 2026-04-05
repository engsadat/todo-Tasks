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

---
---

# Feature: Authentication & Login System

## Context
Adding user authentication to the to-do app using Supabase Auth. Each user will have their own tasks. This introduces login, registration, session management, and Row Level Security.

## Workflow Handoff

| Phase | Who | Deliverable | Status |
|-------|-----|-------------|--------|
| 1. Plan | Claude | Auth plan (this section) | DONE |
| 2. Design | Antigravity | Login & Register page mockups | TODO |
| 3. Code | GLM | Updated source files | TODO |
| 4. Review | Claude | Code review, commit, push | TODO |

---

## What Changes

### Overview

| Area | Before | After |
|------|--------|-------|
| Users | None — anyone can see all tasks | Each user has an account, sees only their tasks |
| Pages | 2 (task list, dashboard) | 4 (+ login, register) |
| Routes | 5 | 9 (+ login, register, logout, auth check) |
| Database | `tasks` table only | `tasks` + Supabase `auth.users` + `user_id` column |
| Security | None | JWT sessions + Row Level Security (RLS) |

---

## Database Changes

### 1. Add `user_id` Column to `tasks` Table

```sql
-- Add user_id column linking tasks to auth.users
ALTER TABLE tasks
  ADD COLUMN user_id UUID REFERENCES auth.users(id);
```

### 2. Enable Row Level Security (RLS)

```sql
-- Enable RLS on tasks table
ALTER TABLE tasks ENABLE ROW LEVEL SECURITY;

-- Policy: Users can only SELECT their own tasks
CREATE POLICY "Users can view own tasks"
  ON tasks FOR SELECT
  USING (auth.uid() = user_id);

-- Policy: Users can only INSERT tasks with their own user_id
CREATE POLICY "Users can insert own tasks"
  ON tasks FOR INSERT
  WITH CHECK (auth.uid() = user_id);

-- Policy: Users can only UPDATE their own tasks
CREATE POLICY "Users can update own tasks"
  ON tasks FOR UPDATE
  USING (auth.uid() = user_id);

-- Policy: Users can only DELETE their own tasks
CREATE POLICY "Users can delete own tasks"
  ON tasks FOR DELETE
  USING (auth.uid() = user_id);
```

### 3. Updated ER Diagram

```
auth.users (Supabase built-in)        tasks (existing + modified)
+------------------+                  +------------------+
| id (UUID) PK     |----<one-to-many>-| id (BIGINT) PK   |
| email            |                  | title (TEXT)      |
| encrypted_pass   |                  | done (BOOLEAN)    |
| created_at       |                  | created_at        |
+------------------+                  | user_id (UUID) FK |
                                      +------------------+
```

---

## New Pages & Routes

### Updated Route Table

| Method | Route | Auth Required | Action |
|--------|-------|---------------|--------|
| GET | `/login` | No | Show login form |
| POST | `/login` | No | Authenticate user, create session |
| GET | `/register` | No | Show registration form |
| POST | `/register` | No | Create new user account |
| POST | `/logout` | Yes | Clear session, redirect to login |
| GET | `/` | Yes | Show user's task list |
| GET | `/dashboard` | Yes | Show user's stats |
| POST | `/add` | Yes | Insert task with user_id |
| POST | `/toggle/<id>` | Yes | Toggle task (own tasks only) |
| POST | `/delete/<id>` | Yes | Delete task (own tasks only) |

### Page 3: Login (login.html)

```
+------------------------------------------+
|                                          |
|              To-Do App                   |
|                                          |
|  +------------------------------------+  |
|  |                                    |  |
|  |  Log In                            |  |
|  |                                    |  |
|  |  Email                             |  |
|  |  [____________________________]    |  |
|  |                                    |  |
|  |  Password                          |  |
|  |  [____________________________]    |  |
|  |                                    |  |
|  |  [        Log In             ]     |  |
|  |                                    |  |
|  |  Don't have an account? Register   |  |
|  |                                    |  |
|  +------------------------------------+  |
|                                          |
|         Powered by Supabase              |
+------------------------------------------+
```

### Page 4: Register (register.html)

```
+------------------------------------------+
|                                          |
|              To-Do App                   |
|                                          |
|  +------------------------------------+  |
|  |                                    |  |
|  |  Create Account                    |  |
|  |                                    |  |
|  |  Email                             |  |
|  |  [____________________________]    |  |
|  |                                    |  |
|  |  Password                          |  |
|  |  [____________________________]    |  |
|  |                                    |  |
|  |  Confirm Password                  |  |
|  |  [____________________________]    |  |
|  |                                    |  |
|  |  [       Create Account      ]     |  |
|  |                                    |  |
|  |  Already have an account? Log in   |  |
|  |                                    |  |
|  +------------------------------------+  |
|                                          |
|         Powered by Supabase              |
+------------------------------------------+
```

### Updated Nav Bar (when logged in)

```
+------------------------------------------+
|  [Tasks]  [Dashboard]    user@email [Logout] |
+------------------------------------------+
```

---

## Supabase Auth — How It Works

### Authentication Flow

```
1. REGISTER
   Browser -> POST /register -> Flask -> Supabase Auth API (POST /auth/v1/signup)
   Supabase creates user in auth.users -> returns access_token + refresh_token
   Flask stores tokens in session -> redirect to /

2. LOGIN
   Browser -> POST /login -> Flask -> Supabase Auth API (POST /auth/v1/token?grant_type=password)
   Supabase verifies credentials -> returns access_token + refresh_token
   Flask stores tokens in session -> redirect to /

3. AUTHENTICATED REQUESTS
   Flask reads access_token from session
   Uses it in Authorization header: "Bearer {access_token}"
   Supabase RLS automatically filters tasks by user_id

4. LOGOUT
   Flask clears session -> redirect to /login
```

### Supabase Auth API Endpoints

| Action | Method | URL | Body |
|--------|--------|-----|------|
| Sign up | POST | `/auth/v1/signup` | `{"email": "...", "password": "..."}` |
| Sign in | POST | `/auth/v1/token?grant_type=password` | `{"email": "...", "password": "..."}` |
| Get user | GET | `/auth/v1/user` | — (use access_token in header) |
| Sign out | POST | `/auth/v1/logout` | — (use access_token in header) |

### Headers for Auth Requests

```python
# For auth endpoints (signup, login)
AUTH_HEADERS = {
    "apikey": SUPABASE_KEY,
    "Content-Type": "application/json"
}

# For data requests (tasks) — use user's access token
def get_user_headers(access_token):
    return {
        "apikey": SUPABASE_KEY,
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json",
        "Prefer": "return=representation"
    }
```

---

## Code Specs (for GLM Phase)

### Updated File Structure

```
ToDoTasks Rebuild Project/
  app.py                 <- Updated: add auth routes + session management
  templates/
    base.html            <- Updated: show user email + logout in nav
    index.html           <- No changes
    dashboard.html       <- No changes
    login.html           <- NEW: login form
    register.html        <- NEW: registration form
  static/
    style.css            <- Updated: add auth form styles
  .env                   <- Updated: add FLASK_SECRET_KEY
  requirements.txt       <- No changes (httpx handles auth API calls)
```

### app.py Changes (~130 lines total)

```
NEW imports: functools (wraps), flask (session)

NEW setup:
  - app.secret_key = os.getenv("FLASK_SECRET_KEY")
  - AUTH_URL = f"{SUPABASE_URL}/auth/v1"

NEW helper — login_required decorator:
  - Check if 'access_token' in session
  - If not, redirect to /login
  - If yes, allow route to proceed

NEW helper — get_user_headers(access_token):
  - Return headers dict with user's access_token (not the service key)

UPDATED helper — get_tasks():
  - Accept access_token parameter
  - Use get_user_headers(access_token) instead of HEADERS

NEW route — GET /login:
  - If already logged in, redirect to /
  - Render login.html

NEW route — POST /login:
  - Get email/password from form
  - POST to Supabase /auth/v1/token?grant_type=password
  - If success: store access_token, refresh_token, user email in session -> redirect /
  - If fail: render login.html with error message

NEW route — GET /register:
  - If already logged in, redirect to /
  - Render register.html

NEW route — POST /register:
  - Get email/password/confirm from form
  - Check passwords match
  - POST to Supabase /auth/v1/signup
  - If success: store tokens in session -> redirect /
  - If fail: render register.html with error message

NEW route — POST /logout:
  - Clear session
  - Redirect to /login

UPDATED route — GET /:
  - Add @login_required decorator
  - Pass session access_token to get_tasks()

UPDATED route — GET /dashboard:
  - Add @login_required decorator
  - Pass session access_token to get_tasks()

UPDATED route — POST /add:
  - Add @login_required decorator
  - Use get_user_headers(session['access_token'])

UPDATED route — POST /toggle/<id>:
  - Add @login_required decorator
  - Use get_user_headers(session['access_token'])

UPDATED route — POST /delete/<id>:
  - Add @login_required decorator
  - Use get_user_headers(session['access_token'])
```

### templates/login.html

```
{% extends "base.html" %}
{% block content %}
  Centered card:
    H1: Log In
    Error message (if any): {{ error }}
    Form (POST /login):
      - Email input (type="email", required)
      - Password input (type="password", required)
      - Submit button: "Log In"
    Link: "Don't have an account? <a href="/register">Register</a>"
{% endblock %}
```

### templates/register.html

```
{% extends "base.html" %}
{% block content %}
  Centered card:
    H1: Create Account
    Error message (if any): {{ error }}
    Form (POST /register):
      - Email input (type="email", required)
      - Password input (type="password", required, minlength=6)
      - Confirm Password input (type="password", required)
      - Submit button: "Create Account"
    Link: "Already have an account? <a href="/login">Log in</a>"
{% endblock %}
```

### templates/base.html Changes

```
Updated nav:
  - If user is logged in (session has email):
      [Tasks]  [Dashboard]           user@email  [Logout]
  - If not logged in:
      (no nav links — login/register pages handle their own navigation)
```

### static/style.css Additions

```
NEW styles:
  - .auth-container: centered card for login/register forms (max-width 400px)
  - .auth-container h1: form title
  - .form-group: label + input wrapper (margin-bottom)
  - .form-group label: display block, font-weight 600
  - .form-group input: full width, same style as existing text input
  - input[type="email"], input[type="password"]: inherit text input styles
  - .error-message: red text, margin-bottom
  - .auth-link: centered text with link to login/register
  - .user-info: nav right-side, shows email + logout button
```

### .env Addition

```
FLASK_SECRET_KEY=a-random-secret-string-for-sessions
```

---

## Supabase Setup Steps (Manual — Before Coding)

These steps must be done in the Supabase Dashboard before GLM codes:

### Step 1: Enable Email Auth
1. Go to Supabase Dashboard → Authentication → Providers
2. Ensure "Email" provider is enabled
3. Optional: Disable "Confirm email" for easier testing (Authentication → Settings → toggle off "Enable email confirmations")

### Step 2: Add `user_id` Column
1. Go to Table Editor → `tasks` table
2. Add column: `user_id`, type UUID, nullable (for now — existing tasks have no user)
3. Add foreign key: references `auth.users(id)`

### Step 3: Enable RLS
1. Go to Table Editor → `tasks` → RLS tab
2. Enable RLS
3. Add 4 policies (SELECT, INSERT, UPDATE, DELETE) as defined in the SQL above

### Step 4: Clean Up Existing Tasks
Option A: Delete all existing tasks (they have no user_id)
Option B: Keep them — they'll be invisible due to RLS (no user_id = no match)

---

## Verification

### Test Checklist

- [ ] Login page loads at `/login`
- [ ] Register page loads at `/register`
- [ ] Can create a new account
- [ ] After register, redirected to task list
- [ ] Can log out
- [ ] After logout, redirected to login
- [ ] Can log in with existing account
- [ ] Task list shows only logged-in user's tasks
- [ ] Can add a task (assigned to logged-in user)
- [ ] Can toggle/delete own tasks
- [ ] Dashboard shows only logged-in user's stats
- [ ] Visiting `/` without login redirects to `/login`
- [ ] Two different users see different task lists
- [ ] Nav shows user email and logout button
- [ ] Error messages show for wrong password / existing email

### Security Checklist

- [ ] Passwords never stored in Flask (Supabase handles hashing)
- [ ] Access tokens stored in server-side session (not cookies)
- [ ] RLS prevents cross-user data access
- [ ] `.env` contains FLASK_SECRET_KEY
- [ ] No hardcoded secrets in code
