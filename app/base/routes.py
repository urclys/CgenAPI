# -*- encoding: utf-8 -*-


from datetime import datetime, timedelta, timezone
from flask_jwt_extended import create_access_token, current_user, get_jwt, get_jwt_identity, set_access_cookies
from app import db
from flask import current_app as app
from app.base import blueprint


@blueprint.before_app_request
def last_seen_updater():
    if current_user:
        current_user.last_seen = db.func.now()
        db.session.commit()

# Using an `after_request` callback, we refresh any token that is within 30
# minutes of expiring. Change the timedeltas to match the needs of your application.
@app.after_request
def refresh_expiring_jwts(response):
    try:
        exp_timestamp = get_jwt()["exp"]
        now = datetime.now(timezone.utc)
        target_timestamp = datetime.timestamp(now + timedelta(minutes=30))
        if target_timestamp > exp_timestamp:
            access_token = create_access_token(identity=get_jwt_identity())
            set_access_cookies(response, access_token)
        return response
    except (RuntimeError, KeyError):
        # Case where there is not a valid JWT. Just return the original response
        return response