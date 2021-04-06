from flask import current_app, g
from project.models.enum.stage_enum import Stage
from project.models.enum.date_stage_enum import DateStage
from project.resources.utils.generals_utils import GeneralsUtils
from project.models.enum.type_planting_enum import TypePlanting

class DataUtils():

    @staticmethod
    def get_configuration_setting(key):
        if not GeneralsUtils.validate_attribute(key, current_app.config):
            raise Exception

        return current_app.config[key]

    @staticmethod
    def set_global_data(key, value):
        if not GeneralsUtils.validate_string(key):
            raise Exception

        setattr(g, key, value)

    @staticmethod    
    def get_global_data(key):
        if not GeneralsUtils.validate_string(key):
            raise Exception

        if key not in g:
            return None

        return g.get(key)