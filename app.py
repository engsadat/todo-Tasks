import os
from datetime import datetime, timezone
from functools import wraps
from flask import Flask, request, redirect, url_for, render_template, session
from dotenv import load_dotenv
import httpx

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv("FLASK_SECRET_KEY")
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
REST_URL = f"{SUPABASE_URL}/rest/v1"
AUTH_URL = f"{SUPABASE_URL}/auth/v1"
AUTH_HEADERS = {
    "apikey": SUPABASE_KEY,
    "Content-Type": "application/json"
}

def get_user_headers(access_token):
    return {
        "apikey": SUPABASE_KEY,
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json",
        "Prefer": "return=representation"
    }

def get_tasks(access_token):
    res = httpx.get(f"{REST_URL}/tasks", params={"order": "id.asc"}, headers=get_user_headers(access_token))
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

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'access_token' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

@app.route('/login', methods=['GET', 'POST'])
def login():
    if 'access_token' in session:
        return redirect(url_for('index'))
    error = None
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        res = httpx.post(f"{AUTH_URL}/token?grant_type=password", json={"email": email, "password": password}, headers=AUTH_HEADERS)
        if res.status_code == 200:
            data = res.json()
            session['access_token'] = data.get('access_token')
            session['refresh_token'] = data.get('refresh_token')
            session['email'] = data.get('user', {}).get('email')
            return redirect(url_for('index'))
        else:
            error = res.json().get('error_description', 'Invalid login credentials')
    return render_template('login.html', error=error)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if 'access_token' in session:
        return redirect(url_for('index'))
    error = None
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        confirm = request.form.get('confirm')
        if password != confirm:
            return render_template('register.html', error="Passwords do not match")
        res = httpx.post(f"{AUTH_URL}/signup", json={"email": email, "password": password}, headers=AUTH_HEADERS)
        if res.status_code in [200, 201]:
            data = res.json()
            if data.get('access_token'):
                session['access_token'] = data.get('access_token')
                session['refresh_token'] = data.get('refresh_token')
                session['email'] = data.get('user', {}).get('email')
                return redirect(url_for('index'))
            else:
                return redirect(url_for('login'))
        else:
            error = res.json().get('msg', 'Registration failed')
    return render_template('register.html', error=error)

@app.route('/logout', methods=['POST'])
def logout():
    session.clear()
    return redirect(url_for('login'))

@app.route("/")
@login_required
def index():
    tasks = get_tasks(session['access_token'])
    completed_count = sum(1 for t in tasks if t.get("done"))
    total_count = len(tasks)
    return render_template("index.html", tasks=tasks, completed_count=completed_count, total_count=total_count)

@app.route("/dashboard")
@login_required
def dashboard():
    tasks = get_tasks(session['access_token'])
    total_count = len(tasks)
    completed_count = sum(1 for t in tasks if t.get("done"))
    pending_count = total_count - completed_count

    res = httpx.get(f"{REST_URL}/tasks", params={"order": "created_at.desc", "limit": 5}, headers=get_user_headers(session['access_token']))
    recent_tasks = res.json()

    for task in recent_tasks:
        task["time_ago"] = time_ago(task.get("created_at"))

    return render_template("dashboard.html",
                           total_count=total_count,
                           completed_count=completed_count,
                           pending_count=pending_count,
                           recent_tasks=recent_tasks)

@app.route("/add", methods=["POST"])
@login_required
def add_task():
    title = request.form.get("title")
    httpx.post(f"{REST_URL}/tasks", json={"title": title}, headers=get_user_headers(session['access_token']))
    return redirect(url_for("index"))

@app.route("/toggle/<int:id>", methods=["POST"])
@login_required
def toggle_task(id):
    headers = get_user_headers(session['access_token'])
    res = httpx.get(f"{REST_URL}/tasks", params={"id": f"eq.{id}"}, headers=headers)
    task = res.json()[0]
    new_value = not task.get("done")

    httpx.patch(f"{REST_URL}/tasks", params={"id": f"eq.{id}"}, json={"done": new_value}, headers=headers)
    return redirect(url_for("index"))

@app.route("/delete/<int:id>", methods=["POST"])
@login_required
def delete_task(id):
    httpx.delete(f"{REST_URL}/tasks", params={"id": f"eq.{id}"}, headers=get_user_headers(session['access_token']))
    return redirect(url_for("index"))

if __name__ == "__main__":
    app.run(debug=True, port=5000)
