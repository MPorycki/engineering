# https://flask-admin.readthedocs.io/en/latest/
import datetime
import uuid

from flask_admin.contrib.sqla import ModelView
from flask_admin.form import SecureForm

from Modules.user_management import send_pass_reset_email
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
            ('customer', 'customer'),
            ('admin', 'admin')
        ]
    }

    form_excluded_columns = ['hashed_password', 'created_at']

    def on_model_change(self, form, model, is_created):
        if is_created:
            model.id = uuid.uuid4().hex
            model.created_at = datetime.datetime.utcnow()

    def after_model_change(self, form, model, is_created):
        if is_created:
            send_pass_reset_email(model.email)


class VisitsView(GeneralView):
    can_create = False

    def after_model_delete(self, model):
        delete_visit_services(model.id)


class ServicesView(GeneralView):
    form_choices = {
        'gender': [
            ('Male', 'MALE'),
            ('Female', 'FEMALE')
        ]
    }

    def on_model_change(self, form, model, is_created):
        if is_created:
            model.id = uuid.uuid4().hex
            model.created_at = datetime.datetime.utcnow()


class SalonsView(GeneralView):
    column_exclude_list = ['adress_id', 'created_at']

    def on_model_change(self, form, model, is_created):
        if is_created:
            model.id = uuid.uuid4().hex
            model.created_at = datetime.datetime.utcnow()
