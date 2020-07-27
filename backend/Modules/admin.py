# https://flask-admin.readthedocs.io/en/latest/
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


class VisitsView(GeneralView):
    pass


class ServicesView(GeneralView):
    form_choices = {
        'gender': [
            ('Male', 'MALE'),
            ('Female', 'FEMALE')
        ]
    }


class SalonsView(GeneralView):
    column_exclude_list = ['adress_id', 'created_at']