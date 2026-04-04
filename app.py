import os
from datetime import datetime, timezone
from flask import Flask, request, redirect, url_for, render_template
from dotenv import load_dotenv
import httpx

load_dotenv()

app = Flask(__name__)
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
REST_URL = f"{SUPABASE_URL}/rest/v1"
HEADERS = {
    "apikey": SUPABASE_KEY,
    "Authorization": f"Bearer {SUPABASE_KEY}",
    "Content-Type": "application/json",
    "Prefer": "return=representation"
}

def get_tasks():
    res = httpx.get(f"{REST_URL}/tasks", params={"order": "id.asc"}, headers=HEADERS)
    return res.json()

def time_ago(date_string):
    if not date_string:
        return ""

    dt = datetime.fromisoformat(date_string.replace('Z', '+00:00'))

    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)

    now = datetime.now(timezone.utc)
    diff = now - dt

    seconds = diff.total_seconds()

    if seconds < 60:
        return "just now"
    minutes = int(seconds / 60)
    if minutes < 60:
        return f"{minutes} min ago"
    hours = int(minutes / 60)
    if hours < 24:
        return f"{hours} hours ago"
    days = int(hours / 24)
    return f"{days} days ago"

@app.route("/")
def index():
    tasks = get_tasks()
    completed_count = sum(1 for t in tasks if t.get("done"))
    total_count = len(tasks)
    return render_template("index.html", tasks=tasks, completed_count=completed_count, total_count=total_count)

@app.route("/dashboard")
def dashboard():
    tasks = get_tasks()
    total_count = len(tasks)
    completed_count = sum(1 for t in tasks if t.get("done"))
    pending_count = total_count - completed_count

    res = httpx.get(f"{REST_URL}/tasks", params={"order": "created_at.desc", "limit": 5}, headers=HEADERS)
    recent_tasks = res.json()

    for task in recent_tasks:
        task["time_ago"] = time_ago(task.get("created_at"))

    return render_template("dashboard.html",
                           total_count=total_count,
                           completed_count=completed_count,
                           pending_count=pending_count,
                           recent_tasks=recent_tasks)

@app.route("/add", methods=["POST"])
def add_task():
    title = request.form.get("title")
    httpx.post(f"{REST_URL}/tasks", json={"title": title}, headers=HEADERS)
    return redirect(url_for("index"))

@app.route("/toggle/<int:id>", methods=["POST"])
def toggle_task(id):
    res = httpx.get(f"{REST_URL}/tasks", params={"id": f"eq.{id}"}, headers=HEADERS)
    task = res.json()[0]
    new_value = not task.get("done")

    httpx.patch(f"{REST_URL}/tasks", params={"id": f"eq.{id}"}, json={"done": new_value}, headers=HEADERS)
    return redirect(url_for("index"))

@app.route("/delete/<int:id>", methods=["POST"])
def delete_task(id):
    httpx.delete(f"{REST_URL}/tasks", params={"id": f"eq.{id}"}, headers=HEADERS)
    return redirect(url_for("index"))

if __name__ == "__main__":
    app.run(debug=True, port=5000)
