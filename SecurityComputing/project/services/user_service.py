import datetime
from project.infrastructure.repositories.common_repository\
    import CommonRepository
from project.resources.utils.encryption_utils import Encryption
from project.resources.utils.security_token import SecurityToken
from project.models.enum.keys_enum import Keys

class UserService():

    def __init__(self):
        self.__repository_user = CommonRepository(
         entity_name="user")

    def create_user(self, data):
        result = {
            "data": [],
            "details": []
        }
 
        data_email = self.validation_email(data)

        if len(data_email['details'])>0:
            return data_email

        data = self.complete_data(data)
        try:
            data = self.__repository_user.insert(data)
        except Exception as ex:
            result['details'].append(
                {
                    "key": 400,
                    "value": "Error create user "+ ex
                }
            )
            return result
        
        if data:
           result['data'].append(
                {
                    "key": "200",
                    "value": "User create"
                }
            )
        else:
            result['details'].append(
                {
                    "key": "400",
                    "value": "User not create "
                }
            )
        return result
    #region ValidationData
    def complete_data(self, data):
        if 'password' in data:
            data['password'] = Encryption().encrypt_value(data['password']).decode("utf-8")
        if 'email' in data:
            data['email'] = data['email'].lower() 
        return data

    def verify_data(self, data):
        data = self.__repository_user.select(
            options={"filters":
                             [['email', "equals", data]]
                             }) 
        return (True, data) if len(data) > 0 else (False, data)
    
    def validation_email(self, data):
        result = {
            "data": [],
            "details": []
        }

        if self.verify_data(data['email'])[0]:
            result['details'].append(
                {
                    "key": 400,
                    "value": "this email is in use"
                }
            )

        return result

    def validation_email_update(self, data):
        result = {
            "data": [],
            "details": []
        }
        if 'email' in data:
            result_data = self.verify_data(data['email'])
            if result_data[0] and result_data[1][0]['id'] != data['id']:
                result['details'].append(
                    {
                        "key": 400,
                        "value": "Este correo se encuentra en uso"
                    }
                )

        return result

    #endregion