from app import db 

############## MIXINS ##############################################

class TimestampMixin(object):
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(
        db.DateTime, server_default=db.func.now(), server_onupdate=db.func.now())

class ActivableMixin(object):
    is_active = db.Column(db.Boolean, default=False)
