import connexion
from project.resources.utils.generals_utils import GeneralsUtils
from project.services.user_service import UserService

def create_user():
    request_data = GeneralsUtils.get_request_body(connexion.request)
    try:
        result = UserService().create_user(request_data)
    except Exception as exception:
        result = exception.args[0]
        return result
    return result