# -*- encoding: utf-8 -*-
from app import db,jwt

from app.base.tools import hash_pass
import secrets
import datetime

@jwt.user_identity_loader
def user_identity_lookup(user):
    return user.id

@jwt.user_lookup_loader
def user_lookup_callback(_jwt_header, jwt_data):
    identity = jwt_data["sub"]
    return User.query.filter_by(id=identity).one_or_none()

############## MIXINS ##############################################

class TimestampMixin(object):
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(
        db.DateTime, server_default=db.func.now(), server_onupdate=db.func.now())

############## Models ##############################################


class User(db.Model, TimestampMixin):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(60), index=True, unique=True)
    first_name = db.Column(db.String(60), index=True, unique=True)
    last_name = db.Column(db.String(60), index=True, unique=True)
    password = db.Column(db.String(128))
    password_reset_token = db.Column(db.String(128))
    password_reset_expires = db.Column(db.DateTime)
    activation_token = db.Column(db.String(128))

    is_admin = db.Column(db.Boolean, default=False)

    last_seen = db.Column(db.DateTime, server_default=db.func.now())
    is_active = db.Column(db.Boolean, default=False)

    def __init__(self, **kwargs):
        for property, value in kwargs.items():
            # depending on whether value is an iterable or not, we must
            # unpack it's value (when **kwargs is request.form, some values
            # will be a 1-element list)
            if hasattr(value, '__iter__') and not isinstance(value, str):
                # the ,= unpack of a singleton fails PEP8 (travis flake8 test)
                value = value[0]

            if property == 'password':
                value = hash_pass(value)  # hash the password

            setattr(self, property, value)

    def __repr__(self):
        return f"<User {self.id} - {self.email}>"

    def change_password(self, newPassword):
        self.password = hash_pass(newPassword)

    def generate_forgot_token(self):
        token = secrets.token_urlsafe(16)
        token_exp_minutes = 10
        self.password_reset_token = token
        self.password_reset_expires = datetime.datetime.now(
        ) + datetime.timedelta(minutes=token_exp_minutes)

    def generate_activation_token(self):
        token = secrets.token_urlsafe(16)
        self.activation_token = token

    @property
    def get_name(self):
        return f"{self.first_name} {self.last_name}"


# it could track who revoked a JWT, when a token expires, notes for why a
# JWT was revoked, an endpoint to un-revoked a JWT, etc.
# Making jti an index can significantly speed up the search when there are
# tens of thousands of records. Remember this query will happen for every
# (protected) request,
# If your database supports a UUID type, this can be used for the jti column
# as well

class TokenBlocklist(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    jti = db.Column(db.String(36), nullable=False, index=True)
    created_at = db.Column(db.DateTime, nullable=False)


# Callback function to check if a JWT exists in the database blocklist
@jwt.token_in_blocklist_loader
def check_if_token_revoked(jwt_header, jwt_payload: dict) -> bool:
    jti = jwt_payload["jti"]
    token = db.session.query(TokenBlocklist.id).filter_by(jti=jti).scalar()
    return token is not None