import connexion
from project.resources.utils.generals_utils import GeneralsUtils
from project.services.login_service import LoginService

def login():
    request_data = GeneralsUtils.get_request_body(connexion.request)
    try:
        result = LoginService().login(request_data)
    except Exception as exception:
        result = exception.args[0]
        return result
    return result

def close_session():
    try:
        result = LoginService().close_session()
    except Exception as exception:
        result = exception.args[0]
        return result   
    return result