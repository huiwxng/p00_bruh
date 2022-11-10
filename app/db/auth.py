from db import get_connection

def create_table():
    conn = get_connection()
    with conn:
        c = conn.cursor()
        c.execute("CREATE TABLE IF NOT EXISTS users (name TEXT)")
    conn.close()