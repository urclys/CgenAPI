import code
from app import db

#Business models

class Clause(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(36), nullable=False, index=True)
    content = db.Column(db.Text, nullable=False)
    

class Contrat(db.Model):
    pass

class DroitType(db.Model):
    pass

