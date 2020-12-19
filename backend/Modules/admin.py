# https://flask-admin.readthedocs.io/en/latest/
import datetime
import uuid

from flask import request, redirect
from flask_admin.contrib.sqla import ModelView
from flask_admin.form import SecureForm

from Modules.user_management import send_password_reset_email, can_access_admin
from Modules.visits import delete_visit_services


class GeneralView(ModelView):
    # CSRF Protection
    form_base_class = SecureForm

    can_view_details = True
    create_modal = True
    edit_modal = True


class AccountAdmin(GeneralView):
    column_exclude_list = ['hashed_password', ]
    form_choices = {
        'account_type': [
            ('hairdresser', 'hairdresser'),
            ('customer', 'customer')
        ]
    }

    form_excluded_columns = ['hashed_password', 'created_at']

    column_details_exclude_list = ['hashed_password']

    def on_model_change(self, form, model, is_created):
        if is_created:
            model.id = uuid.uuid4().hex
            model.created_at = datetime.datetime.utcnow()

    def after_model_change(self, form, model, is_created):
        if is_created:
            send_password_reset_email(model.email)

    def is_accessible(self):
        return can_access_admin(request.cookies.get("session-id"), request.cookies.get("user-id"))

    def inaccessible_callback(self, name, **kwargs):
        return redirect("http://localhost:8080/#/")


class VisitsView(GeneralView):
    can_create = False

    def after_model_delete(self, model):
        delete_visit_services(model.id)

    def is_accessible(self):
        return can_access_admin(request.cookies.get("session-id"), request.cookies.get("user-id"))

    def inaccessible_callback(self, name, **kwargs):
        return redirect("http://localhost:8080/#/")


class ServicesView(GeneralView):
    form_choices = {
        'gender': [
            ('Male', 'MALE'),
            ('Female', 'FEMALE')
        ]
    }

    form_excluded_columns = ['created_at']

    def on_model_change(self, form, model, is_created):
        if is_created:
            model.id = uuid.uuid4().hex
            model.created_at = datetime.datetime.utcnow()

    def is_accessible(self):
        return can_access_admin(request.cookies.get("session-id"), request.cookies.get("user-id"))

    def inaccessible_callback(self, name, **kwargs):
        return redirect("http://localhost:8080/#/")


class SalonsView(GeneralView):
    column_exclude_list = ['created_at']

    def on_model_change(self, form, model, is_created):
        if is_created:
            model.id = uuid.uuid4().hex
            model.created_at = datetime.datetime.utcnow()

    def is_accessible(self):
        return can_access_admin(request.cookies.get("session-id"), request.cookies.get("user-id"))

    def inaccessible_callback(self, name, **kwargs):
        return redirect("http://localhost:8080/#/")
