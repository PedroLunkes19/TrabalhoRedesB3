import os
import psycopg2
from psycopg2.extras import RealDictCursor
from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

DB_CONFIG = {
    "host": os.environ.get("POSTGRES_HOST", "db"),
    "port": os.environ.get("POSTGRES_PORT", "5432"),
    "dbname": os.environ.get("POSTGRES_DB", ""),
    "user": os.environ.get("POSTGRES_USER", ""),
    "password": os.environ.get("POSTGRES_PASSWORD", ""),
}


def get_connection():
    return psycopg2.connect(**DB_CONFIG, cursor_factory=RealDictCursor)


def init_db():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS tasks (
            id SERIAL PRIMARY KEY,
            title TEXT NOT NULL,
            done BOOLEAN NOT NULL DEFAULT FALSE
        )
    """)

    conn.commit()
    cur.close()
    conn.close()


@app.route("/api/tasks", methods=["GET"])
def get_tasks():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("SELECT id, title, done FROM tasks ORDER BY id")
    tasks = cur.fetchall()

    cur.close()
    conn.close()

    return jsonify(tasks)


@app.route("/api/tasks", methods=["POST"])
def create_task():
    data = request.get_json(silent=True) or {}
    title = data.get("title", "").strip()

    if not title:
        return jsonify({"error": "O campo 'title' é obrigatório"}), 400

    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        "INSERT INTO tasks (title, done) VALUES (%s, %s) RETURNING id, title, done",
        (title, False),
    )

    task = cur.fetchone()

    conn.commit()
    cur.close()
    conn.close()

    return jsonify(task), 201


@app.route("/api/tasks/<int:task_id>", methods=["PUT"])
def update_task(task_id):
    data = request.get_json(silent=True) or {}

    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        """
        UPDATE tasks
        SET title = %s, done = %s
        WHERE id = %s
        RETURNING id, title, done
        """,
        (
            data.get("title", ""),
            data.get("done", False),
            task_id,
        ),
    )

    task = cur.fetchone()

    if task is None:
        cur.close()
        conn.close()
        return jsonify({"error": "Tarefa não encontrada"}), 404

    conn.commit()
    cur.close()
    conn.close()

    return jsonify(task)


@app.route("/api/tasks/<int:task_id>", methods=["DELETE"])
def delete_task(task_id):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        "DELETE FROM tasks WHERE id = %s RETURNING id",
        (task_id,),
    )

    deleted = cur.fetchone()

    if deleted is None:
        cur.close()
        conn.close()
        return jsonify({"error": "Tarefa não encontrada"}), 404

    conn.commit()
    cur.close()
    conn.close()

    return "", 204


init_db()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)