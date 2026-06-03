import sqlite3
import bcrypt
from contextlib import closing

DB_PATH = "app_data.db"


def init_db():
    """Initialize database with required tables."""
    with sqlite3.connect(DB_PATH) as conn:
        cur = conn.cursor()
        cur.execute("""CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY,
            username TEXT UNIQUE NOT NULL,
            pw_hash TEXT NOT NULL
        )""")
        cur.execute("""CREATE TABLE IF NOT EXISTS expenses (
            id INTEGER PRIMARY KEY,
            user_id INTEGER,
            amount REAL,
            note TEXT,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY(user_id) REFERENCES users(id)
        )""")
        cur.execute("""CREATE TABLE IF NOT EXISTS todos (
            id INTEGER PRIMARY KEY,
            user_id INTEGER,
            title TEXT,
            done INTEGER DEFAULT 0,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY(user_id) REFERENCES users(id)
        )""")
        conn.commit()


def execute(query, params=(), fetch=False):
    """Execute a query with optional fetch."""
    with sqlite3.connect(DB_PATH) as conn:
        cur = conn.cursor()
        cur.execute(query, params)
        if fetch:
            return cur.fetchall()
        conn.commit()


def create_user(username, password):
    """Create a new user with hashed password."""
    pw_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
    try:
        execute("INSERT INTO users (username, pw_hash) VALUES (?, ?)", (username, pw_hash))
        return True
    except sqlite3.IntegrityError:
        return False


def authenticate(username, password):
    """Authenticate user with username and password."""
    rows = execute("SELECT pw_hash FROM users WHERE username = ?", (username,), fetch=True)
    if not rows:
        return False
    stored = rows[0][0].encode()
    return bcrypt.checkpw(password.encode(), stored)


def get_user_id(username):
    """Get user ID by username."""
    rows = execute("SELECT id FROM users WHERE username = ?", (username,), fetch=True)
    return rows[0][0] if rows else None


# Expenses
def add_expense(user_id, amount, note):
    """Add expense for a user."""
    execute("INSERT INTO expenses (user_id, amount, note) VALUES (?, ?, ?)", (user_id, amount, note))


def get_expenses(user_id):
    """Get all expenses for a user."""
    return execute("SELECT id, amount, note, created_at FROM expenses WHERE user_id = ? ORDER BY created_at DESC", (user_id,), fetch=True)


# Todos
def add_todo(user_id, title):
    """Add todo for a user."""
    execute("INSERT INTO todos (user_id, title) VALUES (?, ?)", (user_id, title))


def get_todos(user_id):
    """Get all todos for a user."""
    return execute("SELECT id, title, done FROM todos WHERE user_id = ? ORDER BY created_at DESC", (user_id,), fetch=True)


def mark_todo_done(todo_id):
    """Mark a todo as done."""
    execute("UPDATE todos SET done = 1 WHERE id = ?", (todo_id,))


def delete_todo(todo_id):
    """Delete a todo."""
    execute("DELETE FROM todos WHERE id = ?", (todo_id,))
