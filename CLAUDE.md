# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

A to-do task app built with Python Flask and Supabase PostgreSQL. The app uses Supabase's REST API via httpx (not the Supabase Python SDK). Frontend is server-rendered with Jinja2 templates.

## Tech Stack

- **Backend:** Python Flask
- **Database:** Supabase PostgreSQL (project: `duthigzpybplibavuvvs.supabase.co`)
- **HTTP Client:** httpx (calls Supabase REST API directly)
- **Config:** python-dotenv (`.env` file with `SUPABASE_URL` and `SUPABASE_KEY`)
- **Frontend:** Jinja2 templates + static CSS

## Build & Run Commands

```bash
pip install -r requirements.txt
python app.py                    # runs on http://localhost:5000
```

## Architecture

The app follows a simple Flask pattern — all routes in `app.py` (~80 lines), Jinja2 templates extending `base.html`, single CSS file.

**Supabase REST pattern:** All database calls go through `{SUPABASE_URL}/rest/v1` with headers containing `apikey`, `Authorization`, `Content-Type`, and `Prefer`. No ORM or SDK — raw HTTP via httpx.

**Routes:**
- `GET /` — task list page (index.html)
- `GET /dashboard` — stats/overview page (dashboard.html)
- `POST /add` — insert task, redirect to /
- `POST /toggle/<id>` — flip `done` boolean, redirect to /
- `POST /delete/<id>` — remove task, redirect to /

**Database table:** Single `tasks` table with columns: `id` (bigint identity), `title` (text), `done` (boolean, default false), `created_at` (timestamptz, default now()).

## Multi-Model Workflow

This project uses a handoff workflow documented in `PLAN.md`: Claude plans, Antigravity designs UI, GLM codes, Claude reviews. Refer to `PLAN.md` for detailed specs including page layouts, design tokens, and code specs.
