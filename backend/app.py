from functools import wraps

from flask import Flask, request, make_response
from flask_admin import Admin
from flask_cors import CORS
from flask.json import jsonify
from flask_restful import Api, Resource

from Modules.admin import AccountAdmin, VisitsView, ServicesView, SalonsView
from Modules.user_management import (
    get_hairdressers_in_salon,
    login,
    logout,
    change_password,
    register_user,
    send_password_reset_email,
    session_is_valid,
    update_user
)
from Modules.services import (create_service, update_service)
from Modules.salons import create_salon, update_salon, delete_salon, \
    get_all_salons
from Modules.visits import create_visit, update_visit, delete_visit, \
    get_available_hours, get_account_visits, get_visit_details, get_visit_details_for_edit, \
    authorized_to_access_visit

from Modules.crud_common import fetch_all_objects, fetch_object, delete_object

from models import (
    Accounts,
    Services,
    Salons,
    Visits,
    session
)
from validation import ServiceInputs, SalonInputs, VisitInputs

app = Flask(__name__)
api = Api(app)
app.secret_key = "testowy"  # TODO ogar tematu secret key i jak zrobić żeby to bylo secure
app.config['FLASK_ADMIN_SWATCH'] = 'flatly'
CORS(app)
admin = Admin(app, name="admin", template_mode="bootstrap3")
admin.add_view(AccountAdmin(Accounts, session))
admin.add_view(VisitsView(Visits, session))
admin.add_view(ServicesView(Services, session))
admin.add_view(SalonsView(Salons, session))


