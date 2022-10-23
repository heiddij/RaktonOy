from app import app
from flask import render_template
from models import Image, Page
import PIL.Image as Image
import io
import base64
from sqlalchemy import select
import os

@app.route('/')
def index():
    pages = Page.query.all()
    file_path = os.path.join(app.config['UPLOAD_FOLDER'])
    # images = []
    # for post in posts:
    #     images.append(getattr(post, "photo"))

    # for img in images:
    #     b = base64.b64decode(img)
    #     image = Image.open(io.BytesIO(b))
    #     image.show()

    return render_template('index.html', pages=pages, file_path=file_path)