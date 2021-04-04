import os
import sys
import traceback
from datetime import datetime


class RegistryUtils():

    @staticmethod
    def report_event(type_event, report):
        print("-------------------------", type_event, "-------------------------")

        print(datetime.today(), ":")

        if isinstance(report, list):
            for item in report:
                print(item)

        else:
            print(report)

    @staticmethod
    def manage_error(data=None, error=None):
        error_type, error_value, error_traceback = sys.exc_info()

        errors_report = []

        for traceback_information in traceback.extract_tb(error_traceback):
            file_name, line_number, function_name, source = traceback_information

            if ('self' in error_traceback.tb_frame.f_locals):
                class_name = error_traceback.tb_frame.f_locals['self']

            else:
                class_name = None

            error_report = {
                    file_name: os.path.basename(file_name),
                    class_name: str(class_name),
                    function_name: function_name,
                    line_number: line_number,
                    source: source
                }

            if not error_value is None and\
                not error_value.args is None and\
                isinstance(error_value.args, list) and\
                len(error_value.args) > 0:

                error_report["exception_arguments"] = error_value.args

            errors_report.append(error_report)

        RegistryUtils.report_event("error", errors_report)

    @staticmethod
    def generate_message_error(default_message, error):
        # Summary: This method is in charge of generating an error
        # message, in case any action executed in the system has a fault.
        # parameters:
        # -default_message (String): a default message 
        # -error (string): a error type
        # return:
        # -(<message_error 'String'>): a message, whit the error of the result.
        message_error = ""

        if len(error.args) > 0:
            message_error = default_message + ": " + ", ".join(error.args)

        else:
            message_error = default_message

        return message_error