def verify_session(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            session_id = request.headers.get("session_id")
            account_id = request.headers.get("account_id")
        except Exception as e:
            print(e)
            return make_response("Invalid session", 401)
        if session_is_valid(session_id, account_id):
            return func(**kwargs)
        else:
            return make_response("Invalid session", 401)

    return wrapper


class Account(Resource):
    method_decorators = {"get": [verify_session], "patch": [verify_session],
                         "delete": [verify_session]}

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
            fist_name = data["first_name"]
            last_name = data["last_name"]
            account_type = data[
                "account_type"]  # TODO add mechanism for hairdresser addition
            salon_id = data["salon_id"]
        except KeyError as e:
            return make_response(
                "Not enough data provided, missing data: " + str(e), 400)
        registration = register_user(
            email, raw_password, fist_name, last_name, account_type, salon_id
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
        try:
            delete = delete_object(object_table=Accounts, object_id=_id)
            return make_response(str(delete), 200)
        except Exception as e:
            return make_response(str(e), 400)


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
                                 401 if the password was incorrect for
                                 the given email or the email is not in the db
        """
        try:
            data = request.get_json()
            raw_password = data["raw_password"]
            email = data["email"]
        except KeyError as e:
            print(e)
            return make_response("Not enough data provided" + str(e), 400)
        result = login(email=email, raw_password=raw_password)
        if result["session_id"]:
            return make_response(jsonify(result), 200)
        else:
            return make_response(jsonify(result), 401)


api.add_resource(AccountLogin, "/account/login")


class AccountResetPassword(Resource):
    def patch(self, _id=None):
        """
        Handle password change initiated by the user.
        Request without an id sends link to the given user, with token id resets the password if
        the token is still valid.
        :return: HTTP response: 200 if the change was successful, 403 otherwise.
        """
        if _id:
            data = request.get_json()
            new_password = data["new_password"]
            account_id = data["account_id"]
            password_change = change_password(account_id, new_password)
            if password_change:
                return make_response("Password changed", 200)
            else:
                return make_response("Password was not changed", 403)
        else:
            data = request.get_json()
            send_password_reset_email(data["email"])
            return make_response("Request handled successfully", 200)


api.add_resource(AccountResetPassword, "/account_reset/", "/account_reset/<_id>")


class AccountLogout(Resource):
    method_decorators = [verify_session]

    def delete(self):
        """
        Logouts the user.
        :return: HTTP Response: 200 if the logout was successful, 400 if
        the session does not exists for the user
        """
        session_id = request.headers.get("session_id")
        logout_result = logout(session_id)
        if logout_result:
            return make_response("User logged out.", 200)
        else:
            return make_response(
                "Did not manage to logout the user.", 400)


api.add_resource(AccountLogout, "/account/logout")


class Session(Resource):
    def get(self):
        account_id = request.headers.get("account_id")
        session_id = request.headers.get("session_id")
        if session_is_valid(session_id, account_id):
            return make_response("Session is valid", 200)
        else:
            return make_response("Invalid session", 401)


api.add_resource(Session, "/session/")


class Service(Resource):
    method_decorators = {"get": [verify_session]}

    def get(self, _id=None):
        if _id:
            result = fetch_object(Services, _id)
            return make_response(result, 200)
        else:
            result = fetch_all_objects(Services)
            return make_response(result, 200)

    def post(self):
        """
        Create a new service based on provided data
        :return: HTTP status of the creation attempt
        """
        data = request.get_json()
        inputs = ServiceInputs(request)
        if inputs.validate():
            service_creation = create_service(data)
        else:
            return make_response(str(inputs.errors), 400)
        if service_creation["success"]:
            return make_response("Service creation was successful", 200)
        else:
            return make_response(jsonify(service_creation), 400)

    def patch(self):
        inputs = ServiceInputs(request)
        if inputs.validate():
            result = update_service(request.get_json())
        else:
            return make_response(str(inputs.errors), 422)
        if result:
            return make_response(str(result), 200)
        else:
            return make_response(str(result), 400)

    def delete(self, _id):
        try:
            delete = delete_object(object_table=Services, object_id=_id)
            return make_response(str(delete), 200)
        except Exception as e:
            return make_response(str(e), 400)


api.add_resource(Service, "/service/", "/service/<_id>")


class Salon(Resource):
    def get(self, _id=None):
        if _id:
            result = fetch_object(Salons, _id)
            return make_response(result, 200)
        else:
            result = get_all_salons()
            return make_response(result, 200)

    def post(self):
        """
        Create a new salon based on provided data
        :return: HTTP status of the creation attempt
        """
        inputs = SalonInputs(request)
        if inputs.validate():
            salon_creation = create_salon(request.get_json())
        else:
            return make_response(str(inputs.errors), 400)

        if salon_creation["success"]:
            return make_response("Salon created successfully", 200)
        else:
            return make_response(jsonify(salon_creation), 400)

    def patch(self):
        inputs = SalonInputs(request)
        if inputs.validate():
            result = update_salon(request.get_json())
        else:
            return make_response(str(inputs.errors), 422)
        if result:
            return make_response(str(result), 200)
        else:
            return make_response(str(result), 400)

    def delete(self, _id):
        try:
            delete = delete_salon(_id)
            return make_response(str(delete), 200)
        except Exception as e:
            return make_response(str(e), 400)


api.add_resource(Salon, "/salon/", "/salon/<_id>")


class Visit(Resource):
    method_decorators = [verify_session]

    def get(self, _id=None):
        if authorized_to_access_visit(_id, request.headers.get("account_id")):
            for_edit = request.headers.get("for_edit")
            if _id and for_edit:
                result = get_visit_details_for_edit(_id)
                return make_response(result, 200)
            elif _id and not for_edit:
                result = get_visit_details(_id)
                return make_response(result, 200)
            else:
                return make_response("No visit id provided", 400)
        else:
            return make_response("User not authorized to see this visit", 401)

    def post(self):
        """
        Create a new visit based on provided data
        :return: HTTP status of the creation attempt
        """
        inputs = VisitInputs(request)
        if inputs.validate():
            data = request.get_json()
            visit_creation = create_visit(data, request.headers.get("account_id"))
        else:
            return make_response(str(inputs.errors), 400)

        if visit_creation["success"]:
            return make_response(visit_creation, 200)
        else:
            return make_response(visit_creation, 400)

    def patch(self):
        if authorized_to_access_visit(request.data.get("id"), request.headers.get("account_id")):
            inputs = VisitInputs(request)
            if inputs.validate():
                data = request.get_json()
                visit_update = update_visit(data)
            else:
                return make_response(str(inputs.errors), 400)

            if visit_update["success"]:
                return make_response("Visit updated successfully", 200)
            else:
                return make_response(jsonify(visit_update), 400)
        else:
            return make_response("User not authorized to edit this visit", 401)

    def delete(self, _id):
        if authorized_to_access_visit(_id, request.headers.get("account_id")):
            try:
                delete = delete_visit(_id)
                return make_response(str(delete), 200)
            except Exception as e:
                return make_response(str(e), 400)
        else:
            return make_response("User not authorized to delete this visit", 401)


api.add_resource(Visit, "/visit/", "/visit/<_id>")


class AccountVisits(Resource):
    method_decorators = [verify_session]

    def get(self):
        result = get_account_visits(request.headers.get("account_id"))
        return make_response(jsonify(result), 200)


api.add_resource(AccountVisits, "/accountVisits/")


class DatesAvailability(Resource):
    method_decorators = [verify_session]

    def post(self):
        data = request.get_json()
        result = get_available_hours(data, request.headers.get("account_id"))
        return make_response(jsonify(result), 200)


api.add_resource(DatesAvailability, "/visit/availability/")


class Hairdresser(Resource):
    def get(self, _id=None):
        """Finds all hairdressers for a given salon_id"""
        if _id:
            hairdressers = get_hairdressers_in_salon(_id)
            return make_response(jsonify(hairdressers), 200)


api.add_resource(Hairdresser, "/hairdresser/", "/hairdresser/<_id>")


class Main(Resource):
    def get(self):
        return make_response("True", 200)


api.add_resource(Main, "/")
