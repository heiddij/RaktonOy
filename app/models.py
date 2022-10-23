from app import db

pages_images = db.Table('pages_images',
                        db.Column('page_id', db.Integer,
                        db.ForeignKey('page.id')),
                        db.Column('image_id', db.Integer,
                        db.ForeignKey('image.id'))
)

class Image(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Unicode(64))
    path = db.Column(db.Unicode(128))

    def __unicode__(self):
        return self.name

    def __repr__(self):
        return f"Kuva: {self.name}"

class Page(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    images = db.relationship('Image', secondary=pages_images, backref=db.backref('pages'), lazy='dynamic')

    def __repr__(self):
        return f"{self.name}"