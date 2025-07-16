from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse
import mysql.connector
import os
from pathlib import Path

app = FastAPI()

# ───────────────────────────────── CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],        # OK for dev; restrict in prod
    allow_methods=["*"],
    allow_headers=["*"],
)

# ───────────────────────────────── DB config
DB_CONFIG = {
    "host": os.getenv("DB_HOST", "db"),
    "user": os.getenv("DB_USER", "user"),
    "password": os.getenv("DB_PASSWORD", "password"),
    "database": os.getenv("DB_NAME", "testdb"),
}

# ───────────────────────────────── API routes
@app.get("/api/users")
def get_users():
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT id, name FROM users")
        users = cursor.fetchall()
        return users
    except Exception as e:
        return {"error": str(e)}
    finally:
        if 'cursor' in locals(): cursor.close()
        if 'conn' in locals(): conn.close()

@app.get("/ping")
def ping():
    return {"message": "pong"}

# ───────────────────────────────── Static React bundle
STATIC_DIR = Path(__file__).parent / "app" / "static"
app.mount("/static", StaticFiles(directory=STATIC_DIR, html=True), name="static")

# Optional convenience redirect: GET /  →  /static/
@app.get("/", include_in_schema=False)
def root_redirect():
    return RedirectResponse("/static/")

