import datetime
import json
import secrets
from flask import current_app, jsonify, redirect, request
from flask_jwt_extended import create_access_token, create_refresh_token, current_user, get_jwt, get_jwt_identity, jwt_required, set_access_cookies, set_refresh_cookies, unset_access_cookies, unset_refresh_cookies, verify_jwt_in_request
import requests

from app import db, init_oauth
from app.base import blueprint
from app.base.forms import SigninForm, ForgotForm
from app.base.models.users import Client, TokenBlocklist, User
from app.base.orm_tools import FactoryController

from app.base.tools import (get_google_provider_cfg, login_user_using_cookies,
                            success_response, fail_response)

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


@blueprint.route("/api/auth/login/google")
def login():
    verify_jwt_in_request(optional=True)
    if get_jwt_identity():
        return success_response(200,'Already logged in, Please log out before trying again !')

    # Find out what URL to hit for Google login
    google_provider_cfg = get_google_provider_cfg()
    authorization_endpoint = google_provider_cfg["authorization_endpoint"]

    # Use library to construct the request for Google login and provide
    # scopes that let you retrieve user's profile from Google
    request_uri = init_oauth(current_app).prepare_request_uri(
        authorization_endpoint,
        redirect_uri=request.base_url + "/callback",
        scope=["openid", "email", "profile"],
    )
    return redirect(request_uri)


@blueprint.route("/api/auth/login/google/callback")
def callback():
    # Get authorization code Google sent back to you
    code = request.args.get("code")
    # Find out what URL to hit to get tokens that allow you to ask for
    # things on behalf of a user
    google_provider_cfg = get_google_provider_cfg()
    token_endpoint = google_provider_cfg["token_endpoint"]

    # Prepare and send a request to get tokens
    client = init_oauth(current_app)
    token_url, headers, body = client.prepare_token_request(
        token_endpoint,
        authorization_response=request.url,
        redirect_url=request.base_url,
        code=code)
    token_response = requests.post(
        token_url,
        headers=headers,
        data=body,
        auth=(current_app.config['GOOGLE_CLIENT_ID'],
              current_app.config['GOOGLE_CLIENT_SECRET']),
    )

    # Parse the tokens!
    client.parse_request_body_response(json.dumps(token_response.json()))

    #  hit the URL  from Google that gives you the user's profile information,
    # including their Google profile image and email
    userinfo_endpoint = google_provider_cfg["userinfo_endpoint"]
    uri, headers, body = client.add_token(userinfo_endpoint)
    userinfo_response = requests.get(uri, headers=headers, data=body)

    # You want to make sure their email is verified.
    # The user authenticated with Google, authorized your
    # app, and now you've verified their email through Google!
    if userinfo_response.json().get("email_verified"):
        print(userinfo_response.json())
        users_email = userinfo_response.json()["email"]
        family_name = userinfo_response.json()["family_name"]
        users_name = userinfo_response.json()["given_name"]
    else:
        return fail_response(
            400, "User email not available or not verified by Google.")

    # Create a user in your db with the information provided
    # by Google

    # Doesn't exist? Add it to the database.
    user = User.query.filter_by(email=users_email).first()
    if not user:
        user = Client(first_name=users_name,
                      last_name=family_name,
                      email=users_email,
                      password=secrets.token_urlsafe(16))
        FactoryController.createOne(user)

    # Begin user session by logging the user in
    resp = login_user_using_cookies(user,
                                    response=success_response(
                                        200, 'Logged in succesfully'))

    # Send user back to homepage
    return resp


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
    access_token = create_access_token(identity=identity, fresh=True)
    response = success_response(200)
    unset_access_cookies(response)
    set_access_cookies(response, access_token)
    return response


@blueprint.route("/api/auth/logout", methods=["GET","DELETE"])
@jwt_required(verify_type=False)
def logout():
    token = get_jwt()
    jti = token["jti"]
    ttype = token["type"]
    now = datetime.datetime.now(datetime.timezone.utc)
    FactoryController.createOne(
        TokenBlocklist(jti=jti, type=ttype, created_at=now))
    resp = success_response(
        200, f"{ttype.capitalize()} token successfully revoked")
    # unset_access_cookies(resp)
    # unset_refresh_cookies(resp)
    return resp
