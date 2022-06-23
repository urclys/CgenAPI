# -*- encoding: utf-8 -*-

import os
import os.path
import secrets
import logging
from datetime import datetime

from functools import wraps
from threading import Thread


from flask import current_app as app, jsonify, make_response
from flask import abort
from flask_mail import Message
from werkzeug.security import generate_password_hash, check_password_hash

from app import db, mail

from decorate_all_methods import decorate_all_methods



def hash_pass(password):
    password_hash = generate_password_hash(password)
    return password_hash


def verify_pass(provided_password, stored_password):
    pwhash = stored_password
    password = provided_password
    return check_password_hash(pwhash, password)


############################ JSON Response format #############################


def success_response(httpCode, data=None):
    return make_response(jsonify({'status': 'success', 'data': data}), httpCode)


def fail_response(httpCode, message):
    return make_response(jsonify({'status': 'fail', 'data': {'error': httpCode, 'message': message}}), httpCode)


########################### Email handler #######################

def send_async_email(app, msg):
    with app.app_context():
        mail.send(msg)


def send_email(subject, sender, recipients, text_body, html_body):
    msg = Message(subject, sender=sender, recipients=recipients)
    msg.body = text_body
    msg.html = html_body
    Thread(target=send_async_email,
           args=(app._get_current_object(), msg)).start()


