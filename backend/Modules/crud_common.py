import copy

from sqlalchemy.orm import Query

from models import session_scope


# READ
def convert_to_dict(query_result: Query) -> dict:
    """
    Converts a Query object returned by session.query method
    :param query_result: A query object returned by querying the database
    :return: Query object converted to a dict
    """
    converted = query_result.__dict__
    del converted['_sa_instance_state']
    result = copy.deepcopy(converted)
    return result


def get_object(object_table, object_id: str):
    """
    Gets a single object record from the database
    :param object_table: the table where the requested object resides
    :param object_id: object_id of the user that is supposed to be returned
    :return: Requested object
    """
    with session_scope() as session:
        result = session.query(object_table).filter(object_table.id == object_id).one()
        yield result


def fetch_object(object_table, object_id: str) -> dict:
    """
    Return the object as dict
    :param object_table: the table where the requested object resides
    :param object_id: account_id of the user that is supposed to be returned
    :return: Object data as dict
    """
    for obj in get_object(object_table, object_id):
        result = convert_to_dict(obj)
    return result


def all_objects_from_db(object_table):
    """
    Gets all user objects from the database
    :return: a user object
    """
    with session_scope() as session:
        for _object in session.query(object_table).all():
            yield _object


def fetch_all_objects(object_table) -> dict:
    """
    :return: list of all objects for frontend
    """
    key_name = object_table.__name__
    result = {key_name: []}

    for _object in all_objects_from_db(object_table):
        result[key_name].append(convert_to_dict(_object))
    return result


# DELETE

def delete_object(object_table, object_id: str):
    try:
        with session_scope() as session:
            deletion = session.query(object_table).filter(object_table.id == object_id)
            deletion.delete()
            session.commit()
        return True
    except Exception as e:
        print(e)
        return False
