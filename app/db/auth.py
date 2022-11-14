from db import get_connection


def create_table():
    conn = get_connection()
    with conn:
        c = conn.cursor()
        c.execute("CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, username TEXT, password TEXT)")
    conn.close()


def check_creds(username, password):
    conn = get_connection()
    with conn:
        c = conn.cursor()
        r = c.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username, password))
        user = r.fetchone()
    conn.close()

    return user is not None


def check_username(username):
    conn = get_connection()
    with conn:
        c = conn.cursor()
        r = c.execute("SELECT * FROM users WHERE username = ?", (username,))
        user = r.fetchone()
    conn.close()

    return user is None


def get_user_id(username):
    conn = get_connection()
    with conn:
        c = conn.cursor()
        r = c.execute("SELECT id FROM users WHERE username = ?", (username,))
        id = r.fetchone()
    conn.close()

    return id[0]


def register_user(username, password):
    available = check_username(username)
    if not available:
        return False

    conn = get_connection()
    with conn:
        c = conn.cursor()
        c.execute("INSERT INTO users(username, password) values (?, ?)", (username, password))
    conn.close()

    return True


def delete_table():
    conn = get_connection()
    with conn:
        c = conn.cursor()
        c.execute("DROP TABLE IF EXISTS users")
    conn.close()
