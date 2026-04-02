from flask import Flask, render_template, request, redirect, session
from flask_cors import CORS
import requests

app = Flask(__name__)
CORS(app)

API = "http://proxy:8080"


# ---------------------------
#   UTILITAIRE : HEADERS JWT
# ---------------------------
def auth_headers():
    token = session.get("token")
    if not token:
        return {}
    return {"Authorization": f"Bearer {token}"}


# ---------------------------
#   ROUTES PAGES JINJA2
# ---------------------------
@app.route("/")
def index():
    return render_template("index.j2")


@app.route("/auth")
def auth():
    return render_template("auth.j2")


@app.route("/users")
def users():
    return render_template("users.j2")


@app.route("/apps")
def apps():
    return render_template("apps.j2")


@app.route("/environments")
def environments():
    return render_template("environments.j2")


@app.route("/deployments")
def deployments():
    return render_template("deployments.j2")


@app.route("/events")
def events():
    return render_template("events.j2")


# ---------------------------
#   APPELS API AUTH
# ---------------------------
@app.route("/call/auth/login", methods=["POST"])
def call_login():
    payload = {
        "username": request.form["username"],
        "password": request.form["password"]
    }

    r = requests.post(f"{API}/auth/login", json=payload)

    if r.status_code == 200:
        data = r.json()
        session["token"] = data["accessToken"]

    return render_template("auth.j2", response=r.json())


@app.route("/call/auth/verify", methods=["POST"])
def call_verify():
    token = request.form["token"]
    r = requests.post(f"{API}/auth/verify", headers={"Authorization": f"Bearer {token}"})
    return render_template("auth.j2", response=r.json())


# ---------------------------
#   USERS
# ---------------------------
@app.route("/call/users/list")
def call_users_list():
    r = requests.get(f"{API}/users", headers=auth_headers())
    return render_template("users.j2", response=r.json())


@app.route("/call/users/create", methods=["POST"])
def call_users_create():
    payload = dict(request.form)
    r = requests.post(f"{API}/users", json=payload, headers=auth_headers())
    return render_template("users.j2", response=r.json())


@app.route("/call/users/get")
def call_users_get():
    user_id = request.args.get("userId")
    r = requests.get(f"{API}/users/{user_id}", headers=auth_headers())
    return render_template("users.j2", response=r.json())


# ---------------------------
#   APPLICATIONS
# ---------------------------
@app.route("/call/apps/list")
def call_apps_list():
    r = requests.get(f"{API}/apps", headers=auth_headers())
    return render_template("apps.j2", response=r.json())


@app.route("/call/apps/create", methods=["POST"])
def call_apps_create():
    payload = dict(request.form)
    r = requests.post(f"{API}/apps", json=payload, headers=auth_headers())
    return render_template("apps.j2", response=r.json())


@app.route("/call/apps/get")
def call_apps_get():
    app_id = request.args.get("app_id")
    r = requests.get(f"{API}/apps/{app_id}", headers=auth_headers())
    return render_template("apps.j2", response=r.json())


# ---------------------------
#   ENVIRONMENTS
# ---------------------------
@app.route("/call/environments/list")
def call_env_list():
    r = requests.get(f"{API}/environments", headers=auth_headers())
    return render_template("environments.j2", response=r.json())


@app.route("/call/environments/create", methods=["POST"])
def call_env_create():
    payload = dict(request.form)
    r = requests.post(f"{API}/environments", json=payload, headers=auth_headers())
    return render_template("environments.j2", response=r.json())


# ---------------------------
#   DEPLOYMENTS
# ---------------------------
@app.route("/call/deployments/list")
def call_deployments_list():
    r = requests.get(f"{API}/deployments", headers=auth_headers())
    return render_template("deployments.j2", response=r.json())


@app.route("/call/deployments/create", methods=["POST"])
def call_deployments_create():
    payload = dict(request.form)
    r = requests.post(f"{API}/deployments", json=payload, headers=auth_headers())
    return render_template("deployments.j2", response=r.json())


# ---------------------------
#   EVENTS
# ---------------------------
@app.route("/call/events/list")
def call_events_list():
    r = requests.get(f"{API}/events", headers=auth_headers())
    return render_template("events.j2", response=r.json())


@app.route("/call/events/create", methods=["POST"])
def call_events_create():
    payload = dict(request.form)
    r = requests.post(f"{API}/events", json=payload, headers=auth_headers())
    return render_template("events.j2", response=r.json())


# ---------------------------
#   RUN
# ---------------------------
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8081)
