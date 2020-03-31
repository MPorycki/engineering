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
from Modules.adresses import get_adress

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
            session_id = request.headers.get("session_id")
            account_id = request.headers.get("account_id")
        except Exception as e:
            print(e)
            return make_response(401, "Invalid session")
        if session_exists(session_id, account_id):
            return func(**kwargs)
        else:
            return make_response(401, "Invalid session")

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
            return make_response("Registration succesfull", 200)
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
        # Password change handling
        new_password = request.form.get("new_password")
        account_id = request.headers.get("account_id")
        password_change = change_password(account_id, new_password)
        if password_change == "password_changed":
            return make_response(password_change, 200)
        elif password_change == "user_does_not_exist":
            return make_response(password_change, 403)
        elif password_change == "message_not_sent":
            return make_response(password_change, 400)


api.add_resource(AccountResetPassword, "/account/reset")


class AccountLogout(Resource):
    def delete(self):
        # Logout
        account_id = request.headers.get("account_id")
        session_id = request.headers.get("session_id")
        logout_result = logout(session_id, account_id)
        if logout_result == "logout_successful":
            return make_response(logout_result, 200)
        elif logout_result == "logout_unsuccessful":
            return make_response(logout_result, 400)
        else:
            return make_response(None, 500)


api.add_resource(AccountLogout, "/account/logout")


class Projects(Resource):  # we assume the session is verified
    def get(self, project_id=None):
        if project_id:
            project = fetch_object(
                object_table=projects_table, object_id=project_id
            )
            # Add adress to payload
            adress = get_adress(project["id"])
            project.update(adress)
            return make_response(jsonify(project), 200)
        else:
            projects = fetch_all_objects(projects_table)
            return make_response(jsonify(projects), 200)

    def post(self):
        try:
            data = request.get_json()
            name = data["name"]
            owner = data["owner_id"]
            description = data["description"]
            adress = data["adress"]
            requested_participants = data["requested_participants"]
        except Exception as e:
            print(str(e.__class__.__name__) + ": " + str(e))
            return make_response("Not enough data provided", 400)
        project = create_project(
            name, owner, description, requested_participants, adress
        )
        if project:
            add_participant(
                account_id=data["owner_id"], project_id=project, role="Tworca"
            )
            return make_response("", 200)
        else:
            return make_response("Serwer nie przyjal danych", 400)

    def patch(self):
        data = request.get_json()
        _id = update_project(data)
        if _id:
            return make_response(str(_id), 200)
        else:
            return make_response("Serwer nie przyjal danych", 400)

    def delete(self, project_id):
        delete = delete_object(
            object_table=projects_table, object_id=project_id
        )
        return make_response(str(delete), 200)


api.add_resource(Projects, "/projects", "/projects/<project_id>")


class Ranking(Resource):
    def get(self):
        ranking = dict()
        ranking["projects"] = get_best_projects()
        return make_response(jsonify(ranking), 200)


api.add_resource(Ranking, "/ranking")


class Comments(Resource):
    def get(self, id):
        comments = get_comments(id)
        return make_response(comments, 200)

    def post(self):
        data = request.get_json()
        result = create_comment(
            user_id=data["user_id"],
            project_id=data["project_id"],
            text=data["text"],
        )
        if result:
            return make_response(jsonify(result), 200)
        else:
            return make_response("", 400)

    def patch(self):
        data = request.get_json()
        _id = update_comment(data)
        if _id:
            return make_response(str(_id), 200)
        else:
            return make_response(str(_id), 400)

    def delete(self, id):
        delete = delete_object(object_table=comments_table, object_id=id)
        return make_response(str(delete), 200)


api.add_resource(Comments, "/comments", "/comments/<id>")


class Comment(Resource):
    def get(self, _id):
        comment = get_comment(_id)
        return make_response(jsonify(comment), 200)


api.add_resource(Comment, "/comment/<_id>")


class Participants(Resource):
    def get(self, _id):
        result = fetch_all_participants(_id)
        return make_response(result, 200)

    def post(self):
        data = request.get_json()
        result = add_participant(
            account_id=data["user_id"],
            project_id=data["project_id"],
            role=data["role"],
        )
        if result:
            return make_response(jsonify(result), 200)
        else:
            return make_response("", 400)

    def patch(self):
        data = request.get_json()
        result = update_participant(data["participant_id"], data["role"])
        return make_response(str(result), 200)

    def delete(self, _id):
        delete = delete_object(
            object_table=InitiativesParticipants, object_id=_id
        )
        return make_response(str(delete), 200)


api.add_resource(Participants, "/participants/", "/participants/<_id>")


class Votes(Resource):
    def post(self):
        data = request.get_json()
        if not alread_voted(data["user_id"], data["type"], data["object_id"]):
            _id = vote(
                data["user_id"],
                data["type"],
                data["object_id"],
                data["is_upvote"],
            )
            return make_response(str(_id), 200)
        else:
            return make_response("Juz na to zaglosowales", 403)


api.add_resource(Votes, "/votes/")


class Main(Resource):
    def get(self):
        return make_response("True", 200)


api.add_resource(Main, "/")
