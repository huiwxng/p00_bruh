from flask import Flask, render_template, request, session, redirect
import secrets
from db import auth, stories

app = Flask(__name__)

@app.route("/", methods=['GET', 'POST'])
def home():
    if request.method == "GET":
        if 'username' in session:
            return render_template('home.html', contributed_stories=[], new_stories=[]) 
        return render_template('login.html')
    else:
        username = request.form["username"]
        password = request.form["password"]
        info_correct = auth.check_creds(username, password)

        if info_correct:
            session['username'] = request.form['username']
            return render_template('home.html', contributed_stories=[], new_stories=[])

        return render_template('login.html', message = "wrong username or password")

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
    return render_template('stories.html', page_title="read stories", stories=[]) 

@app.route("/new_stories")
def new_stories():
    return render_template('stories.html', page_title="new stories", stories=[]) 

@app.route("/new")
def new():
    return render_template('new_story.html') 

@app.route("/story/<id>")
def story(id):
    # should only be visible to users who contributed to story id
    return render_template('story.html', story_title="test", authors=["ts", "sm"], story="hello world") 

@app.route("/hidden_story/<id>") # merge with /story/<id> once db in place
def hidden_story(id):
    return render_template('hidden_story.html', story_title="test", story_id=id, last_line="hello") 

@app.route("/logout")
def logout():
    session.pop('username', None)
    return redirect("/")

if __name__ == "__main__":
    app.debug = True
    app.secret_key = secrets.token_hex()
    
    auth.create_table()
    stories.create_tables()

    app.run()