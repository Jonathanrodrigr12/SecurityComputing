from cryptography.fernet import Fernet
from project.configuration_manager import ConfigurationManger
from project.models.models import TransactionResult
from project.resources.utils.generals_utils import GeneralsUtils


class Encryption():

    @staticmethod
    def get_key():
        return ConfigurationManger.get_config("KEY_PRIVATE")

    @staticmethod
    def encrypt_value(ciphertext):
        """ Method encrypt values """
        transaction_result = TransactionResult("EncryptValue", None)
        try:
            transaction_result.process = "logtopology"
            transaction_result.action = "Encrypt"
            transaction_result.datestamp_process = GeneralsUtils.get_datetime()
            key = Encryption.get_key().encode()
            data = ciphertext.encode()
            fernet = Fernet(key)
            value_encrypt = fernet.encrypt(data)
        except Exception as exception:
            transaction_result.result = "Failed"
            transaction_result.message = "Encrypt Values Failed" +\
                                         exception.args[0]
        transaction_result.message = "Encrypt Values Successfully"
        return value_encrypt
    
    @staticmethod
    def decrypt_value(ciphertext):
        """ Method encrypt values """
        transaction_result = TransactionResult("EncryptValue", None)
        try:
            transaction_result.process = "logtopology"
            transaction_result.action = "Encrypt"
            transaction_result.datestamp_process = GeneralsUtils.get_datetime()
            key = Encryption.get_key().encode()
            data = ciphertext.encode()
            fernet = Fernet(key)
            value_encrypt = fernet.decrypt(data)
        except Exception as exception:
            transaction_result.result = "Failed"
            transaction_result.message = "Encrypt Values Failed" +\
                                         exception.args[0]
        transaction_result.message = "Encrypt Values Successfully"
        return value_encrypt