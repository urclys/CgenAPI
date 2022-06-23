
# -*- encoding: utf-8 -*-

import logging

from functools import wraps

from sqlalchemy import exc
from flask import abort

from app import db
from decorate_all_methods import decorate_all_methods


def db_error_handler(function):
    @wraps(function)
    def wrapper(*args, **kwargs):
        try:
            function(*args, **kwargs)
        except exc.SQLAlchemyError as e:
            db.session.rollback()
            logging.error('DB_error_handler {} : {}'.format(function.__name__, e))
            abort(500)

    return wrapper


@decorate_all_methods(db_error_handler)
class FactoryController:
    @staticmethod
    def get_one(Model, id):
        return Model.query.get_or_404(id)

    @staticmethod
    def get_all(Model):
        return Model.query.all()

    @staticmethod
    def createOne(obj):
        db.session.add(obj)
        db.session.commit()
        return obj.id

    @staticmethod
    def updateOne(obj, **kwargs):
        for property, value in kwargs.items():
            setattr(obj, property, value)
        db.session.commit()

    @staticmethod
    def deleteOne(obj):
        db.session.delete(obj)
        db.session.commit()

    @staticmethod
    def commit():
        db.session.commit()

    @staticmethod
    def rollback():
        db.session.rollback()
