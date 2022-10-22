from app import app, db
from flask import render_template
from models import Post

@app.route('/')
def index():
    posts = Post.query.all()
    return render_template('index.html', posts=posts)