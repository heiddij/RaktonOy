from app import app, db, mail
from flask import Flask, render_template, redirect, url_for, request, session, jsonify
from models import Page, ContactForm
from sqlalchemy import select
import os
from flask_security import login_required
from forms import FormContact
import re
from flask_mail import Mail, Message
from chat import get_response


# app.route default method is GET
@app.route('/')
def index():
    page = Page.query.filter_by(name='Etusivu').first() 
    file_path = os.path.join(app.config['UPLOAD_FOLDER'])
    return render_template('index.html', page=page, file_path=file_path)


@app.route('/asuntokauppa')
def asuntokauppa():
    page = Page.query.filter_by(name='Asuntokaupan kuntotarkastus').first() 
    file_path = os.path.join(app.config['UPLOAD_FOLDER'])
    return render_template('asuntokauppa.html', page=page, file_path=file_path)


@app.route('/vaestonsuoja')
def vaestonsuoja():
    page = Page.query.filter_by(name='Väestönsuojan tarkastus').first() 
    file_path = os.path.join(app.config['UPLOAD_FOLDER'])
    return render_template('vaestonsuoja.html', page=page, file_path=file_path)

@app.route('/remontit')
def remontit():
    page = Page.query.filter_by(name='Huoneisto- ja toimistoremontit').first() 
    file_path = os.path.join(app.config['UPLOAD_FOLDER'])
    return render_template('remontit.html', page=page, file_path=file_path)


@app.route('/contact', methods=('GET', 'POST'))
def post_contact():
    form = FormContact()
    thank_u = "Kiitos yhteydenotostasi, otamme sinuun yhteyttä mahdollisimman pian!"
    if form.validate_on_submit(): # also checks that the request is a POST request
        # Sanitize fields from HTML tags
        name = re.sub(r"<.*?>", "", form.name.data)
        phone = re.sub(r"<.*?>", "", form.phone.data)
        email = re.sub(r"<.*?>", "", form.email.data)
        message = re.sub(r"<.*?>", "", form.message.data)
        contact = ContactForm(name=name, phone=phone, email=email, message=message)
        # Add to database and save
        db.session.add(contact)
        db.session.commit()
        # Send email
        msg = Message("Uusi yhteydenottopyyntö", sender='heidi.joutsijoki@gmail.com', recipients=['heidi20151@student.hamk.fi'])
        msg.body = """ 
        From: %s <%s> %s
        %s 
        """ % (form.name.data, form.email.data, form.phone.data, form.message.data)
        mail.send(msg)
        #return redirect(url_for('index')) # muuta tää vielä et kiitosteksti tms
    return render_template('contact.html', form=form, thank_u=thank_u)


@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))


@app.route('/predict', methods=['POST'])
def predict():
    text = request.get_json().get("message")
    # TODO: check if text is valid
    response = get_response(text)
    message = {"answer": response}
    return jsonify(message)

