#!/bin/bash
export FLASK_APP=run.py  

echo "Initiating"
flask db init

echo "migrating"
flask db migrate

echo "upgrading"
flask db upgrade

echo "running"
flask run --host=0.0.0.0