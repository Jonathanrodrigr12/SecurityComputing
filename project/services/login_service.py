import json
from project.infrastructure.repositories.common_repository\
    import CommonRepository
from project.resources.utils.security_token import SecurityToken    
from project.resources.utils.encryption_utils import Encryption

class LoginService:
    def __init__(self):
        self.__repository_user = CommonRepository(
         entity_name="user")

    def login(self, data):
        results = {
            "data": [],
            "details": []
        }
        if "user" not in data or "password" not in data:
            results['details'].append(
                {
                    "code": "400",
                    "message": "User or password required"
                }
            )
            return results
        
        result = self.__repository_user.select(
            options={"filters":
                             [['email', "equals", data['user'].lower()]]
                             })
        if not self.validation_login(result, data['password']):
            results['details'].append(
                {
                    "key": 400,
                    "value": "User or password incorrect"
                }
            )
            return results
        if len(result)>0:
            token = SecurityToken.get_token(data['user'])
            SecurityToken.add_token(token)
            results['data'].append({
                "token": token
            })
        return results

    def validation_login(self, data, password):
        value = True
        
        if len(data)==0:
            return False
        password_validation = Encryption().decrypt_value(data[0]['password']).decode("utf-8")
        if password_validation != password:
            return False
        return value

    def close_session(self):
        result = {
            "data": [],
            "details": []
        }

        validation_token = SecurityToken().finish_token() 
        if validation_token:
            result['data'].append(
                {
                    "key": 200,
                    "value": True
                }
            )
        else:
           result['details'].append(
                {
                    "key": 400,
                    "value": False
                }
            )
        return result    