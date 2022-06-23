from flask import jsonify
from app import jwt
from app.base import blueprint
from app.base.tools import fail_response

# Set a callback function to return a custom response whenever an expired
# token attempts to access a protected route. This particular callback function
# takes the jwt_header and jwt_payload as arguments, and must return a Flask
# response. Check the API documentation to see the required argument and return
# values for other callback functions.
@jwt.expired_token_loader
def my_expired_token_callback(jwt_header, jwt_payload):
    return fail_response(413,'Your token has expired !')


@blueprint.app_errorhandler(403)
def access_forbidden(error):
    return fail_response(403, error)

@blueprint.app_errorhandler(404)
def not_found_error(error):
    msg = 'This route doesnt exist or underconstruction'
    return fail_response(404, msg)

@blueprint.app_errorhandler(500)
def internal_error(error):
    msg = 'Internal Error. Please try again !'
    return fail_response(500,msg)

