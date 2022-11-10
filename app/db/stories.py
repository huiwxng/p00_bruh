from db import get_connection

def create_tables():
    conn = get_connection()
    with conn:
        c = conn.cursor()
        c.execute("CREATE TABLE IF NOT EXISTS stories (id INT, title TEXT)")
        c.execute("CREATE TABLE IF NOT EXISTS contributions (id INT, text TEXT, timestamp INT, story_id INT, user_id INT)")
    conn.close()