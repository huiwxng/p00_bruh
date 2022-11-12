from db import get_connection

def create_tables():
    conn = get_connection()
    with conn:
        c = conn.cursor()
        c.execute("CREATE TABLE IF NOT EXISTS stories (id INTEGER PRIMARY KEY, title TEXT)")
        c.execute("CREATE TABLE IF NOT EXISTS contributions (id INTEGER PRIMARY KEY, text TEXT, story_id INT, user_id INT)")
    conn.close()


def add_contribution(text, story_id, user_id):
    conn = get_connection()
    with conn:
        c = conn.cursor()
        c.execute("INSERT INTO contributions (text, story_id, user_id) values (?, ?, ?)", (text, story_id, user_id))
    conn.close()


def create_story(title, text, user_id):
    conn = get_connection()
    with conn:
        c = conn.cursor()
        r = c.execute("INSERT INTO stories (title) values (?) RETURNING id", (title,))
        story = r.fetchone()
        story_id = story[0]
    conn.close()
    add_contribution(text, story_id, user_id)

    return story_id

def get_title(story_id):
    conn = get_connection()
    with conn:
        c = conn.cursor()
        r = c.execute("SELECT title FROM stories WHERE id = ?", (story_id,))
        title = r.fetchone()
    conn.close()
    return title[0]

def get_story(story_id):
    conn = get_connection()
    with conn:
        c = conn.cursor()
        r = c.execute("SELECT text FROM contributions WHERE story_id = ?", (story_id,))
        story = r.fetchall()
        story = [line[0] for line in story]
    conn.close()
    return story

def get_contributors(story_id):
    conn = get_connection()
    with conn:
        c = conn.cursor()
        r = c.execute("SELECT username FROM users JOIN contributions ON users.id=contributions.user_id WHERE story_id=?", (story_id,))
        contributors = r.fetchall()
        contributors = [line[0] for line in contributors]
    conn.close()
    print(contributors)

# TODO
def get_all_contributed_stories(user_id):
    conn = get_connection()
    with conn:
        c = conn.cursor()
        r = c.execute("SELECT * FROM stories JOIN contributions ON contributions.story_id = stories.id")
        story = r.fetchmany()
        print(story)
    conn.close()

def delete_table():
    conn = get_connection()
    with conn:
        c = conn.cursor()
        c.execute("DROP TABLE IF EXISTS stories")
        c.execute("DROP TABLE IF EXISTS contributions")
    conn.close()