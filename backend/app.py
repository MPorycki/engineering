from functools import wraps

from flask import Flask, request, make_response
from flask.json import jsonify
from flask_restful import Api, Resource
from flask_cors import CORS

from Modules.user_management import (
    login,
    register_user,
    logout,
    change_password,
    session_exists,
    update_user,
)

from Modules.crud_common import fetch_all_objects, fetch_object, delete_object

from models import (
    Accounts,
)

app = Flask(__name__)
api = Api(app)
CORS(app)


def verify_session(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            data = request.get_json()
            session_id = data["session_id"]
            account_id = data["account_id"]
        except Exception as e:
            print(e)
            return make_response("Invalid session", 401)
        if session_exists(session_id, account_id):
            return func(**kwargs)
        else:
            return make_response("Invalid session", 401)

    return wrapper()


class Account(Resource):
    def get(self, _id=None):
        if _id:
            result = fetch_object(Accounts, _id)
            return make_response(result, 200)
        else:
            result = fetch_all_objects(Accounts)
            return make_response(result, 200)

    def post(self):
        """
        Create a new user based on provided data
        :return: HTTP status of the registration attempt
        """
        try:
            data = request.get_json()
            email = data["email"]
            raw_password = data["raw_password"]
            fist_name = data["fist_name"]
            last_name = data["last_name"]
            account_type = data["account_type"]
        except KeyError as e:
            print(e)
            return make_response("Not enough data provided, missing data: " + e, 400)
        registration = register_user(
            email, raw_password, fist_name, last_name, account_type
        )
        if registration["success"]:
            return make_response("Registration successful", 200)
        else:
            return make_response(jsonify(registration), 401)

    def patch(self):
        data = request.get_json()
        result = update_user(data)
        if result:
            return make_response(str(result), 200)
        else:
            return make_response(str(result), 400)

    def delete(self, _id):
        delete = delete_object(object_table=Accounts, object_id=_id)
        return make_response(str(delete), 200)


api.add_resource(Account, "/account/", "/account/<_id>")


class AccountLogin(Resource):
    def post(self):
        """
        Authorizes the user via provided email and password
        :return: HTTP Response with a JSON attached
                 Structure of the JSON  {"session_id": uuid,
                                        "account_id": uuid,
                                        "email_exists": bool,
                                        "correct_pass": bool}
                 HTTP responses: 200 if authorization was successful
                                 400 if not enough data was provided
                                 401 if the password was incorrect for the given email or the email is not in the db
        """
        try:
            data = request.get_json()
            raw_password = data["raw_password"]
            email = data["email"]
        except KeyError as e:
            print(e)
            return make_response("Not enough data provided" + e, 400)
        result = login(email=email, raw_password=raw_password)
        if result["session_id"]:
            return make_response(jsonify(result), 200)
        else:
            return make_response(jsonify(result), 401)


api.add_resource(AccountLogin, "/account/login")


class AccountResetPassword(Resource):
    def patch(self):
        """
        Handle password change initiated by the user.
        :return: HTTP response: 200 if the change was successful, 403 otherwise.
        """
        data = request.get_json()
        new_password = data["new_password"]
        account_id = data["account_id"]
        password_change = change_password(account_id, new_password)
        if password_change:
            return make_response("Password changed", 200)
        else:
            return make_response("Password was not changed", 403)


api.add_resource(AccountResetPassword, "/account/reset")


class AccountLogout(Resource):
    def delete(self):
        """
        Logouts the user.
        :return: HTTP Response: 200 if the logout was successful, 400 if the session does not exists for the user
        """
        account_id = request.headers.get("account_id")
        session_id = request.headers.get("session_id")
        logout_result = logout(session_id, account_id)
        if logout_result:
            return make_response("User logged out.", 200)
        else:
            return make_response("Given session does not exists for given user.", 400)


api.add_resource(AccountLogout, "/account/logout")


class Main(Resource):
    def get(self):
        return make_response("True", 200)


api.add_resource(Main, "/")
