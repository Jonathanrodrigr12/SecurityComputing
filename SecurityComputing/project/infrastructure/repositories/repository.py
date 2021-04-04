import json

from sqlalchemy import func, MetaData, and_, or_
from sqlalchemy import Table, Column, ForeignKey, Boolean, DateTime, Float, Integer, JSON, String
from project.configuration_manager import ConfigurationManger
from project.resources.utils.generals_utils import GeneralsUtils
from project.resources.utils.entity_utils import EntityUtils
from project.resources.utils.sqlalchemy_utils import SqlalchemyUtils


class Repository():

    def __init__(self, context, entity_name=None):
        self.__context = context

        self.__entity_name = entity_name

    def get_relation_validate(self, deviceId, servicePointId):

        utils_sqlalchemy = SqlalchemyUtils()
        session = self.__context.session()
        meta_data = MetaData(session, schema= self.__context.get_connection_string_configuration("schema"))
        array_data = utils_sqlalchemy.configure_table(self.__entity_name, meta_data)
        statement = array_data.select().where(or_(array_data.c.identifier == deviceId,array_data.c.identifier == servicePointId))
        with session as connection:
            query_result = connection.execute(statement)

        return query_result

    def get_brand_model(self, brand, model):
        utils_sqlalchemy = SqlalchemyUtils()
        session = self.__context.session()
        meta_data = MetaData(session, schema= self.__context.get_connection_string_configuration("schema"))
        array_data = utils_sqlalchemy.configure_table(self.__entity_name, meta_data)
        statement = array_data.select().where(and_(array_data.c.brand == brand,array_data.c.model == model))
        with session as connection:
            query_result = connection.execute(statement)  

        return query_result


    def query(self, operation, entity_name=None, options=None):
        context = self.__context

        have_id = False

        entity_name = entity_name or self.__entity_name

        if not isinstance(entity_name, str):
            raise Exception("The entity name has not been configured")

        if context is None:
            raise Exception("The database context has not been configured")

        if not isinstance(options, dict):
            options = {}

        if "id" in options:
            have_id = True

        session = context.session()

        meta_data = MetaData(session,
                             schema=context.\
                                get_connection_string_configuration("schema"))

        if entity_name == "device_insert":
            with session as connection:
                query_result = connection.add_all(options["values"])

            return True

        table_sqlalchemy = SqlalchemyUtils.configure_table(
            entity_name, meta_data)

        if (operation == "delete" or\
           operation == "select" or\
           operation == "update") and have_id:
            primary_key_columns = getattr(
               table_sqlalchemy.primary_key,
               "columns")

            if len(primary_key_columns) != 1:
                raise Exception("Common delete, update or selection operation requires a primary key definition")

            primary_key_column = next(iter(primary_key_columns))

        if operation == "select":
            if "distinct_column_name" in options or\
               "group_by" in options or\
               "filters" in options or\
               "order_by" in options or\
               "paginate" in options:
                statement =  SqlalchemyUtils.\
                    generate_select_statement(entity_name, table_sqlalchemy, options)

            else:
                statement = table_sqlalchemy.select()

        elif operation == "insert" or\
             operation == "update":
            if "values" not in options:
                raise Exception

            values = options["values"]
            statement_function = table_sqlalchemy.insert

            if operation == "update":
                if not isinstance(values, dict):
                    raise Exception("The values to update do not correspond to the expected format")

                try:
                    statement_function = table_sqlalchemy.update
                    values_statement = EntityUtils.get_editables_values(entity_name, values, True)

                except Exception as error:
                    raise Exception("Error getting entity editable values", error)

            else:
                if isinstance(values, dict):
                    values = [values]

                try:
                    values_statement = [EntityUtils.translate_dictionary(
                        entity_name=entity_name,
                        entity_properties=item) for item in values]

                except Exception as error:
                    raise Exception("", error)

            statement = statement_function(None).\
                values(values_statement)

        elif operation == "delete":
            if have_id or\
               "options" in options :
                statement = table_sqlalchemy.delete(None)    
            else:
                raise Exception("When requesting a deletion it is mandatory to specify the id of the record to delete")   
            

        if "options" in options and\
           (operation == "update" or \
           operation == "delete"):
            statement = SqlalchemyUtils.generate_where_statement(entity_name,
                                                                 options,
                                                                 statement,
                                                                 table_sqlalchemy)

        if have_id:
            statement = statement.where(primary_key_column == options["id"])
        
        with session as connection:
            query_result = connection.execute(statement)

        return query_result

    def count(self, entity_name=None, options=None):
        # Summary: Counts the number of records in a table or view according to the configured request
        # parameters:
        # - entity_name: This parameter indicates the entity to which we are going to refer
        # - options: this parameter is to make a filter regarding what is needed in the request
        # return: a result list

        query_result = self.query(
            "select",
            entity_name or self.__entity_name,
            options
        )

        result = query_result.rowcount

        return result

    def delete(self, id, entity_name=None):
        query_result = self.query(
            "delete",
            entity_name or self.__entity_name,
            {
                "id": id
            }
        )

        if query_result.rowcount != 1:
            raise Exception(
                "Fatal error: deletion operation has affected more than one column, {}".format(id))

        return True

    def insert(self, values, entity_name=None):
        query_result = self.query(
            "insert",
            entity_name or self.__entity_name,
            {"values": values}
        )

        if query_result == True:
            return query_result

        if query_result.rowcount == 0: 
            raise Exception

        return True

    def select(self, entity_name=None, options=None):
        # T
        result = []
        fail = False
        error_detected = None

        query_result = self.query(
            "select",
            entity_name or self.__entity_name,
            options
        )

        for row in query_result:
            try:
                result.append(
                    EntityUtils.translate_dictionary(
                        entity_name=entity_name or self.__entity_name,
                        table=dict(row))
                )

            except Exception as error:
                error_detected = error
                fail = True
                break

        if fail:
            raise Exception("", error_detected)

        return result

    def select_all(self, entity_name=None):
        # T
        result = []
        fail = False
        error_detected = None

        query_result = self.query(
            "select",
            entity_name
        )

        for row in query_result:
            try:
                result.append(
                    EntityUtils.translate_dictionary(
                        entity_name=entity_name or self.__entity_name,
                        table=dict(row)))

            except Exception as error:
                fail = True
                error_detected = error
                break

        if fail:
            raise Exception("", error_detected)

        return result

    def select_distinct(self, column_name, entity_name=None):
        # T
        result = []
        fail = False
        error_detected = None

        if not isinstance(column_name, str):
            raise Exception("")

        query_result = self.query(
            "select",
            {"distinct_column_name": column_name}
        )

        for row in query_result:
            try:
                result.append(
                    EntityUtils.translate_dictionary(
                        entity_name=entity_name or self.__entity_name,
                        table=dict(row)))

            except Exception as error:
                fail = True
                error_detected = error
                break

        if fail:
            raise Exception("", error_detected)

        return result

    def select_group_by(self, column_name, with_total_count=False, entity_name=None, options=None):
        # T
        result = []
        fail = False
        error_detected = None

        if not isinstance(column_name, str):
            raise Exception("")

        if not isinstance(with_total_count, bool):
            with_total_count = False

        options = options or {}
        options["group_by"] = {
            "column_name": column_name,
            "with_total_count": with_total_count
        }

        query_result = self.query(
            "select",
            entity_name or self.__entity_name,
            options
        )

        for row in query_result:
            try:
                result.append(row)

            except Exception as error:
                fail = True
                error_detected = error
                break

        if fail:
            raise Exception("", error_detected)

        return result

    def select_one(self, id, entity_name=None):
        # T
        result = []
        fail = False
        error_detected = None

        query_result = self.query(
            "select",
            entity_name,
            {
                "id": id
            }
        )

        for row in query_result:
            try:
                result.append(
                    EntityUtils.translate_dictionary(
                        entity_name=entity_name or self.__entity_name,
                        table=dict(row))
                )

            except Exception as error:
                fail = True
                error_detected = error
                break

        if fail:
            raise Exception("", error_detected)

        return result

    def update(self, id, values, entity_name=None):
        query_result = self.query(
            "update",
            entity_name or self.__entity_name,
            {
                "id": id,
                "values": values
            }
        )

        if query_result.rowcount != 1:
            raise Exception

        return True

    def update_compound_key(self, ids, values, entity_name=None):
        """ This method is using for tables  update, when this have a compound primary key. """
        try:
            query_result = self.query(
                "update",
                entity_name or self.__entity_name,
                {
                    "options": ids,
                    "values": values
                }
            )
        except Exception as error:
            error_detected = error

            if query_result.rowcount != 1:
                raise Exception("Fatal Error: The data was not updated.", error_detected)

        return True

    def delete_compound_key(self, ids, entity_name=None):
        """ This method is using for tables  delete, when this have a compound primary key. """
        try:
            query_result = self.query(
                "delete",
                entity_name or self.__entity_name,
                {
                    "options": ids
                }
            )
        except Exception as error:
            error_detected = error

        if query_result.rowcount != 1:
            raise Exception("Error deleting.", error_detected)

        return True    
