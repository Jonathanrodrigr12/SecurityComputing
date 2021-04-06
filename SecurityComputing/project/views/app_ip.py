import connexion
from project.resources.utils.generals_utils import GeneralsUtils
from project.services.app_ip_service import AppIpService

def get_ip(ip):
    try:
        result = AppIpService().get_app_ip(ip)
    except Exception as exception:
        result = exception.args[0]
        return result
    return result

def get_country(name):
    try:
        result = AppIpService().get_country(name)
    except Exception as exception:
        result = exception.args[0]
        return result
    return result
