import os
import sqlite3
from pathlib import Path

from flask import Flask, g, jsonify, request
from werkzeug.security import check_password_hash, generate_password_hash


def create_app(test_config=None):
    app = Flask(__name__)
    app.config.from_mapping(
        DATABASE=os.environ.get("ACEEST_DATABASE", str(Path(app.instance_path) / "aceest_fitness.db")),
        ADMIN_USERNAME=os.environ.get("ACEEST_ADMIN_USERNAME", "admin"),
        ADMIN_PASSWORD=os.environ.get("ACEEST_ADMIN_PASSWORD", "change-me"),
    )
    if test_config:
        app.config.update(test_config)
    Path(app.instance_path).mkdir(parents=True, exist_ok=True)

    def get_db():
        if "db" not in g:
            g.db = sqlite3.connect(app.config["DATABASE"])
            g.db.row_factory = sqlite3.Row
        return g.db

    def init_db():
        db = get_db()
        db.executescript(
            """
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password_hash TEXT NOT NULL,
                role TEXT NOT NULL
            );
            CREATE TABLE IF NOT EXISTS clients (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT UNIQUE NOT NULL,
                age INTEGER,
                height REAL,
                weight REAL,
                program TEXT,
                target_weight REAL,
                membership_expiry TEXT
            );
            CREATE TABLE IF NOT EXISTS workouts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                client_id INTEGER NOT NULL,
                date TEXT NOT NULL,
                workout_type TEXT NOT NULL,
                duration_min INTEGER NOT NULL,
                notes TEXT DEFAULT '',
                FOREIGN KEY (client_id) REFERENCES clients (id)
            );
            """
        )
        admin = db.execute(
            "SELECT id FROM users WHERE username = ?",
            (app.config["ADMIN_USERNAME"],),
        ).fetchone()
        if admin is None:
            db.execute(
                "INSERT INTO users (username, password_hash, role) VALUES (?, ?, ?)",
                (
                    app.config["ADMIN_USERNAME"],
                    generate_password_hash(app.config["ADMIN_PASSWORD"]),
                    "Admin",
                ),
            )
        db.commit()

    @app.teardown_appcontext
    def close_db(_error=None):
        db = g.pop("db", None)
        if db is not None:
            db.close()

    with app.app_context():
        init_db()

    @app.get("/health")
    def health():
        return jsonify(status="ok", service="aceest-fitness")

    @app.post("/login")
    def login():
        payload = request.get_json(silent=True) or {}
        user = get_db().execute(
            "SELECT username, password_hash, role FROM users WHERE username = ?",
            (payload.get("username", ""),),
        ).fetchone()
        if user is None or not check_password_hash(user["password_hash"], payload.get("password", "")):
            return jsonify(error="Invalid credentials"), 401
        return jsonify(username=user["username"], role=user["role"])

    @app.get("/clients")
    def list_clients():
        rows = get_db().execute("SELECT * FROM clients ORDER BY name").fetchall()
        return jsonify([dict(row) for row in rows])

    @app.post("/clients")
    def create_client():
        payload = request.get_json(silent=True) or {}
        name = str(payload.get("name", "")).strip()
        if not name:
            return jsonify(error="name is required"), 400
        try:
            db = get_db()
            cursor = db.execute(
                """INSERT INTO clients
                   (name, age, height, weight, program, target_weight, membership_expiry)
                   VALUES (?, ?, ?, ?, ?, ?, ?)""",
                (
                    name,
                    payload.get("age"),
                    payload.get("height"),
                    payload.get("weight"),
                    payload.get("program"),
                    payload.get("target_weight"),
                    payload.get("membership_expiry"),
                ),
            )
            db.commit()
        except sqlite3.IntegrityError:
            return jsonify(error="client already exists"), 409
        client = db.execute("SELECT * FROM clients WHERE id = ?", (cursor.lastrowid,)).fetchone()
        return jsonify(dict(client)), 201

    @app.get("/clients/<int:client_id>/workouts")
    def list_workouts(client_id):
        client = get_db().execute("SELECT id FROM clients WHERE id = ?", (client_id,)).fetchone()
        if client is None:
            return jsonify(error="client not found"), 404
        rows = get_db().execute(
            "SELECT * FROM workouts WHERE client_id = ? ORDER BY date DESC, id DESC",
            (client_id,),
        ).fetchall()
        return jsonify([dict(row) for row in rows])

    @app.post("/clients/<int:client_id>/workouts")
    def create_workout(client_id):
        payload = request.get_json(silent=True) or {}
        required = ("date", "workout_type", "duration_min")
        missing = [field for field in required if payload.get(field) in (None, "")]
        if missing:
            return jsonify(error=f"missing fields: {', '.join(missing)}"), 400
        client = get_db().execute("SELECT id FROM clients WHERE id = ?", (client_id,)).fetchone()
        if client is None:
            return jsonify(error="client not found"), 404
        db = get_db()
        cursor = db.execute(
            """INSERT INTO workouts (client_id, date, workout_type, duration_min, notes)
               VALUES (?, ?, ?, ?, ?)""",
            (
                client_id,
                payload["date"],
                payload["workout_type"],
                payload["duration_min"],
                payload.get("notes", ""),
            ),
        )
        db.commit()
        workout = db.execute("SELECT * FROM workouts WHERE id = ?", (cursor.lastrowid,)).fetchone()
        return jsonify(dict(workout)), 201

    return app


app = create_app()


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", "5000")))
