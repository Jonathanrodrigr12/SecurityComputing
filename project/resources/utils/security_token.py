import jwt
import datetime
from project.configuration_manager import ConfigurationManger
from flask import request
from project.infrastructure.repositories.common_repository\
    import CommonRepository

class SecurityToken:
    @staticmethod
    def get_key():
        return ConfigurationManger.get_config("PRIVATE_KEY")

    @staticmethod
    def get_algorithms():
        return ConfigurationManger.get_config("ALGORITHMS")

    @staticmethod
    def get_token(value,expiration=28800):
        return jwt.encode({'exp': datetime.datetime.utcnow() + datetime.timedelta(seconds=expiration), 'val': value}, 
                          SecurityToken.get_key()).decode("utf-8")

    @staticmethod
    def validate_token(token=None):
        token_passed = request.headers['Token'] if 'Token' in request.headers else None
        token_passed = token or token_passed
        if token_passed is not None:
            try:
                data = jwt.decode(token_passed,SecurityToken.get_key(),
                            algorithm=SecurityToken.get_algorithms())
                return (True, token_passed, data['val'])
            except jwt.exceptions.ExpiredSignatureError:
                return (False, 400, '', token_passed)
            except Exception as e:
                return (False, 400, e, token_passed)
        return (False, 400, '', token_passed)
    
    @staticmethod
    def add_token(token, token_new=None):
        data = {
            'token': token,
            'active': True
        }
    
        repository_security = CommonRepository(
         entity_name="security")
        
        if token_new is None:
            repository_security.insert(data)
        else:
            result = repository_security.select(
            options={"filters":
                             [['token', "equals", data['token']]]
                             })
            data['token'] = token_new
            repository_security.update(result[0]['id'], data)

    @staticmethod
    def finish_token():
        token = request.headers['Token'] if 'Token' in request.headers else None
        repository_security = CommonRepository(
         entity_name="security")
        result = repository_security.select(
            options={"filters":
                             [['token', "equals", token]]
                             })
        return repository_security.delete(result[0]['id']) if len(result) > 0 else False

    @staticmethod
    def verify_exist_token(token_new=None):
        token = request.headers['Token'] if 'Token' in request.headers else None
        token = token_new or token
        repository_security = CommonRepository(
         entity_name="security")
        result = repository_security.select(
            options={"filters":
                             [['token', "equals", token]]
                             })
        return result[0]['active'] if len(result) > 0 else False
    