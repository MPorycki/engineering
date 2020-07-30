# https://flask-admin.readthedocs.io/en/latest/
import datetime
import uuid

from flask_admin.contrib.sqla import ModelView



class GeneralView(ModelView):
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

    def on_model_change(self, form, model, is_created): # TODO a co z haslem
        if is_created:
            model.id = uuid.uuid4().hex
            model.created_at = datetime.datetime.utcnow()


class VisitsView(GeneralView):
    def on_model_change(self, form, model, is_created):
        if is_created:
            model.id = uuid.uuid4().hex
            model.created_at = datetime.datetime.utcnow()


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