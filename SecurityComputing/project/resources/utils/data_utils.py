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

    @staticmethod
    def calulate_date_stage(stage, type_planting):
        start = 0
        end = 0
        if stage == Stage.stage_two.value:
           start = DateStage.stage_two_start.value
           end = DateStage.stage_two_end.value
        elif stage == Stage.stage_three.value and type_planting == TypePlanting.riego.value:
           start = DateStage.stage_three_start_riego.value
           end = DateStage.stage_three_end_riego.value
        elif stage == Stage.stage_three.value or stage == Stage.stage_four.value:
           start = DateStage.stage_three_start.value
           end = DateStage.stage_three_end.value
        elif stage == Stage.stage_five.value and type_planting == TypePlanting.riego.value:
            start = DateStage.stage_five_start_riego.value
            end = DateStage.stage_five_end_riego.value
        elif stage == Stage.stage_five.value and type_planting == TypePlanting.secano.value:
            start = DateStage.stage_five_start_secano.value
            end = DateStage.stage_five_end_secano.value 
        elif stage == Stage.stage_six.value and type_planting == TypePlanting.secano.value:
            start = DateStage.stage_six_start_secano.value
            end = DateStage.stage_six_end_secano.value
        elif stage == Stage.stage_six.value and type_planting == TypePlanting.riego.value:
            start = DateStage.stage_six_start_riego.value
            end = DateStage.stage_six_end_riego.value  
        elif stage == Stage.stage_seven.value and type_planting == TypePlanting.secano.value:
            start = DateStage.stage_seven_start_secano.value
            end = DateStage.stage_seven_end_secano.value
        elif stage == Stage.stage_seven.value and type_planting == TypePlanting.riego.value:
            start = DateStage.stage_seven_start_riego.value
            end = DateStage.stage_seven_end_riego.value 
        elif stage == Stage.stage_eight.value and type_planting == TypePlanting.riego.value:
            start = DateStage.stage_eight_start_riego.value
            end = DateStage.stage_eight_end_riego.value
        elif stage == Stage.stage_eight.value and type_planting == TypePlanting.secano.value:
            start = DateStage.stage_eight_start_secano.value
            end = DateStage.stage_eight_end_secano.value
        elif stage == Stage.stage_nine.value and type_planting == TypePlanting.riego.value:
            start = DateStage.stage_nine_start_riego.value
            end = DateStage.stage_nine_end_riego.value
        elif stage == Stage.stage_nine.value and type_planting == TypePlanting.secano.value:
            start = DateStage.stage_nine_start_secano.value
            end = DateStage.stage_nine_end_secano.value
        elif stage == Stage.stage_ten.value and type_planting == TypePlanting.riego.value:
            start = DateStage.stage_ten_start_riego.value
            end = DateStage.stage_ten_end_riego.value
        elif stage == Stage.stage_ten.value and type_planting == TypePlanting.secano.value:
            start = DateStage.stage_ten_start_secano.value
            end = DateStage.stage_ten_end_secano.value 
        elif stage == Stage.stage_eleven.value and type_planting == TypePlanting.riego.value:
            start = DateStage.stage_eleven_start_riego.value
            end = DateStage.stage_eleven_end_riego.value
        elif stage == Stage.stage_eleven.value and type_planting == TypePlanting.secano.value:
            start = DateStage.stage_eleven_start_secano.value
            end = DateStage.stage_eleven_end_secano.value  
        elif stage == Stage.stage_twelve.value and type_planting == TypePlanting.riego.value:
            start = DateStage.stage_twelve_start_riego.value
            end = DateStage.stage_twelve_end_riego.value
        elif stage == Stage.stage_twelve.value and type_planting == TypePlanting.secano.value:
            start = DateStage.stage_twelve_start_secano.value
            end = DateStage.stage_twelve_end_secano.value 
        elif stage == Stage.stage_thirteen.value and type_planting == TypePlanting.riego.value:
            start = DateStage.stage_thirteen_start_riego.value
            end = DateStage.stage_thirteen_end_riego.value
        elif stage == Stage.stage_thirteen.value and type_planting == TypePlanting.secano.value:
            start = DateStage.stage_thirteen_start_secano.value
            end = DateStage.stage_thirteen_end_secano.value 
        elif stage == Stage.stage_fourteen.value and type_planting == TypePlanting.riego.value:
            start = DateStage.stage_fourteen_start_riego.value
            end = DateStage.stage_fourteen_end_riego.value
        elif stage == Stage.stage_fourteen.value and type_planting == TypePlanting.secano.value:
            start = DateStage.stage_fourteen_start_secano.value
            end = DateStage.stage_fourteen_end_secano.value 
        elif stage == Stage.stage_fifteen.value:
            start = DateStage.stage_fifteen_start.value
            end = DateStage.stage_fifteen_end.value      
        return (start, end)