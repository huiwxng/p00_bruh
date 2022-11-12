from flask import Flask, render_template, request, session, redirect, flash
import secrets
from db import auth, stories

app = Flask(__name__)

@app.route("/")
def home():
    if 'username' in session:
        return render_template('home.html', contributed_stories=[], new_stories=[]) 
    return render_template('login.html')

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "GET":
        if 'username' in session:
            return redirect("/")
        return render_template('register.html')
    else:
        username = request.form["username"]
        password = request.form["password"]

        available = auth.check_username(username)
        if not available:
            return render_template('register.html', message="username not available")

        auth.register_user(username, password)

        session['username'] = request.form['username']
        return redirect('/') 

@app.route("/stories")
def contributed_stories():
    if 'username' not in session:
        return redirect("/")
    return render_template('stories.html', page_title="read stories", stories=[]) 

@app.route("/new_stories")
def new_stories():
    if 'username' not in session:
        return redirect("/")
    return render_template('stories.html', page_title="new stories", stories=[]) 

@app.route("/new", methods=["GET", "POST"])
def new():
    if 'username' not in session:
        return redirect("/")
    if request.method == "GET":
        return render_template('new_story.html')
    else:
        stories.create_story(request.form["title"], request.form["story"], session['user_id'])
        return redirect('/') 

@app.route("/story/<id>")
def story(id):
    if 'username' not in session:
        return redirect("/")
    # should only be visible to users who contributed to story id
    return render_template('story.html', story_title="test", authors=["ts", "sm"], story="hello world") 

@app.route("/hidden_story/<id>") # merge with /story/<id> once db in place
def hidden_story(id):
    if 'username' not in session:
        return redirect("/")
    return render_template('hidden_story.html', story_title="test", story_id=id, last_line="hello") 

@app.route("/login", methods=["POST"])
def login():
    username = request.form["username"]
    password = request.form["password"]
    info_correct = auth.check_creds(username, password)

    if info_correct:
        session['username'] = username
        session['user_id'] = auth.get_user_id(username)
    else:
        flash("invalid username or password")

    return redirect("/")

@app.route("/home")
def back_home():
    return redirect("/")

@app.route("/logout")
def logout():
    session.pop('username', None)
    flash("logged out")
    return redirect("/")

if __name__ == "__main__":
    app.debug = True
    app.secret_key = secrets.token_hex()
    
    auth.create_table()
    stories.create_tables()

    app.run()