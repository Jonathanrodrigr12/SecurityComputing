import base64
import json
import os

from datetime import datetime
from flask import g


class GeneralsUtils:

    @staticmethod
    def generate_key(key, prefix=None):
        """ method to convert parameters into key """
        result = None
        if isinstance(key, (int, float)):
            key = str(key)

        if not GeneralsUtils.validate_string(key):
            raise TypeError("The 'key' parameter is not the correct type")

        if prefix is not None and not GeneralsUtils.validate_string(prefix):
            raise TypeError("The 'prefix' parameter is not the correct type")

        if prefix is not None:
            key = f"{prefix} {key}"

        key_splited = key.split()
        result = ("_".join(key_splited)).lower()

        return result

    @staticmethod
    def encode_data(data):
        """ convert information to base64 """
        data_bytes = data.encode("ascii")
        data_encoded = base64.b64encode(data_bytes)
        return data_encoded

    @staticmethod
    def decode_data(data):
        """ decode base64 information """
        return base64.b64decode(data).decode('utf-8')

    @staticmethod
    def delete_column(dictionary_list, key):
        if not isinstance(dictionary_list, list):
            raise Exception

        if not all(isinstance(item, dict)  for item in dictionary_list):
            raise Exception

        if not GeneralsUtils.validate_string(key):
            raise Exception

        for dictionary in dictionary_list:
            if key in dictionary:
                del dictionary[key]

        return dictionary_list

    @staticmethod
    def get_global_data(key):
        if not GeneralsUtils.validate_string(key):
            raise Exception

        if key not in g:
            return None

        return g.get(key)

    @staticmethod
    def get_request_body(request):
        result = None

        if not GeneralsUtils.validate_attribute("json", request, dict):
            data = request.data
            if isinstance(data, bytes) or\
                isinstance(data, str):
                result = json.loads(data)
            elif isinstance(data, dict):
                result = json.loads(data)
            elif isinstance(request.form, dict):
                result = request.form

        return result

    @staticmethod
    def read_file(path, output_type="json"):
        # T
        OUTPUT_TYPES = ("json", "text")

        if not GeneralsUtils.validate_string(path):
            raise Exception

        if not os.path.isfile(path):
            raise Exception

        if not GeneralsUtils.\
            validate_attribute(output_type, OUTPUT_TYPES, str):
            raise Exception

        with open(path, "r") as text_file:
            if output_type == "json":
                result = json.load(text_file)
            if output_type == "text":
                result = text_file

        return result

    @staticmethod
    def set_global_data(key, value):
        if not GeneralsUtils.validate_string(key):
            raise Exception

        setattr(g, key, value)

    @staticmethod
    def validate_attribute(attribute_name, structure, types_attributes_allowed=None):
        result = False

        if not GeneralsUtils.validate_string(attribute_name) or\
           not isinstance(structure, (dict, tuple, list)) or\
           attribute_name not in structure:
            return False

        if types_attributes_allowed is None:
            result = True

        elif isinstance(types_attributes_allowed, type) or\
                (
                    isinstance(types_attributes_allowed, tuple) and
                    all(isinstance(type_attribute_allowed, type)
                        for type_attribute_allowed in types_attributes_allowed)
                ):

            if isinstance(structure, dict):
                attribute = structure[attribute_name]
            else:
                attribute = next(item for item in structure if attribute_name == item)

            if isinstance(attribute, types_attributes_allowed):
                result = True

        else:
            return False

        return result

    @staticmethod
    def validate_string(value):
        if not isinstance(value, str):
            return False

        if str.strip(value) == "":
            return False

        return True

    @staticmethod
    def get_datetime():
        result = datetime.today().isoformat()

        return result

    @staticmethod
    def try_parse_date_time(value):
        """Mehtod try parse string to date"""
        DATE_TIME_FORMATS = (
            '%Y-%m-%dT%H:%M:%SZ',
            '%Y-%m-%dT%H:%M:%S.%fZ',
            '%Y-%m-%d %H:%M:%SZ',
            '%Y-%m-%d %H:%M:%S.%fZ',
            '%Y-%m-%dT%H:%M:%S',
            '%Y-%m-%dT%H:%M:%S.%f',
            '%Y-%m-%d %H:%M:%S',
            '%Y-%m-%d %H:%M:%S.%f')

        if value == "":
            return ''
        for date_time_format in DATE_TIME_FORMATS:
            try:
                return datetime.strptime(value, date_time_format)

            except ValueError:
                pass

        raise ValueError('no valid date format found')