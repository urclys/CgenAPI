#!/bin/bash
export FLASK_APP=run.py  
export CONFIG_MODE Docker
export OAUTHLIB_INSECURE_TRANSPORT=True


echo "running"
flask run --host=0.0.0.0