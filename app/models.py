from xmlrpc.client import Boolean
from app import db
from flask_security import UserMixin, RoleMixin


# Create table for many-to-many relationship for pages and images
pages_images = db.Table('pages_images',
                        db.Column('page_id', db.Integer,
                        db.ForeignKey('page.id')),
                        db.Column('image_id', db.Integer,
                        db.ForeignKey('image.id'))
)

roles_users = db.Table('roles_users',
                        db.Column('user_id', db.Integer,
                        db.ForeignKey('user.id')),
                        db.Column('role_id', db.Integer,
                        db.ForeignKey('role.id'))
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


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(255))
    active = db.Column(db.Boolean)
    roles = db.relationship('Role', secondary=roles_users, backref=db.backref('users'), lazy='dynamic')


class Role(db.Model, RoleMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True)


class ContactForm(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    phone = db.Column(db.String)
    email = db.Column(db.String)
    message = db.Column(db.String)