# encoding: utf-8
import os

from flask import current_app

from project.resources.utils.generals_utils import GeneralsUtils


class ConfigurationManger():

    CONFIG_CONNECTIONS_STRINGS_KEY = "CONNECTIONS_STRINGS"

    @staticmethod
    def get_connection_string(connection_string_name):
        if connection_string_name in os.environ:
            return os.environ[connection_string_name]

        connection_string =\
            GeneralsUtils.get_global_data(connection_string_name)

        if connection_string is None:
            connections_strings = ConfigurationManger.\
               get_config(ConfigurationManger.CONFIG_CONNECTIONS_STRINGS_KEY)
            if not GeneralsUtils.\
               validate_attribute(connection_string_name,
                                  connections_strings):
                raise Exception("ConfigurationManger.get_connection_string "
                                + "error. connection_string_name: "
                                + connection_string_name)

        connection_string = connections_strings[connection_string_name]

        return connection_string

    @staticmethod
    def get_config(key):
        if key in os.environ:
            return os.environ[key]

        if not GeneralsUtils.validate_attribute(key, current_app.config):
            raise Exception("ConfigurationManger.get_config error. Key: "
                            + key)

        return current_app.config[key]
