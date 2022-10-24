from app import app
from flask import render_template, redirect, url_for, session
from models import Page
from sqlalchemy import select
import os
from flask_security import login_required


@app.route('/')
def index():
    pages = Page.query.all() # filteröidään vielä etusivun objektit
    file_path = os.path.join(app.config['UPLOAD_FOLDER'])

    return render_template('index.html', pages=pages, file_path=file_path)

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))