
from flask import jsonify, request
from flask_jwt_extended import create_access_token, create_refresh_token, current_user, get_jwt_identity, jwt_required, set_access_cookies, set_refresh_cookies, unset_access_cookies, unset_refresh_cookies, verify_jwt_in_request

from app import db
from app.base import blueprint
from app.base.forms import SigninForm, ForgotForm
from app.base.models.users import User

from app.base.tools import (success_response, fail_response)

# @blueprint.route('/api/auth/protected')
# @jwt_required()
# def protected_route():
#     return jsonify(
#         id=current_user.id,
#         full_name=current_user.get_name
#     )

# @blueprint.route('/api/auth/fresh')
# @jwt_required(fresh=True)
# def protected_fresh_route():
#     return jsonify(
#         id=current_user.id,
#         full_name=current_user.get_name
#     )


@blueprint.route('/api/auth/login', methods=['POST'])
def login():
    verify_jwt_in_request(optional=True)
    if get_jwt_identity():
        return success_response(200,'Already logged in, Please log out before trying again !')
    
    data = request.json
    form = SigninForm(data=data)

    if form.validate():
        response = success_response(200)
        access_token = create_access_token(identity=form._user,fresh=True)
        refresh_token = create_refresh_token(identity=form._user)
        set_access_cookies(response, access_token)
        set_refresh_cookies(response, refresh_token)
        return response

    return fail_response(401, form.errors)


@blueprint.route('/api/auth/forgotPassword', methods=['POST'])
def forgot_password():
    data = request.json
    form = ForgotForm(data=data)
    if form.validate():
        user = User.query.filter_by(email=form.email.data).first()
        user.generate_forgot_token()
        db.session.commit()
        return success_response(200)
    else:
        return fail_response(400, form.errors)



# We are using the `refresh=True` options in jwt_required to only allow
# refresh tokens to access this route.
@blueprint.route("/api/auth/refresh", methods=["POST"])
@jwt_required(refresh=True)
def refresh():
    identity = get_jwt_identity()
    access_token = create_access_token(identity=identity,fresh=True)
    response = success_response(200)
    unset_access_cookies(response)
    set_access_cookies(response, access_token)
    return response

@blueprint.route("/api/auth/logout",methods=["GET"])
def logout():
    response = success_response(200,"You have successfully logged out !")
    unset_access_cookies(response)
    unset_refresh_cookies(response)
    return response