import operator

from datetime import datetime
from sqlalchemy import MetaData, Table, Column, func, select, Boolean, DateTime, Float, Integer, JSON, String, or_, and_
from sqlalchemy.sql.operators import ColumnOperators

from project.configuration_manager import ConfigurationManger
from project.resources.utils.entity_utils import EntityUtils
from project.resources.utils.generals_utils import GeneralsUtils


class SqlalchemyUtils():

    # T
    schema_types_by_sqlalchemy_functions = {
        "boolean": Boolean,
        "dateTime": DateTime,
        "integer": Integer,
        "number": Float,
        "object": JSON,
        "string": String
    }

    # T
    string_to_operator_number = {
        "=": operator.eq,
        "==": operator.eq,
        "equals": operator.eq,
        "eq": operator.eq,

        "<>": operator.ne,
        "!=": operator.ne,
        "ne": operator.ne,

        "<": operator.lt,
        "lt": operator.lt,

        ">": operator.gt,
        "gt": operator.gt,

        "<=": operator.le,
        "le": operator.le,

        ">=": operator.ge,
        "ge": operator.ge,
    }

    # T
    string_to_operator_string = {
        "=": "like",
        "==": "like",
        "equals": "like",
        "eq": "like",

        "contains": "contains",

        "startswith": "startswith",

        "endswith": "endswith"
    }

    # T
    string_to_operator_boolean = {
        "=": operator.eq,
        "==": operator.eq,
        "equals": operator.eq,
        "eq": operator.eq,
    }

    # T
    string_to_operator_datetime = {
        "=": operator.eq,
        "==": operator.eq,
        "equals": operator.eq,
        "eq": operator.eq,

        "<>": operator.ne,
        "!=": operator.ne,
        "ne": operator.ne,

        "<": operator.lt,
        "lt": operator.lt,

        ">": operator.gt,
        "gt": operator.gt,

        "<=": operator.le,
        "le": operator.le,

        ">=": operator.ge,
        "ge": operator.ge,
    }

    @staticmethod
    def configure_table(entity_name, meta_data):
        fail = False
 
        if not GeneralsUtils.validate_string(entity_name) or\
            not isinstance(meta_data, MetaData):
            raise Exception

        table_definitions = EntityUtils.get_entity_definitions(entity_name)

        if "tableName" not in table_definitions:
            raise Exception

        table_sqlalchemy = Table(table_definitions["tableName"], meta_data)

        if not GeneralsUtils.validate_attribute("properties", table_definitions, dict):
            raise Exception

        if not GeneralsUtils.validate_attribute("primaryKey", table_definitions):
            table_definitions["primaryKey"] = []

        if not GeneralsUtils.validate_attribute("uniques", table_definitions):
            table_definitions["uniques"] = []

        for item_key, item_value  in table_definitions["properties"].items():
            if "type" not in item_value or\
               not GeneralsUtils.\
                    validate_attribute(item_value["type"],
                                       SqlalchemyUtils.\
                                                        schema_types_by_sqlalchemy_functions):
                fail = True
                break

            if  item_key in table_definitions["primaryKey"]:
                item_value["primaryKey"] = True

            else:
                item_value["primaryKey"] = False

            if  item_key in table_definitions["uniques"]:
                item_value["unique"] = True

            else:
                item_value["unique"] = False

            column_sqlalchemy = Column(
                item_value["dbName"],
                SqlalchemyUtils.schema_types_by_sqlalchemy_functions[item_value["type"]],
                primary_key=item_value["primaryKey"],
                unique=item_value["unique"])

            table_sqlalchemy.append_column(column_sqlalchemy)

        if fail:
            raise Exception("")

        return table_sqlalchemy

    @staticmethod
    def generate_select_statement(entity_name, table_sqlalchemy, options):
        statement = table_sqlalchemy.select()
        fail = False
        error_detected = None
        message_error = None
 
        if not isinstance(table_sqlalchemy, Table) or\
           not isinstance(options, dict):
            raise Exception

        if not isinstance(entity_name, str):
            raise Exception("The entity name has not been configured")

        entity_definitions = EntityUtils.get_entity_definitions(entity_name)

        if "group_by" in options:
            group_by_attributes = options["group_by"]

            if not GeneralsUtils.validate_attribute("column_name", group_by_attributes, str):
                raise Exception("")

            column_db_name = EntityUtils.translate_attribute_name(
                entity_definitions=entity_definitions,
                property_name=group_by_attributes["column_name"])

            column_sqlalchemy = getattr(table_sqlalchemy.columns,
                                        column_db_name)

            statement = select([column_sqlalchemy, func.count(column_sqlalchemy)]).group_by(column_sqlalchemy)

        if "distinct_column_name" in options:
            column_name = options["distinct_column_name"]

            if not GeneralsUtils.validate_string(column_name):
                raise Exception("")

            if not column_name in entity_definitions["properties"]:
                raise Exception("")

            column_db_name = EntityUtils.translate_attribute_name(
                entity_definitions=entity_definitions,
                property_name=column_name)

            statement = statement.distinct(column_db_name)

        if "filters" in options:
            filters = options["filters"]
            fail = False
            if not isinstance(filters, list):
                raise Exception

            if len(filters) == 3 and\
               GeneralsUtils.validate_string(filters[0]) and\
               isinstance(filters[2], (str, int, float, bool, datetime)):
                filters = [filters]

            properties = entity_definitions["properties"]

            and_filters = []
            or_filters = []
            filter_list = []
            filter_default = []
            len_filters = len(filters) - 1
            index = 0

            for filter_item in filters[::2]:
                if not isinstance(filter_item, list) or\
                   not len(filter_item) == 3 and\
                   not (GeneralsUtils.validate_string(filter_item[0]) and
                        isinstance(filter_item[1], str)):
                    fail = True
                    message_error = "Filter parameters are poorly formed"
                    break

                if len_filters == 0:
                    filter_list = filter_default

                elif index < len_filters:
                    if filters[index + 1] == "or":
                        filter_list = or_filters

                    elif filters[index + 1] == "and":
                        filter_list = and_filters
                    else:
                        fail = True
                        message_error = "Unidentified logical operator"
                        break

                index = index + 2

                try:
                    if properties[filter_item[0]]["type"] == "dateTime":
                        filter_item[2] = datetime.strptime(filter_item[2], "%Y-%m-%dT%H:%M:%SZ")

                except Exception as error:
                    fail = True
                    error_detected = error
                    message_error = "Error converting a dateTime type value" 
                    break

                try:
                    attribute_name = EntityUtils.translate_attribute_name(
                        entity_definitions=entity_definitions,
                        property_name=filter_item[0])
                    column_sqlalchemy = getattr(table_sqlalchemy.columns,
                                                attribute_name)

                except Exception as error:
                    fail = True
                    error_detected = error
                    message_error = "Error getting column from sqlalchemy table"
                    break

                try:
                    string_to_operator = {}
                    if isinstance(filter_item[2], str) or\
                       isinstance(filter_item[2], tuple):
                        string_to_operator = SqlalchemyUtils.string_to_operator_string
                        if (filter_item[1] == "=" or
                            filter_item[1] == "==" or
                            filter_item[1] == "equals" or
                            filter_item[1] == "eq"):
                            filter_list.append(column_sqlalchemy.like(filter_item[2]))

                        elif filter_item[1] == "contains":
                            filter_list.append(column_sqlalchemy.contains(filter_item[2]))

                        elif filter_item[1] == "startswith":
                            filter_list.append(column_sqlalchemy.startswith(filter_item[2]))

                        elif filter_item[1] == "endswith":
                            filter_list.append(column_sqlalchemy.endswith(filter_item[2]))

                        elif filter_item[1] == "in":
                            filter_list.append(column_sqlalchemy.in_(filter_item[2]))
                        else:
                            message_error = "The operator configured for the filter was not recognized"
                            fail = True
                            break

                        continue

                    elif isinstance(filter_item[2], (int, float)):
                        string_to_operator = SqlalchemyUtils.string_to_operator_number

                    elif isinstance(filter_item[2], bool):
                        string_to_operator = SqlalchemyUtils.string_to_operator_boolean

                    elif isinstance(filter_item[2], datetime):
                        string_to_operator = SqlalchemyUtils.string_to_operator_datetime

                    else:
                        message_error = "Unsupported filter type"
                        fail = True
                        break

                    filter_list.append(string_to_operator[filter_item[1]](column_sqlalchemy, filter_item[2]))

                except Exception as error:
                    error_detected = error
                    message_error = "Filter setting error"
                    fail = True
                    break

                if fail:
                    raise Exception("", message_error, error_detected)

            if len(and_filters) > 0 and len(or_filters) > 0:
                statement = statement.where(or_(and_(*and_filters), or_(*or_filters)))

            elif len(and_filters) > 0:
                statement = statement.where(and_(*and_filters))

            elif len(or_filters) > 0:
                statement = statement.where(or_(*or_filters))

            elif len(filter_list) > 0 and len(and_filters) == 0 and len(or_filters) == 0:
                statement = statement.where(*filter_list)

        if "order_by" in options:
            order_by_items = options["order_by"]
            message_error = ""
            fail = False

            if isinstance(order_by_items, dict):
                order_by_items = [order_by_items]

            if not isinstance(order_by_items, list):
                raise Exception("")

            for order_by_item in order_by_items:
                if not GeneralsUtils.\
                    validate_attribute("column_name", order_by_item, str):
                    error_detected = "'Column name' not present in 'order by' parameters"
                    fail = True
                    break

                try:
                    column_sqlalchemy = getattr(
                        table_sqlalchemy.columns,
                        EntityUtils.translate_attribute_name(
                            entity_definitions=entity_definitions,
                            property_name=order_by_item["column_name"]))

                except Exception as error:
                    error_detected = error
                    message_error = ""
                    fail = True
                    break

                if not GeneralsUtils.\
                   validate_attribute("desc", order_by_item):
                    statement = statement.order_by(column_sqlalchemy.asc())
                    break

                if not isinstance(order_by_item["desc"], bool):
                    message_error = ""
                    fail = True
                    break

                if order_by_item["desc"]:
                    statement = statement.order_by(column_sqlalchemy.desc())

                else:
                    statement = statement.order_by(column_sqlalchemy.asc())

            if fail:
                raise Exception("", message_error, error_detected)

        if  "paginate" in options:
            options_paginate = options["paginate"]
            if not GeneralsUtils.\
                   validate_attribute("offset", options_paginate, int) or\
               not GeneralsUtils.\
                   validate_attribute("limit", options_paginate, int) or\
               options["paginate"]["offset"] < 0 or\
               options["paginate"]["limit"] < 1:
                raise Exception("")

            statement = statement.limit(
                options["paginate"]["limit"]).\
                offset(options["paginate"]["offset"])

        return statement

    @staticmethod
    def generate_where_statement(entity_name,
                                 options,
                                 statement,
                                 table_sqlalchemy):
        """ This method does a where, using multiple primary keys. """

        if not isinstance(entity_name, str):
            raise Exception("The entity name has not been configured.")

        if not isinstance(options['options'], dict):
            raise Exception("The entity options is not valid.")

        if not isinstance(statement, object):
            raise Exception("The statement is not valid.")

        entity_definitions = EntityUtils.get_entity_definitions(entity_name)

        for key in options['options']:
            column_sqlalchemy = getattr(
                        table_sqlalchemy.columns,
                        EntityUtils.translate_attribute_name(
                            entity_definitions=entity_definitions,
                            property_name=key))
            statement = statement.where(column_sqlalchemy ==
                                        options['options'][key])

        return statement
