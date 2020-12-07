from functools import wraps

from flask import Flask, request, make_response
from flask_admin import Admin
from flask_cors import CORS
from flask.json import jsonify
from flask_restful import Api, Resource

from Modules.admin import AccountAdmin, VisitsView, ServicesView, SalonsView
from Modules.user_management import (
    login,
    register_user,
    logout,
    change_password,
    session_exists,
    update_user,
    get_hairdressers_in_salon
)
from Modules.services import (create_service, update_service)
from Modules.salons import create_salon, update_salon, delete_salon, \
    get_all_salons
from Modules.visits import create_visit, update_visit, delete_visit, \
    get_available_hours, get_account_visits, get_visit_details, get_visit_details_for_edit

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
        if session_exists(session_id, account_id):
            return func(**kwargs)
        else:
            return make_response("Invalid session", 401)

    return wrapper


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
        :return: HTTP Response: 200 if the logout was successful, 400 if
        the session does not exists for the user
        """
        data = request.get_json(force=True)
        account_id = data["account_id"]
        session_id = data["session_id"]
        logout_result = logout(session_id, account_id)
        if logout_result:
            return make_response("User logged out.", 200)
        else:
            return make_response(
                "Given session does not exists for given user.", 400)


api.add_resource(AccountLogout, "/account/logout")


class Service(Resource):
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
        for_edit = request.headers.get("for_edit")
        if _id and for_edit:
            result = get_visit_details_for_edit(_id)
            return make_response(result, 200)
        elif _id and not for_edit:
            result = get_visit_details(_id)
            return make_response(result, 200)
        else:
            result = fetch_all_objects(Visits)
            return make_response(result, 200)

    def post(self):
        """
        Create a new visit based on provided data
        :return: HTTP status of the creation attempt
        """
        inputs = VisitInputs(request)
        if inputs.validate():
            visit_creation = create_visit(request)
        else:
            return make_response(str(inputs.errors), 400)

        if visit_creation["success"]:
            return make_response(visit_creation, 200)
        else:
            return make_response(visit_creation, 400)

    def patch(self):
        inputs = VisitInputs(request)
        if inputs.validate():
            visit_update = update_visit(request.get_json())
        else:
            return make_response(str(inputs.errors), 400)

        if visit_update["success"]:
            return make_response("Visit updated successfully", 200)
        else:
            return make_response(jsonify(visit_update), 400)

    def delete(self, _id):
        try:
            delete = delete_visit(_id)
            return make_response(str(delete), 200)
        except Exception as e:
            return make_response(str(e), 400)


api.add_resource(Visit, "/visit/", "/visit/<_id>")


class AccountVisits(Resource):
    def get(self, _id):
        result = get_account_visits(_id)
        return make_response(jsonify(result), 200)


api.add_resource(AccountVisits, "/accountVisits/<_id>")


class DatesAvailability(Resource):
    def post(self):
        data = request.get_json()
        result = get_available_hours(data)
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
